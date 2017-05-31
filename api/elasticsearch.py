import json
import re

from pyelasticsearch import ElasticSearch as PyElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError, BulkError
import http.client
http.client._MAXHEADERS = 1000
from django.conf import settings
from collections import OrderedDict
from django.db.models import ForeignKey, Q

from grid.views.change_deal_view import ChangeDealView
from grid.forms.deal_spatial_form import DealSpatialForm
from landmatrix.models.activity import HistoricalActivity
from grid.forms.parent_investor_formset import ParentCompanyForm
from grid.forms.investor_form import ParentInvestorForm
from landmatrix.models.investor import Investor, InvestorVentureInvolvement

FIELD_TYPE_MAPPING = {
    'IntegerField': 'integer',
    'CharField': 'string', # use 'exact_value' instead of string??
    'AreaField': 'geo_shape',
    'FloatField': 'float',
}

DOC_TYPES_ACTIVITY = ('deal', 'location', 'data_source', 'contract')
DOC_TYPES_INVESTOR = ('investor', 'involvement')

_landmatrix_properties = None
def get_elasticsearch_properties(doc_type=None):
    """ Generates a list of elasticsearch document properties from all filter fields in the
    attribute model forms. doc_type can be deal, location, contract, data_source, involvement or investor """
    global _landmatrix_properties
    
    if _landmatrix_properties is None:
        # Get field type mappings for deal
        _landmatrix_properties = OrderedDict()
        _landmatrix_properties['deal'] = {
            'id': {'type': 'string'}, # use 'exact_value' instead of string??
            'historical_activity_id': {'type': 'integer'},
            'activity_identifier': {'type': 'integer'},
            'geo_point': {'type': 'geo_point'},
            'status': {'type': 'integer'},
        }
        _landmatrix_properties['location'] = {
            'id': {'type': 'string'},
            'fk_activity': {'type': 'keyword'},
        }
        _landmatrix_properties['contract'] = {
            'id': {'type': 'string'},
            'fk_activity': {'type': 'keyword'},
        }
        _landmatrix_properties['data_source'] = {
            'id': {'type': 'string'},
            'fk_activity': {'type': 'keyword'},
        }
        _landmatrix_properties['involvement'] = {
            'id': {'type': 'string'},
            'fk_activity': {'type': 'keyword'},
            'fk_investor': {'type': 'keyword'},
        }
        _landmatrix_properties['investor'] = {
            'id': {'type': 'string'},
        }
        # Doc types: deal, location, contract and data_source
        for form in ChangeDealView.FORMS:
            formset_name = hasattr(form, "form") and form.Meta.name or None
            form = formset_name and form.form or form
            for name, field in form.base_fields.items():
                # Title field?
                if name.startswith('tg_') and not name.endswith('_comment'):
                    continue
                _landmatrix_properties['deal'][name] = {
                    'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')
                }
                if formset_name:
                    _landmatrix_properties[formset_name][name] = {
                        'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')
                    }
        # Doc type: involvement
        for name, field in ParentCompanyForm.base_fields.items():
            # Title field?
            if name.startswith('tg_') and not name.endswith('_comment'):
                continue
            _landmatrix_properties['involvement'][name] = {
                'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')
            }
        # Doc type: investor
        for name, field in ParentInvestorForm.base_fields.items():
            # Title field?
            if name.startswith('tg_') and not name.endswith('_comment'):
                continue
            _landmatrix_properties['investor'][name] = {
                'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')
            }
    if doc_type:
        return _landmatrix_properties[doc_type]
    else:
        return _landmatrix_properties


class ElasticSearch(object):
    conn = None
    url = settings.ELASTICSEARCH_URL
    index_name = settings.ELASTICSEARCH_INDEX_NAME
    stdout = None
    stderr = None

    def __init__(self, index_name=None, stdout=None, stderr=None):
        self.conn = PyElasticSearch()
        if index_name:
            self.index_name = index_name
        if stdout:
            self.stdout = stdout
        if stderr:
            self.stderr = stderr

    def get_spatial_properties(self):
        return DealSpatialForm.base_fields.keys()

    def create_index(self, delete=True):
        if delete:
            try:
                self.conn.delete_index(self.index_name)
            except ElasticHttpNotFoundError as e:
                pass 
        mappings = dict((k, {'properties': v}) for k, v in get_elasticsearch_properties().items())
        self.conn.create_index(self.index_name, settings={'mappings': mappings})

    def index_activity_by_id(self, activity_id):
        activity = HistoricalActivity.objects.get(pk=activity_id)
        return self.index_activity(activity)

    def index_activity(self, activity):
        for doc_type in DOC_TYPES_ACTIVITY:
            docs = self.get_activity_documents(activity, doc_type=doc_type)
            if len(docs) > 0:
                try:
                    self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
                        index=self.index_name,
                        doc_type=doc_type)
                except BulkError as e:
                    for error in e.errors:
                        stderr and stderr.write('%s: %s (caused by %s: %s, ID: %s)' % (
                                error['index']['error']['type'],
                                error['index']['error']['reason'],
                                error['index']['error']['caused_by']['type'],
                                error['index']['error']['caused_by']['reason'],
                                error['index']['_id']
                              ))

    def index_investor(self, investor):
        for doc_type in DOC_TYPES_INVESTOR:
            docs = self.get_investor_documents(investor, doc_type=doc_type)
            if len(docs) > 0:
                try:
                    self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
                        index=self.index_name,
                        doc_type=doc_type)
                except BulkError as e:
                    for error in e.errors:
                        stderr and stderr.write('%s: %s (caused by %s: %s, ID: %s)' % (
                                error['index']['error']['type'],
                                error['index']['error']['reason'],
                                error['index']['error']['caused_by']['type'],
                                error['index']['error']['caused_by']['reason'],
                                error['index']['_id']
                              ))

    def index_activity_documents(self, activity_identifiers=[]):
        activity_identifiers = activity_identifiers or HistoricalActivity.objects.filter(fk_status__in=(
                HistoricalActivity.STATUS_ACTIVE, HistoricalActivity.STATUS_PENDING, 
                HistoricalActivity.STATUS_OVERWRITTEN, HistoricalActivity.STATUS_DELETED
            )).distinct().values_list('activity_identifier', flat=True).distinct()

        for doc_type in DOC_TYPES_ACTIVITY:
            docs = []
            # Collect documents
            self.stdout and self.stdout.write('Collect %ss for %i deals...' % (doc_type, len(activity_identifiers)))
            for activity_identifier in activity_identifiers:
                for activity in self.get_activity_versions(activity_identifier):
                    docs.extend(self.get_activity_documents(activity, doc_type=doc_type))
            # Bulk index documents
            self.stdout and self.stdout.write('Index %i %ss...' % (len(docs), doc_type))
            if len(docs) > 0:
                try:
                    self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
                        index=self.index_name,
                        doc_type=doc_type)
                except BulkError as e:
                    for error in e.errors:
                        self.stderr and self.stderr.write('%s: %s (caused by %s: %s, ID: %s)' % (
                                error['index']['error']['type'],
                                error['index']['error']['reason'],
                                error['index']['error']['caused_by']['type'],
                                error['index']['error']['caused_by']['reason'],
                                error['index']['_id']
                              ))

    def index_investor_documents(self):
        investors = Investor.objects.all()

        for doc_type in DOC_TYPES_INVESTOR:
            docs = []
            # Collect documents
            self.stdout and self.stdout.write('Collect %ss for %i investors...' % (doc_type, investors.count()))
            for investor in investors:
                docs.extend(self.get_investor_documents(investor, doc_type=doc_type))
            # Bulk index documents
            self.stdout and self.stdout.write('Index %i %ss...' % (len(docs), doc_type))
            if len(docs) > 0:
                try:
                    self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
                        index=self.index_name,
                        doc_type=doc_type)
                except BulkError as e:
                    for error in e.errors:
                        stderr and stderr.write('%s: %s (caused by %s: %s, ID: %s)' % (
                                error['index']['error']['type'],
                                error['index']['error']['reason'],
                                error['index']['error']['caused_by']['type'],
                                error['index']['error']['caused_by']['reason'],
                                error['index']['_id']
                              ))

    #def index_activity_by_version(self, activity_identifier):
    #    for doc_type in _landmatrix_properties.keys():
    #        docs = self.get_documents_for_activity_version(activity_identifier, doc_type=doc_type)
    #        if len(docs) > 0:
    #            try:
    #                self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
    #                    index=self.index_name,
    #                    doc_type=doc_type)
    #            except BulkError as e:
    #                for error in e.errors:
    #                    stderr and stderr.write('%s: %s (caused by %s: %s, ID: %s)' % (
    #                            error['index']['error']['type'],
    #                            error['index']['error']['reason'],
    #                            error['index']['error']['caused_by']['type'],
    #                            error['index']['error']['caused_by']['reason'],
    #                            error['index']['_id']
    #                          ))

    def get_activity_versions(self, activity_identifier):
        versions = []
        # get the newest non-pending, readable historic version:
        try:
            newest = HistoricalActivity.objects.filter(activity_identifier=activity_identifier, fk_status__in=(
                HistoricalActivity.STATUS_ACTIVE, HistoricalActivity.STATUS_OVERWRITTEN, HistoricalActivity.STATUS_DELETED)).distinct().latest()
            if newest:
                versions.append(newest)
        except HistoricalActivity.DoesNotExist:
            newest = None
            
        # get all pendings
        pendings = HistoricalActivity.objects.filter(activity_identifier=activity_identifier, fk_status_id=HistoricalActivity.STATUS_PENDING).distinct()
        versions.extend(pendings)
        
        return versions

    def get_activity_documents(self, activity, doc_type='deal'):
        docs = []
        spatial_names = self.get_spatial_properties()
        spatial_attrs = {}
        deal_attrs = {
            'historical_activity_id': activity.id,
            'activity_identifier': activity.activity_identifier,
            'status': activity.fk_status_id,
        }
        for a in activity.attributes.select_related('fk_group__name').all().order_by('fk_group__name'):
            # do not include the django object id
            if a.name == 'id': 
                continue
            value = a.value

            # Area field?
            if a.name and 'area' in a.name and a.polygon is not None:
                # Get polygon
                value = json.loads(a.polygon.json)
                # Apparently this is case sensitive: MultiPolygon as provided by
                # the GeoJSON does not work ...
                value['type'] = 'multipolygon'
            # do not include empty values
            if value is None or value == '':
                continue

            # Doc types: location, data_source or contract
            group_match = re.match('(?P<doc_type>location|data_source|contract)_(?P<count>\d+)', a.fk_group.name)
            if group_match:
                dt, count = group_match.groupdict()['doc_type'], int(group_match.groupdict()['count'])
                # Fallback for wrong entries, should be deprecated soon
                if count == 0:
                    count = 1
                if doc_type == dt:
                    while len(docs) < count:
                        docs.append({
                            'id': '%i_%i' % (a.id, count),
                            'activity_id': a.id,
                        })
                    docs[count-1][a.name] = [value,]
                # Set doc type counter within deal doc type (for location/data_source/contract)
                elif doc_type == 'deal':
                    key = '%s_count' % dt
                    if key not in deal_attrs.keys():
                        deal_attrs[key] = count
                    elif deal_attrs[key] < count:
                        deal_attrs[key] = count
            # Doc type: deal
            if doc_type == 'deal':
                if a.name in spatial_names:
                    if a.fk_group_id in spatial_attrs:
                        spatial_attrs[a.fk_group_id][a.name] = value
                    else:
                        spatial_attrs[a.fk_group_id] = {a.name: value}
                elif a.name in deal_attrs:
                    deal_attrs[a.name].append(value)
                else:
                    deal_attrs[a.name] = [value,]

        # Create single document for each location
        # FIXME: Saving single deals for each location might be deprecated since we have doc_type location now?
        for group, group_attrs in spatial_attrs.items():
            doc = deal_attrs.copy()
            doc.update(group_attrs)
            # Set unique ID for location (deals can have multiple locations)
            doc['id'] = '%s_%s' % (doc['historical_activity_id'], group)
            if 'point_lat' in group_attrs and 'point_lon' in group_attrs:
                doc['geo_point'] = '%s,%s' % (group_attrs.get('point_lat'), group_attrs.get('point_lon'))
            # FIXME: we dont really need 'point_lat' and 'point_lon' here,
            # so we should pop them from doc when adding 'geo_point'
            docs.append(doc)

        return docs

    def get_investor_documents(self, investor, doc_type='investor'):
        docs = []
        # Doc types: involvement and investor
        if doc_type == 'involvement':
            ivis = InvestorVentureInvolvement.objects.filter(Q(fk_venture=investor) | Q(fk_investor=investor))
            for ivi in ivis:
                doc = {}
                for field in ivi._meta.local_fields:
                    if isinstance(field, ForeignKey):
                        doc[field.name] = getattr(ivi, '%s_id' % field.name)
                    else:
                        doc[field.name] = getattr(ivi, field.name)
                docs.append(doc)
        elif doc_type == 'investor':
            doc = {}
            for field in investor._meta.local_fields:
                if isinstance(field, ForeignKey):
                    doc[field.name] = getattr(investor, '%s_id' % field.name)
                else:
                    doc[field.name] = getattr(investor, field.name)
            docs.append(doc)
        return docs

    def refresh_index(self):
        self.conn.refresh(self.index_name)
        
    def search(self, elasticsearch_query):
        """ Executes paginated queries until all results have been retrieved. 
            @return: The full list of hits. """
        start = 0
        size = 10000 # 10000 is the default elasticsearch max_window_size (pagination is cheap, so more is not necessarily better)
        raw_result_list = []
        
        done = False
        while not done:
            query = {
                'query': elasticsearch_query,
                'from': start,
                'size': size
            }
            query_result = self.conn.search(query, index=self.index_name)
            raw_result_list.extend(query_result['hits']['hits'])
            results_total = query_result['hits']['total']
            
            if len(raw_result_list) >= results_total:
                done = True
            else:
                start = len(raw_result_list)
        
        self.stdout and self.stdout.write('\nElasticsearch returned %i documents from a total of %i \n\n' % (
            len(raw_result_list), query_result['hits']['total'])
        )
        
        return raw_result_list

# Init two connections
es_search = ElasticSearch()
es_save = ElasticSearch()
