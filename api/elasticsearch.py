import json
import re

from pyelasticsearch import ElasticSearch as PyElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError, BulkError
import http.client
http.client._MAXHEADERS = 1000
from collections import OrderedDict

from django.conf import settings
from django.db.models import ForeignKey, Q
from django.forms import MultiValueField
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _

from grid.views.change_deal_view import ChangeDealView
from landmatrix.models.activity import HistoricalActivity, Activity
from grid.forms.investor_form import ExportInvestorForm
from grid.forms.parent_investor_formset import InvestorVentureInvolvementForm
from landmatrix.models.investor import Investor, InvestorVentureInvolvement
from grid.utils import get_spatial_properties

FIELD_TYPE_MAPPING = {
    'IntegerField': 'integer',
    'CharField': 'string', # use 'exact_value' instead of string??
    'AreaField': 'geo_shape',
    'FloatField': 'float',
}

DOC_TYPES_ACTIVITY = ('deal', 'location', 'data_source', 'contract')
DOC_TYPES_INVESTOR = ('investor', 'involvement')

_landmatrix_mappings = None
def get_elasticsearch_properties(doc_type=None):
    """ Generates a list of elasticsearch document properties from all filter fields in the
    attribute model forms. doc_type can be deal, location, contract, data_source, involvement or investor """
    global _landmatrix_mappings
    
    if _landmatrix_mappings is None:
        # Get field type mappings for deal
        _landmatrix_mappings = OrderedDict()
        _landmatrix_mappings['deal'] = {
            'properties': {
                'id': {'type': 'string'}, # use 'exact_value' instead of string?
                'historical_activity_id': {'type': 'integer'},
                'activity_identifier': {'type': 'integer'},
                'geo_point': {'type': 'geo_point'},
                'status': {'type': 'integer'},
            }
        }
        _landmatrix_mappings['location'] = {
            '_parent': {'type': 'deal'},
            'properties': {
                'id': {'type': 'string'},
            }
        }
        _landmatrix_mappings['data_source'] = {
            '_parent': {'type': 'deal'},
            'properties': {
                'id': {'type': 'string'},
            }
        }
        _landmatrix_mappings['contract'] = {
            '_parent': {'type': 'deal'},
            'properties': {
                'id': {'type': 'string'},
            }
        }
        _landmatrix_mappings['involvement'] = {
            'properties': {
                'id': {'type': 'string'},
                'fk_activity': {'type': 'keyword'},
                'fk_investor': {'type': 'keyword'},
            }
        }
        _landmatrix_mappings['investor'] = {
            'properties': {
                'id': {'type': 'string'},
            }
        }
        # Doc types: deal, location, contract and data_source
        for form in ChangeDealView.FORMS:
            formset_name = hasattr(form, "form") and form.Meta.name or None
            form = formset_name and form.form or form
            for name, field in form.base_fields.items():
                # Title field?
                if name.startswith('tg_') and not name.endswith('_comment'):
                    continue
                mappings = {
                    name: {'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')},
                    '%s_export' % name: {'type': 'string'},
                }
                # Additionally save complete attribute (including value2, date, is_current) for all MultiValueFields
                if isinstance(field, MultiValueField):
                    mappings['%s_attr' % name] = {'type': 'nested'}
                _landmatrix_mappings['deal']['properties'].update(mappings)
                if formset_name:
                    _landmatrix_mappings[formset_name]['properties'].update(mappings)

        # Doc type: involvement
        for field_name, field in InvestorVentureInvolvementForm.base_fields.items():
            # Title field?
            if field_name.startswith('tg_') and not field_name.endswith('_comment'):
                continue
            _landmatrix_mappings['involvement']['properties'].update({
                field_name: {'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')},
                '%s_export' % field_name: {'type': 'string'},
            })
        # Doc type: investor
        for field_name, field in ExportInvestorForm.base_fields.items():
            # Title field?
            if field_name.startswith('tg_') and not field_name.endswith('_comment'):
                continue
            _landmatrix_mappings['investor']['properties'].update({
                field_name: {'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')},
                '%s_export' % field_name: {'type': 'string'},
            })
    if doc_type:
        return _landmatrix_mappings[doc_type]
    else:
        return _landmatrix_mappings


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

    def create_index(self, delete=True):
        if delete:
            try:
                self.conn.delete_index(self.index_name)
            except ElasticHttpNotFoundError as e:
                pass 
        mappings = dict((k, v) for k, v in get_elasticsearch_properties().items())
        self.conn.create_index(self.index_name, settings={'mappings': mappings})

    def index_activity_by_id(self, activity_id):
        activity = HistoricalActivity.objects.get(pk=activity_id)
        return self.index_activity(activity)

    def index_activity(self, activity):
        for doc_type in DOC_TYPES_ACTIVITY:
            docs = self.get_activity_documents(activity, doc_type=doc_type)
            if len(docs) > 0:
                try:
                    self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id'), parent=doc.pop('_parent', None)) for doc in docs),
                        index=self.index_name,
                        doc_type=doc_type)
                except BulkError as e:
                    for error in e.errors:
                        msg = '%s: %s on ID %s' % (
                                error['index']['error']['type'],
                                error['index']['error']['reason'],
                                error['index']['_id']
                              )
                        if 'caused_by' in error['index']['error']:
                            msg += ' (%s: %s)' % (
                                error['index']['error']['caused_by']['type'],
                                error['index']['error']['caused_by']['reason']
                            )
                        self.stderr and self.stderr.write(msg)

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
                        msg = '%s: %s on ID %s' % (
                                error['index']['error']['type'],
                                error['index']['error']['reason'],
                                error['index']['_id']
                              )
                        if 'caused_by' in error['index']['error']:
                            msg += ' (%s: %s)' % (
                                error['index']['error']['caused_by']['type'],
                                error['index']['error']['caused_by']['reason']
                            )
                        self.stderr and self.stderr.write(msg)

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
                paginator = Paginator(docs, 1000)
                for page in paginator.page_range:
                    try:
                        self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id'), parent=doc.pop('_parent', None)) for doc in paginator.page(page)),
                            index=self.index_name,
                            doc_type=doc_type)
                    except BulkError as e:
                        for error in e.errors:
                            msg = '%s: %s on ID %s' % (
                                error['index']['error']['type'],
                                error['index']['error']['reason'],
                                error['index']['_id']
                            )
                            if 'caused_by' in error['index']['error']:
                                msg += ' (%s: %s)' % (
                                    error['index']['error']['caused_by']['type'],
                                    error['index']['error']['caused_by']['reason']
                                )
                            self.stderr and self.stderr.write(msg)
                    self.conn.refresh()



    def index_investor_documents(self):
        investors = Investor.objects.public().order_by('investor_identifier', '-id').distinct('investor_identifier')

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
                        msg = '%s: %s on ID %s' % (
                                error['index']['error']['type'],
                                error['index']['error']['reason'],
                                error['index']['_id']
                              )
                        if 'caused_by' in error['index']['error']:
                            msg += ' (%s: %s)' % (
                                error['index']['error']['caused_by']['type'],
                                error['index']['error']['caused_by']['reason']
                            )
                        self.stderr and self.stderr.write(msg)

    #def index_activity_by_version(self, activity_identifier):
    #    for doc_type in _landmatrix_mappings.keys():
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
        deal_attrs = {
            'id': activity.activity_identifier,
            'activity_identifier': activity.activity_identifier,
            'historical_activity_id': activity.id,
            'status': activity.fk_status_id,
        }

        # Todo: Is there a nice way to prevent this extra Activity query?
        # e.g. if we save is_public/deal_scope as ActivityAttributes
        try:
            public_activity = Activity.objects.get(activity_identifier=activity.activity_identifier)
            deal_attrs.update({
                'is_public': public_activity.is_public,
                'deal_scope': public_activity.deal_scope,
                'deal_size': public_activity.deal_size,
                'current_negotiation_status': public_activity.negotiation_status,
                'top_investors': public_activity.top_investors,
            })
        except Activity.DoesNotExist:
            # Fixme: This should not happen
            self.stderr.write(_('Missing activity for historical activity %i (Activity identifier: #%i)' % (
                activity.id,
                activity.activity_identifier
            )))
        except Activity.MultipleObjectsReturned:
            # Fixme: This should not happen
            self.stderr.write(_('Too much activities for historical activity %i (Activity identifier: #%i)' % (
                activity.id,
                activity.activity_identifier
            )))


        for a in activity.attributes.select_related('fk_group__name').order_by('fk_group__name'):
            # do not include the django object id
            if a.name == 'id': 
                continue
            attribute = None
            attribute_key = '%s_attr' % a.name
            if attribute_key in _landmatrix_mappings['deal']['properties'].keys():
                attribute = {
                    'value': a.value,
                    'value2': a.value2,
                    'date': a.date,
                    'is_current': a.is_current,
                }
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
                count += 1
                if doc_type == dt:
                    while len(docs) < count:
                        docs.append({
                            '_parent': activity.activity_identifier,
                            'id': a.id,#'%i_%i' % (a.id, count),
                        })
                    docs[count-1][a.name] = [value,]
                # Set doc type counter within deal doc type (for location/data_source/contract)
                elif doc_type == 'deal':
                    # Set counter
                    key = '%s_count' % dt
                    if key not in deal_attrs.keys():
                        deal_attrs[key] = count
                    elif deal_attrs[key] < count:
                        deal_attrs[key] = count

                    # Create list with correct length to ensure formset values have the same index
                    if not a.name in deal_attrs:
                        deal_attrs[a.name] = [''] * count
                        if attribute:
                            deal_attrs[attribute_key] = [''] * count
                    else:
                        while len(deal_attrs[a.name]) < count:
                            deal_attrs[a.name].append('')
                            if attribute:
                                deal_attrs[attribute_key].append('')
                    deal_attrs[a.name][count-1] = value
                    if attribute:
                        deal_attrs['%s_attr' % a.name][count-1]= attribute

            # Doc type: deal and not formset
            elif doc_type == 'deal':
                if a.name in deal_attrs:
                    deal_attrs[a.name].append(value)
                    if '%s_attr' % a.name in _landmatrix_mappings['deal']['properties'].keys():
                        deal_attrs['%s_attr' % a.name].append(attribute)
                else:
                    deal_attrs[a.name] = [value,]
                    if '%s_attr' % a.name in _landmatrix_mappings['deal']['properties'].keys():
                        deal_attrs['%s_attr' % a.name] = [attribute,]

        if doc_type == 'deal':
            # Additionally save operational company attributes
            oc = Investor.objects.filter(investoractivityinvolvement__fk_activity__activity_identifier=activity.activity_identifier)
            if oc.count() > 0:
                oc = oc.first()
                for field in Investor._meta.fields:
                    if isinstance(field, ForeignKey):
                        deal_attrs['operational_company_%s' % field.name] = getattr(oc, '%s_id' % field.name)
                    else:
                        deal_attrs['operational_company_%s' % field.name] = getattr(oc, field.name)
            else:
                pass
                #self.stderr.write("Missing operational company for deal #%i" % activity.activity_identifier)

        # Create single document for each location
        # FIXME: Saving single deals for each location might be deprecated since we have doc_type location now?
        spatial_names = list(get_spatial_properties())
        for i in range(deal_attrs.get('location_count', 0)):
            doc = deal_attrs.copy()
            for name in spatial_names:
                if not name in doc:
                    continue
                if len(deal_attrs[name]) > i:
                    doc[name] = deal_attrs[name][i]
                else:
                    doc[name] = ''
            # Set unique ID for location (deals can have multiple locations)
            doc['id'] = '%s_%i' % (doc['id'], i)
            if 'point_lat' in doc and 'point_lon' in doc:
                doc['geo_point'] = '%s,%s' % (doc.get('point_lat'), doc.get('point_lon'))
            # FIXME: we dont really need 'point_lat' and 'point_lon' here,
            # so we should pop them from doc when adding 'geo_point'
            docs.append(doc)

        # Update docs with export values
        for doc in docs:
            doc.update(self.get_export_properties(doc, doc_type=doc_type))

        return docs

    def get_export_properties(self, doc, doc_type='deal'):
        if doc_type == 'investor':
            return ExportInvestorForm.export(doc)
        elif doc_type == 'involvement':
            return InvestorVentureInvolvementForm.export(doc)
        else:
            properties = {
                'deal_scope_export': doc.get('deal_scope', ''),
                'is_public_export': doc.get('is_public', False) and str(_('Yes')) or str(_('No')),
                'deal_size_export': doc.get('deal_size', ''),
                'current_negotiation_status_export': doc.get('current_negotiation_status', ''),
                'top_investors_export': doc.get('top_investors', ''),
            }
            # Doc types: deal, location, contract and data_source
            for form in ChangeDealView.FORMS:
                formset_name = hasattr(form, "form") and form.Meta.name or None
                form = formset_name and form.form or form
                properties.update(form.export(doc, formset=formset_name))
            properties.update(ExportInvestorForm.export(doc, prefix='operational_company_'))
            return properties

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

        # Update docs with export values
        for doc in docs:
            doc.update(self.get_export_properties(doc, doc_type=doc_type))

        return docs

    def refresh_index(self):
        self.conn.refresh(self.index_name)
        
    def search(self, elasticsearch_query, doc_type='deal'):
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
                'size': size,
            }
            query_result = self.conn.search(query, index=self.index_name, doc_type=doc_type)
            raw_result_list.extend(query_result['hits']['hits'])
            results_total = query_result['hits']['total']
            
            if len(raw_result_list) >= results_total:
                done = True
            else:
                start = len(raw_result_list)
        
        print('\nElasticsearch returned %i documents from a total of %i \n\n' % (
            len(raw_result_list), query_result['hits']['total'])
        )
        return raw_result_list

# Init two connections
es_search = ElasticSearch()
es_save = ElasticSearch()
