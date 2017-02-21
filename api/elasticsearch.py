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
    'CharField': 'string',
    'AreaField': 'geo_shape',
}

class ElasticSearch(object):
    conn = None
    url = settings.ELASTICSEARCH_URL

    def __init__(self):
        self.conn = PyElasticSearch()

    def get_properties(self):
        # Get field type mappings
        properties = {
            'id': {'type': 'integer'},
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
                self.conn.delete_index('landmatrix')
            except ElasticHttpNotFoundError as e:
                pass 
        deal_mapping = {
            'deal': {
                'properties': self.get_properties()
            }
        }
        self.conn.create_index('landmatrix', settings={'mappings': deal_mapping})

    def index_documents(self, queryset):
        docs = []
        for activity in queryset:
            for doc in self.get_documents(activity):
                docs.append(doc)
        self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
            index='landmatrix',
            doc_type='deal')

    def index_document(self, activity):
        for doc in self.get_documents(activity):
            self.conn.index(index='landmatrix', doc_type='deal', doc=doc, id=doc.pop('id'))

    def get_documents(self, activity):
        docs = []
        spatial_names = self.get_spatial_properties()
        spatial_attrs = {}
        attrs = {
            'id': activity.id,
            'activity_identifier': activity.activity_identifier,
            'status': activity.fk_status_id,
        }
        # FIXME: Only use current values? .filter(is_current=True)
        for a in activity.attributes.all():
            if a.name == 'id': 
+                continue
            value = 'area' in a.name if a.polygon else a.value
            if a.name in spatial_names:
                if a.fk_group.name in spatial_attrs:
                    spatial_attrs[a.fk_group.name][a.name] = value
                else:
                    spatial_attrs[a.fk_group.name] = {a.name: value}
            elif a.name in attrs:
                attrs[a.name].append(value)
            else:
                attrs[a.name] = [value,]
        for group, group_attrs in spatial_attrs.items():
            doc = attrs.copy()
            doc.update(group_attrs)
            if 'point_lat' in group_attrs and 'point_lon' in group_attrs:
                doc['geo_point'] = '%s,%s' % (group_attrs.get('point_lat'), group_attrs.get('point_lon'))
            docs.append(doc)
        return docs

    def refresh_index(self):
        self.conn.refresh('landmatrix')

# Init two connections
es_search = ElasticSearch()
es_save = ElasticSearch()