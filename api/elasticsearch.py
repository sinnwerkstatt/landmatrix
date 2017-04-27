import json

from pyelasticsearch import ElasticSearch as PyElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError
import http.client
http.client._MAXHEADERS = 1000
from django.conf import settings

from grid.views.change_deal_view import ChangeDealView
from grid.forms.deal_spatial_form import DealSpatialForm


from landmatrix.models.activity import HistoricalActivity


FIELD_TYPE_MAPPING = {
    'IntegerField': 'integer',
    'CharField': 'string', # use 'exact_value' instead of string??
    'AreaField': 'geo_shape',
    'FloatField': 'float',
}


_landmatrix_properties = None
def get_elasticsearch_properties():
    """ Generates a list of elasticsearch document properties from all filter fields in the
        Deal attribute model Forms """
    global _landmatrix_properties
    
    if _landmatrix_properties is None:
        # Get field type mappings
        _landmatrix_properties = {
            'id': {'type': 'string'}, # use 'exact_value' instead of string??
            'historical_activity_id': {'type': 'integer'},
            'activity_identifier': {'type': 'integer'},
            'geo_point': {'type': 'geo_point'},
            'status': {'type': 'integer'}, 
        }
        for form in ChangeDealView.FORMS:
            form = hasattr(form, "form") and form.form or form
            for name, field in form.base_fields.items():
                # Title field?
                if name.startswith('tg_') and not name.endswith('_comment'):
                    continue
                _landmatrix_properties[name] = {'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')}
    #print(str(_landmatrix_properties))
    return _landmatrix_properties


class ElasticSearch(object):
    conn = None
    url = settings.ELASTICSEARCH_URL
    index_name = settings.ELASTICSEARCH_INDEX_NAME
    

    def __init__(self, index_name=None):
        self.conn = PyElasticSearch()
        if index_name:
            self.index_name = index_name

    def get_spatial_properties(self):
        return DealSpatialForm.base_fields.keys()

    def create_index(self, delete=True):
        if delete:
            try:
                self.conn.delete_index(self.index_name)
            except ElasticHttpNotFoundError as e:
                pass 
        deal_mapping = {
            'deal': {
                'properties': get_elasticsearch_properties()
            }
        }
        self.conn.create_index(self.index_name, settings={'mappings': deal_mapping})
    """
    def index_documents(self, queryset):
        docs = []
        for activity in queryset:
            for doc in self.get_documents(activity):
                docs.append(doc)
<<<<<<< HEAD
        self.conn.bulk(
            (self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
            index='landmatrix',
=======
        self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
            index=self.index_name,
>>>>>>> merge-map-refactor
            doc_type='deal')
    """
    def index_document_by_id(self, activity_id):
        activity = HistoricalActivity.objects.get(pk=activity_id)
        return self.index_document(activity)

    def index_document(self, activity):
        for doc in self.get_documents(activity):
            self.conn.index(index=self.index_name, doc_type='deal', doc=doc, id=doc.pop('id'))
    
    def index_documents_by_version(self, activity_identifiers=[], drop_index=True):
        activity_identifiers = activity_identifiers or HistoricalActivity.objects.filter(fk_status__in=(
                HistoricalActivity.STATUS_ACTIVE, HistoricalActivity.STATUS_PENDING, 
                HistoricalActivity.STATUS_OVERWRITTEN, HistoricalActivity.STATUS_DELETED
            )).distinct().values_list('activity_identifier', flat=True).distinct()
        docs = []
        print('>> Collecting documents for', len(activity_identifiers), 'deal entries...')
        for activity_identifier in activity_identifiers:
            for doc in self.get_documents_for_activity_version(activity_identifier):
                docs.append(doc)
        
        if drop_index:
            print ('>> Dropping index...')
            self.create_index()
        
        print('>> Indexing', len(docs), 'documents...')
        self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
            index=self.index_name,
            doc_type='deal')
    
    def index_document_by_version(self, activity_identifier):
        for doc in self.get_documents_for_activity_version(activity_identifier):
            self.conn.index(index=self.index_name, doc_type='deal', doc=doc, id=doc.pop('id'))
    
    def get_documents_for_activity_version(self, activity_identifier):
        docs = []
        #print('>>> for act', activity_identifier)
        # get the newes non-pending, readable historic version:
        try:
            newest = HistoricalActivity.objects.filter(activity_identifier=activity_identifier, fk_status__in=(
                HistoricalActivity.STATUS_ACTIVE, HistoricalActivity.STATUS_OVERWRITTEN, HistoricalActivity.STATUS_DELETED)).distinct().latest()
            #print('           newest', newest.activity_identifier, newest.fk_status_id, newest.id)
            docs.extend(self.get_documents(newest))
        except HistoricalActivity.DoesNotExist:
            newest = None
            
        # get all pendings
        pendings = HistoricalActivity.objects.filter(activity_identifier=activity_identifier, fk_status_id=HistoricalActivity.STATUS_PENDING).distinct()
        for pending in pendings:
            #print('           pending', pending.activity_identifier, pending.fk_status_id, pending.id)
            docs.extend(self.get_documents(pending))
        
        return docs
    
    def get_documents(self, activity):
        docs = []
        spatial_names = self.get_spatial_properties()
        spatial_attrs = {}
        attrs = {
            'historical_activity_id': activity.id,
            'activity_identifier': activity.activity_identifier,
            'status': activity.fk_status_id,
        }
        # FIXME: Only use current values? .filter(is_current=True)
        for a in activity.attributes.all():
            # do not include the django object id
            if a.name == 'id': 
                continue

            value = a.value
            if a.name and 'area' in a.name and a.polygon is not None:
                value = json.loads(a.polygon.json)

                # Apparently this is case sensitive: MultiPolygon as provided by
                # the GeoJSON does not work ...
                value['type'] = 'multipolygon'

            # TODO: are polygons used at all for searching?

            # do not include empty values
            if value is None or value == '':
                continue
            
            if a.name in spatial_names:
                if a.fk_group_id in spatial_attrs:
                    spatial_attrs[a.fk_group_id][a.name] = value
                else:
                    spatial_attrs[a.fk_group_id] = {a.name: value}
            elif a.name in attrs:
                attrs[a.name].append(value)
            else:
                attrs[a.name] = [value,]
              
        for group, group_attrs in spatial_attrs.items():
            doc = attrs.copy()
            doc.update(group_attrs)
            # Set unique ID for location (deals can have multiple locations)
            doc['id'] = '%s_%s' % (doc['historical_activity_id'], group)
            if 'point_lat' in group_attrs and 'point_lon' in group_attrs:
                doc['geo_point'] = '%s,%s' % (group_attrs.get('point_lat'), group_attrs.get('point_lon'))
            # FIXME: we dont really need 'point_lat' and 'point_lon' here, so we should pop them from doc when adding 'geo_point'
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
        
        print('\n>> Elasticsearch returned', len(raw_result_list), 'documents from a total of', query_result['hits']['total'], '\n\n')
        
        return raw_result_list

# Init two connections
es_search = ElasticSearch()
es_save = ElasticSearch()
