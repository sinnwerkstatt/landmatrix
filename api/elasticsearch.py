from pyelasticsearch import ElasticSearch as PyElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError, ElasticHttpError
import http.client
http.client._MAXHEADERS = 1000
from django.conf import settings
from django.utils.datastructures import MultiValueDict

from grid.views.change_deal_view import ChangeDealView
from grid.forms.deal_spatial_form import DealSpatialForm


FIELD_TYPE_MAPPING = {
    'IntegerField': 'integer',
    'CharField': 'string', # use 'exact_value' instead of string??
    'AreaField': 'geo_shape',
}

class ElasticSearch(object):
    conn = None
    url = settings.ELASTICSEARCH_URL
    index_name = None
    

    def __init__(self, index_name='landmatrix'):
        self.conn = PyElasticSearch()
        self.index_name = index_name

    def get_properties(self):
        # Get field type mappings
        properties = {
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
                properties[name] = {'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')}
        print(str(properties))
        return properties

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
                'properties': self.get_properties()
            }
        }
        self.conn.create_index(self.index_name, settings={'mappings': deal_mapping})

    def index_documents(self, queryset):
        docs = []
        for activity in queryset:
            for doc in self.get_documents(activity):
                docs.append(doc)
        self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
            index=self.index_name,
            doc_type='deal')

    def index_document(self, activity):
        for doc in self.get_documents(activity):
            self.conn.index(index=self.index_name, doc_type='deal', doc=doc, id=doc.pop('id'))

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
            value = 'area' in a.name if a.polygon else a.value
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
        
    def search(self, query):
        return self.conn.search(query, index=self.index_name)

# Init two connections
es_search = ElasticSearch()
es_save = ElasticSearch()
