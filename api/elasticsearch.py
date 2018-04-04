import json
import re
import logging
logger = logging.getLogger('elasticsearch')
logger.setLevel('WARNING')

from pyelasticsearch import ElasticSearch as PyElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError, BulkError
import http.client
http.client._MAXHEADERS = 1000
from collections import OrderedDict

from django.conf import settings
from django.db.models import ForeignKey, Q
from django.forms import MultiValueField, ModelChoiceField, ChoiceField, BooleanField
from django.core.paginator import Paginator
from django.utils.translation import ugettext_lazy as _

from grid.views.change_deal_view import ChangeDealView
from landmatrix.models.activity import HistoricalActivity, Activity
from grid.forms.investor_form import ExportInvestorForm
from grid.forms.parent_investor_formset import InvestorVentureInvolvementForm
from landmatrix.models.investor import Investor, InvestorVentureInvolvement
from grid.utils import get_spatial_properties
from landmatrix.models.country import Country


FIELD_TYPE_MAPPING = {
    'CharField': 'keyword',
    'TextField': 'text',
    'FloatField': 'float',
    'IntegerField': 'integer',
    # don't use 'geo_shape' for areas (yet?), because elasticsearch takes parsing (too?) seriously,
    # which prevents deals from being indexed because of the following errors:
    # - invalid_shape_exception: Provided shape has duplicate consecutive coordinates
    # - invalid_shape_exception: Self-intersection at or near point
    'AreaField': 'text',
    'ChoiceField': 'keyword',
    'ModelChoiceField': 'keyword',
    'YearMonthDateValidator': 'keyword',
    'YearMonthDateField': 'keyword',
    'YearBasedField': 'keyword',
    'YearBasedBooleanField': 'keyword',
    'YearBasedIntegerField': 'keyword',
    'YearBasedFloatField': 'keyword',
    'YearBasedChoiceField': 'keyword',
    'YearBasedModelMultipleChoiceField': 'keyword',
    'YearBasedModelMultipleChoiceIntegerField': 'keyword',
    'YearBasedMultipleChoiceIntegerField': 'keyword',
    'MultiCharField': 'keyword',
    'UserModelChoiceField': 'keyword',
    'PrimaryInvestorField': 'keyword',
    'NestedMultipleChoiceField': 'keyword',
    'FileFieldWithInitial': 'keyword',
    'CountryField': 'keyword',
    'ActorsField': 'keyword',
    'MultiFileField': 'keyword',
}
FIELD_TYPE_FALLBACK = 'text'

DOC_TYPES_ACTIVITY = ('deal', 'location', 'data_source', 'contract', 'involvement_size')
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
                'id': {'type': 'text'}, # use 'exact_value' instead of string?
                'historical_activity_id': {'type': 'integer'},
                'history_date': {'type': 'date'},
                'activity_identifier': {'type': 'integer'},
                'geo_point': {'type': 'geo_point'},
                'status': {'type': 'integer'},
                'is_public': {'type': 'boolean'},
                'is_public_display': {'type': 'text'},
                'deal_scope': {'type': 'keyword'},
                'init_date': {'type': 'date',
                              'format': "yyyy-MM-dd||yyyy-MM||yyyy"},
                'current_negotiation_status': {'type': 'keyword'},
                'current_implementation_status': {'type': 'keyword'},
                'deal_size': {'type': 'integer'},
                'deal_country': {'type': 'keyword'},
                'top_investors': {'type': 'keyword'},
                'investor_country': {'type': 'keyword'},
                'investor_region': {'type': 'keyword'},
                'fully_updated_date': {'type': 'text'},
                'target_region': {'type': 'keyword'},
                'target_region_display': {'type': 'keyword'},
                'operating_company_region': {'type': 'keyword'},
                'operating_company_region_display': {'type': 'keyword'},
                'agricultural_produce': {'type': 'keyword'},
            }
        }
        _landmatrix_mappings['location'] = {
            '_parent': {'type': 'deal'},
            'properties': {
                'id': {'type': 'keyword'},
            }
        }
        _landmatrix_mappings['data_source'] = {
            '_parent': {'type': 'deal'},
            'properties': {
                'id': {'type': 'keyword'},
            }
        }
        _landmatrix_mappings['contract'] = {
            '_parent': {'type': 'deal'},
            'properties': {
                'id': {'type': 'keyword'},
            }
        }
        _landmatrix_mappings['involvement_size'] = {
            '_parent': {'type': 'deal'},
            'properties': {
                'id': {'type': 'keyword'},
                'deal_id': {'type': 'keyword'},
                'deal_scope': {'type': 'keyword'},
                'target_country': {'type': 'keyword'},
                'target_region': {'type': 'keyword'},
                'investor_id': {'type': 'keyword'},
                'investor_country': {'type': 'keyword'},
                'investor_region': {'type': 'keyword'},
                'deal_size': {'type': 'integer'},
            }
        }
        _landmatrix_mappings['involvement'] = {
            'properties': {
                'id': {'type': 'keyword'},
            }
        }
        _landmatrix_mappings['investor'] = {
            'properties': {
                'id': {'type': 'keyword'},
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
                field_type = FIELD_TYPE_MAPPING.get(field.__class__.__name__,
                                                    FIELD_TYPE_FALLBACK)
                field_mappings = {}
                field_mappings[name] = {'type': field_type}
                if isinstance(field, (ChoiceField, ModelChoiceField, MultiValueField,
                                      BooleanField)):
                    field_mappings['%s_display' % name] = {'type': field_type}
                # Additionally save complete attribute (including value2, date, is_current) for all MultiValueFields
                if isinstance(field, MultiValueField):
                    field_mappings['%s_attr' % name] = {'type': 'nested'}
                _landmatrix_mappings['deal']['properties'].update(field_mappings)
                if formset_name:
                    _landmatrix_mappings[formset_name]['properties'].update(field_mappings)
        for field_name, field in ExportInvestorForm.base_fields.items():
            field_name = 'operating_company_%s' % field_name
            field_type = FIELD_TYPE_MAPPING.get(field.__class__.__name__, FIELD_TYPE_FALLBACK)
            field_mappings = {}
            field_mappings[field_name] = {'type': field_type}
            if isinstance(field, (ChoiceField, ModelChoiceField, MultiValueField, BooleanField)):
                field_mappings['%s_display' % field_name] = {'type': field_type}
            _landmatrix_mappings['deal']['properties'].update(field_mappings)

        # Doc type: involvement
        for field_name, field in InvestorVentureInvolvementForm.base_fields.items():
            field_type = FIELD_TYPE_MAPPING.get(field.__class__.__name__, FIELD_TYPE_FALLBACK)
            field_mappings = {}
            field_mappings[field_name] = {'type': field_type}
            if isinstance(field, (ChoiceField, ModelChoiceField, MultiValueField, BooleanField)):
                field_mappings['%s_display' % field_name] = {'type': field_type}
            _landmatrix_mappings['involvement']['properties'].update(field_mappings)
        # Doc type: investor
        for field_name, field in ExportInvestorForm.base_fields.items():
            field_type = FIELD_TYPE_MAPPING.get(field.__class__.__name__, FIELD_TYPE_FALLBACK)
            field_mappings = {}
            field_mappings[field_name] = {'type': field_type}
            if isinstance(field, (ChoiceField, ModelChoiceField, MultiValueField, BooleanField)):
                field_mappings['%s_display' % field_name] = {'type': field_type}
            _landmatrix_mappings['investor']['properties'].update(field_mappings)

        # FIXME: Location = Deal for now, that should be changed in the future
        _landmatrix_mappings['location'] = _landmatrix_mappings['deal']
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
        settings = {
            "analysis": {
                "analyzer": {
                    "no_lowercase": {
                        "type": "custom",
                        "tokenizer": "standard"
                    }
                }
            }
        }
        self.conn.create_index(self.index_name, settings={'mappings': mappings,
                                                          'settings': settings})

    def index_activity_by_id(self, activity_id):
        activity = HistoricalActivity.objects.get(pk=activity_id)
        return self.index_activity(activity)

    def delete_activity_by_id(self, activity_id):
        activity = HistoricalActivity.objects.get(pk=activity_id)
        return self.delete_activity(activity)

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

    def index_activity_documents(self, activity_identifiers=[], doc_types=DOC_TYPES_ACTIVITY):
        activity_identifiers = activity_identifiers or set(HistoricalActivity.objects.filter(
            fk_status__in=(
                HistoricalActivity.STATUS_ACTIVE, HistoricalActivity.STATUS_PENDING, 
                HistoricalActivity.STATUS_OVERWRITTEN, HistoricalActivity.STATUS_DELETED
            )).values_list('activity_identifier', flat=True).distinct())
        #activity_identifiers = list(activity_identifiers)[:5]
        #activity_identifiers = [352,]
        for doc_type in doc_types:
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

    def index_investor_documents(self, doc_types=DOC_TYPES_INVESTOR):
        investors = Investor.objects.public().order_by('investor_identifier', '-id').distinct('investor_identifier')

        for doc_type in doc_types:
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
    #    for doc_type in get_elasticsearch_properties().keys():
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
                HistoricalActivity.STATUS_ACTIVE,
                HistoricalActivity.STATUS_OVERWRITTEN,
                HistoricalActivity.STATUS_DELETED)).distinct().latest()
            if newest:# and not newest.fk_status_id == HistoricalActivity.STATUS_DELETED:
                versions.append(newest)
        except HistoricalActivity.DoesNotExist:
            newest = None
            
        # get newer pendings
        pendings = HistoricalActivity.objects.filter(activity_identifier=activity_identifier,
                                                     fk_status_id=HistoricalActivity.STATUS_PENDING).distinct()
        if newest:
            pendings.filter(history_date__gt=newest.history_date)
        versions.extend(pendings)
        
        return versions

    def get_activity_documents(self, activity, doc_type='deal'):
        # TODO: Split this method into smaller chunks
        docs = []
        if doc_type in ('deal', 'location', 'data_source', 'contract'):
            deal_attrs = {
                # don't use activity identifier as ID, since we need to save multiple stati of a deal
                'id': activity.id,
                'activity_identifier': activity.activity_identifier,
                'historical_activity_id': activity.id,
                'history_date': activity.history_date.isoformat(),
                'status': activity.fk_status_id,
            }
            # TODO: Prevent extra Activity query
            # e.g. if we save is_public/deal_scope as ActivityAttributes
            public_activity = Activity.objects.filter(activity_identifier=activity.activity_identifier).order_by('-id').first()
            if public_activity:
                top_investors = public_activity.get_top_investors()
                investor_countries = public_activity.get_investor_countries()
                deal_attrs.update({
                    'is_public': public_activity.is_public_deal(),
                    'deal_scope': public_activity.get_deal_scope(),
                    'deal_size': public_activity.get_deal_size(),
                    'init_date': public_activity.get_init_date() or None,
                    'current_negotiation_status': public_activity.get_negotiation_status(),
                    'current_implementation_status': public_activity.get_implementation_status(),
                    'top_investors': public_activity.format_investors(top_investors),
                    'investor_country': [c.id for c in investor_countries],
                    'investor_country_display': [c.name for c in investor_countries],
                    'fully_updated_date': public_activity.get_fully_updated_date(),
                    'agricultural_produce': public_activity.get_agricultural_produce(),
                })
            else:
                # Fixme: This should not happen
                self.stderr and self.stderr.write(_('Missing activity for historical activity %i (Activity identifier: #%i)' % (
                    activity.id,
                    activity.activity_identifier
                )))
            #except Activity.MultipleObjectsReturned:
            #    # Fixme: This should not happen
            #    self.stderr and self.stderr.write(_('Too much activities for historical activity %i (Activity identifier: #%i)' % (
            #        activity.id,
            #        activity.activity_identifier
            #    )))

            for a in activity.attributes.select_related('fk_group__name').order_by('fk_group__name'):
                # do not include the django object id
                if a.name == 'id':
                    continue
                attribute = None
                attribute_key = '%s_attr' % a.name
                if attribute_key in get_elasticsearch_properties()['deal']['properties'].keys():
                    attribute = {
                        'value': a.value.strip() if a.value else None,
                        'value2': a.value2.strip() if a.value2 else None,
                        'date': a.date,
                        'is_current': a.is_current,
                    }
                value = a.value.strip() if a.value else None
                # Area field?
                if a.name and 'area' in a.name and a.polygon is not None:
                    # Get polygon
                    #value = json.loads(a.polygon.json)
                    # Apparently this is case sensitive: MultiPolygon as provided by the GeoJSON does not work
                    #value['type'] = 'multipolygon'
                    value = a.polygon.json or ''
                # do not include empty values
                if value is None or value == '':
                    continue

                # Doc types: location, data_source or contract
                group_match = a.fk_group and a.fk_group.name or ''
                group_match = re.match('(?P<doc_type>location|data_source|contract)_(?P<count>\d+)', group_match)
                if group_match:
                    dt, count = group_match.groupdict()['doc_type'], int(group_match.groupdict()['count'])
                    if count == 0:
                        # Fixme: This should not happen
                        self.stderr and self.stderr.write(
                            _('Attribute group "%s" is invalid counter (groups should start with 1) for historical activity %i (Activity identifier: #%i)' % (
                                a.fk_group and a.fk_group.name or '',
                                activity.id,
                                activity.activity_identifier
                            )))
                        continue
                    if doc_type in ('data_source', 'contract'):
                        if doc_type == dt:
                            while len(docs) < count:
                                docs.append({
                                    '_parent': activity.id,
                                    'id': a.id,#'%i_%i' % (a.id, count),
                                })
                            docs[count-1][a.name] = [value,]
                    # Set doc type counter within deal doc type (for data_source/contract)
                    elif doc_type in ('deal', 'location'):
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

                # Doc type: deal/location
                if doc_type in ('deal', 'location'):
                    if a.name in deal_attrs:
                        deal_attrs[a.name].append(value)
                        if '%s_attr' % a.name in get_elasticsearch_properties()['deal']['properties'].keys():
                            deal_attrs['%s_attr' % a.name].append(attribute)
                    else:
                        deal_attrs[a.name] = [value,]
                        if '%s_attr' % a.name in get_elasticsearch_properties()['deal']['properties'].keys():
                            deal_attrs['%s_attr' % a.name] = [attribute,]

            if doc_type in ('deal', 'location'):
                # Additionally save operating company attributes
                oc = Investor.objects.filter(investoractivityinvolvement__fk_activity__activity_identifier=activity.activity_identifier)
                if oc.count() > 0:
                    oc = oc.first()
                    for field in Investor._meta.fields:
                        if isinstance(field, ForeignKey):
                            deal_attrs['operating_company_%s' % field.name] = getattr(oc, '%s_id' % field.name)
                        else:
                            deal_attrs['operating_company_%s' % field.name] = getattr(oc, field.name)
                else:
                    pass
                    #self.stderr and self.stderr.write("Missing operating company for deal #%i" % activity.activity_identifier)

            if doc_type in ('deal', 'location'):
                deal_attrs.update(self.get_display_properties(deal_attrs, doc_type=doc_type))
                deal_attrs.update(self.get_spatial_properties(deal_attrs, doc_type=doc_type))
                if doc_type ==  'location':
                    # Create single document for each location
                    spatial_names = list(get_spatial_properties()) + ['target_region', 'geo_point']
                    for i in range(deal_attrs.get('location_count', 0)):
                        doc = deal_attrs.copy()
                        for name in spatial_names:
                            if name not in doc:
                                continue
                            if len(deal_attrs[name]) > i:
                                doc[name] = deal_attrs[name][i]
                            else:
                                doc[name] = ''
                            name_display = '%s_display' % name
                            if name_display in deal_attrs and len(deal_attrs[name_display]) > i:
                                doc[name_display] = deal_attrs[name_display][i]
                        # Set unique ID for location (deals can have multiple locations)
                        doc['id'] = '%s_%i' % (doc['activity_identifier'], i)
                        docs.append(doc)
                elif doc_type == 'deal':
                    docs.append(deal_attrs)
        elif doc_type == 'involvement_size':
            # Deal size split by investor (required for fast aggregation e.g. in charts)
            # A) Operating company with no parent companies gets assigned complete deal size
            # B) All Parent companies with no parents get assigned the complete deal size each
            # Exception: Parent company multiple roles, assign deal size only once.
            public_activity = Activity.objects.filter(
                activity_identifier=activity.activity_identifier).order_by('-id').first()
            if public_activity:
                country = public_activity.target_country
                deal_attrs = {
                    '_parent': activity.id,
                    'deal_id': activity.id,
                    'activity_identifier': activity.id,
                    'target_country': country.id if country else None,
                    'target_country_display': country.name if country else None,
                    'target_region': country.fk_region_id if country else None,
                    'target_region_display': country.fk_region.name if country else None,
                    'deal_size': public_activity.get_deal_size(),
                    'deal_scope': public_activity.get_deal_scope(),
                }
                for investor in public_activity.get_top_investors():
                    country = None
                    if investor.fk_country_id:
                        try:
                            # Use defer, because direct access to ForeignKey is very slow sometimes
                            country = Country.objects.defer('geom').get(id=investor.fk_country_id)
                        except Country.DoesNotExist:
                            pass
                    doc = deal_attrs.copy()
                    doc.update({
                        'id': '%i-%i' % (activity.id, investor.id),
                        'investor_id': investor.id,
                        'investor_country': investor.fk_country_id,
                        'investor_country_display': country.name if country else None,
                        'investor_region': country.fk_region_id if country else None,
                        'investor_region_display': country.fk_region.name if country else None,
                    })
                    docs.append(doc)

        return docs

    def get_spatial_properties(self, doc, doc_type='deal'):
        properties = {
            'geo_point': [],
            'point_lat': [],
            'point_lon': [],
            'target_country': [],
            'target_country_display': [],
            'target_region': [],
            'target_region_display': [],
        }
        point_lat = doc.get('point_lat', [])
        point_lon = doc.get('point_lon', [])
        target_country = doc.get('target_country', [])
        for i in range(doc.get('location_count', 1)):
            if len(point_lat) > i and len(point_lon) > 1:
                # Parse values
                try:
                    parsed_lat, parsed_lon = float(point_lat[i]), float(point_lon[i])
                    properties['geo_point'].append('%s,%s' % (point_lat[i], point_lon[i]))
                except ValueError:
                    properties['geo_point'].append('0,0')
                properties['point_lat'].append(point_lat[i])
                properties['point_lon'].append(point_lon[i])
            else:
                properties['geo_point'].append('0,0')
                properties['point_lat'].append('0')
                properties['point_lon'].append('0')
            # Set target region
            if len(target_country) > i and target_country[i]:
                country = Country.objects.get(pk=target_country[i])
                properties['target_country'].append(country.id)
                properties['target_country_display'].append(country.name)
                region = country.fk_region
                properties['target_region'].append(region.id)
                properties['target_region_display'].append(region.name)
        return properties

    def get_display_properties(self, doc, doc_type='deal'):
        if doc_type == 'investor':
            return ExportInvestorForm.get_display_properties(doc)
        elif doc_type == 'involvement':
            return InvestorVentureInvolvementForm.get_display_properties(doc)
        elif doc_type in ('deal', 'location'):
            NEGOTIATION_STATUS_MAP = dict(Activity.NEGOTIATION_STATUS_CHOICES)
            current_negotiation_status = doc.get('current_negotiation_status')
            current_negotiation_status = NEGOTIATION_STATUS_MAP.get(current_negotiation_status)
            IMPLEMENTATION_STATUS_MAP = dict(Activity.IMPLEMENTATION_STATUS_CHOICES)
            current_implementation_status = doc.get('current_implementation_status')
            current_implementation_status = IMPLEMENTATION_STATUS_MAP.get(current_implementation_status)
            properties = {
                'is_public_display': doc.get('is_public', False) and str(_('Yes')) or str(_('No')),
                'current_negotiation_status_display': str(current_negotiation_status),
                'current_implementation_status_display': str(current_implementation_status),
            }
            for form in ChangeDealView.FORMS:
                formset_name = hasattr(form, "form") and form.Meta.name or None
                form = formset_name and form.form or form
                properties.update(form.get_display_properties(doc, formset=formset_name))
            properties.update(ExportInvestorForm.get_display_properties(doc,
                                                                        prefix='operating_company_'))
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

            # Append top_investors
            top_investors = investor.get_top_investors()
            doc['top_investors'] = investor.format_investors(top_investors)

            # Append involvements for quicker queries
            ivis = InvestorVentureInvolvement.objects.filter(fk_investor=investor)
            doc['parent_company_of'] = []
            doc['tertiary_investor_of'] = []
            for ivi in ivis:
                if ivi.role == InvestorVentureInvolvement.STAKEHOLDER_ROLE:
                    doc['parent_company_of'].append(ivi.fk_venture_id)
                elif ivi.role == InvestorVentureInvolvement.INVESTOR_ROLE:
                    doc['tertiary_investor_of'].append(ivi.fk_venture_id)
            docs.append(doc)

        # Update docs with export values
        for doc in docs:
            doc.update(self.get_display_properties(doc, doc_type=doc_type))

        return docs

    def refresh_index(self):
        self.conn.refresh(self.index_name)

    def search(self, query, doc_type='deal', sort=[], aggs={}):
        """ Executes paginated queries until all results have been retrieved. 
            @return: The full list of hits. """
        results = []
        
        scroll_id = None 
        while True:
            if scroll_id:
                es_query = scroll_id
                body = {
                    'scroll': '1m',
                    'scroll_id': scroll_id,
                }
                query_result = self.conn.send_request(
                    'GET',
                    ['_search', 'scroll'],
                    body)
                scroll_id = None
            else:
                es_query = {
                    'query': query,
                    'size': 1000,
                }
                if sort:
                    es_query['sort'] = sort
                if aggs:
                    es_query['aggs'] = aggs
                query_params = {'scroll':'1m'}
                query_result = self.conn.search(es_query,
                                        index=self.index_name,
                                        doc_type=doc_type,
                                        query_params=query_params)

            if aggs:
                results = query_result['aggregations']
                break
            else:
                scroll_id = query_result.get('_scroll_id')
                hits = query_result['hits']['hits']
                if len(hits) > 0:
                    # DELETE scroll
                    results.extend(hits)
                else:
                    break
            
        return results

    def aggregate(self, aggregations, query=None, doc_type='deal'):
        """
        Executes aggregation queries
        @return: The full list of hits.
        """

        es_query = {
            'aggregations': aggregations,
            'query': query,
            'size': 0,
        }
        raw_result = self.conn.search(es_query, index=self.index_name, doc_type=doc_type)
        result = {}
        for key in aggregations.keys():
            result[key] = raw_result['aggregations'][key]['buckets']
        return result

    def delete_activity(self, activity):
        for doc_type in DOC_TYPES_ACTIVITY:
            try:
                if doc_type == 'deal':
                    self.conn.delete(
                        id=activity.activity_identifier,
                        index=self.index_name,
                        doc_type=doc_type)
                else:
                    self.conn.delete_by_query(query={
                        "parent_id": {
                            "type": "deal",
                            "id": str(activity.activity_identifier),
                            }
                        },
                        index=self.index_name,
                        doc_type=doc_type)
            except ElasticHttpNotFoundError as e:
                pass

    def get_deals_by_activity_identifier(self, activity_identifier, doc_type='deal'):
        return self.search({"constant_score": {
            "filter": {
                "term": {
                    "activity_identifier": activity_identifier
                }
            }
        }})

# Init two connections
es_search = ElasticSearch()
es_save = ElasticSearch()
