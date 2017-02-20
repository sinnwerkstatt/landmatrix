from pyelasticsearch import ElasticSearch as PyElasticSearch
from pyelasticsearch.exceptions import ElasticHttpNotFoundError, ElasticHttpError
import http.client
http.client._MAXHEADERS = 1000
from django.conf import settings

from grid.views.change_deal_view import ChangeDealView



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
        properties = {'geo_point': {'type': 'geo_point'}}
        for form in ChangeDealView.FORMS:
            form = hasattr(form, "form") and form.form or form
            for name, field in form.base_fields.items():
                # Title field?
                if name.startswith('tg_') and not name.endswith('_comment'):
                    continue
                properties[name] = {'type': FIELD_TYPE_MAPPING.get(field.__class__.__name__, 'string')}
        return properties

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
            doc = {'id': activity.activity_identifier}
            doc.update(dict([a.name, a.value] for a in activity.attributes.all()))
            if 'point_lat' in doc and 'point_lon' in doc:
                doc['geo_point'] = '%s,%s' % (doc.get('point_lat', None), doc.get('point_lon', None))
            docs.append(doc)
        self.conn.bulk((self.conn.index_op(doc, id=doc.pop('id')) for doc in docs),
            index='landmatrix',
            doc_type='deal')

    def index_document(self, activity):
        doc = {'id': activity.activity_identifier}
        doc.update(dict([a.name, a.value] for a in activity.attributes.all()))
        if 'point_lat' in doc and 'point_lon' in doc:
            doc['geo_point'] = '%s,%s' % (doc.get('point_lat', None), doc.get('point_lon', None))
        self.conn.index(index='landmatrix', doc_type='deal', doc=doc, id=doc.pop('id'))

    def refresh_index(self):
        self.conn.refresh('landmatrix')