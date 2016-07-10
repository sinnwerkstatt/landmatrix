from mapping.map_model import MapModel
import landmatrix.models
import old_editor.models
from migrate import V1, V2

from mapping.map_activity_attribute_group import MapActivityAttributeGroup

from django.db import transaction, connections

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


#class MapPublicInterfaceCache(MapModel):
#
#    old_class = old_editor.models.A_Key_Value_Lookup
#    new_class = landmatrix.models.PublicInterfaceCache
#    depends = [ MapActivityAttributeGroup ]
#
#    relevant_keys = ('pi_deal', 'deal_scope', 'pi_negotiation_status', 'pi_implementation_status', 'pi_deal_size')
#
#    @classmethod
#    @transaction.atomic(using=V2)
#    def map_all(cls, save=False, verbose=False):
#
#        cls._check_dependencies()
#        cls._start_timer()
#
#        activity_identifiers = cls.all_ids()
#        cls._count = len(activity_identifiers)
#        for index, activity_identifier in enumerate(activity_identifiers):
#            lookup_objects = old_editor.models.A_Key_Value_Lookup.objects.using(V1).\
#                filter(activity_identifier=activity_identifier).\
#                filter(key__in=cls.relevant_keys)
#            if lookup_objects:
#                tags = { lu.key: lu.value for lu in lookup_objects}
#                pi_cache = landmatrix.models.PublicInterfaceCache(
#                    fk_activity=get_activity_for_identifier(activity_identifier),
#                    is_public=tags.get('pi_deal', 'False') == 'True',
#                    deal_scope=tags.get('deal_scope', None),
#                    deal_size=int(tags.get('pi_deal_size', 0) or 0),
#                    implementation_status=tags.get('pi_implementation_status', None),
#                    negotiation_status=tags.get('pi_negotiation_status', None),
#
#                )
#                if save:
#                    pi_cache.save(using=V2)
#
#            cls._print_status({'id': pi_cache.pk}, index)
#
#        cls._done = True
#        cls._print_summary()
#
#    @classmethod
#    def all_records(cls):
#        ids = cls.all_ids()
#        cls._count = len(ids)
#        activities = []
#        for activity_identifier in ids:
#            activities.append(
#                MapPublicInterfaceCache.get_activity_for_identifier(activity_identifier)
#            )
#        return cls.old_class.objects.using(V1).filter(pk__in=ids).values()
#
#
#    @classmethod
#    def all_ids(cls):
#        cursor = connections[V1].cursor()
#        cursor.execute("""
#SELECT DISTINCT activity_identifier FROM a_key_value_lookup
#WHERE `key` IN %s
#ORDER BY activity_identifier
#        """ % str(cls.relevant_keys))
#        return [id[0] for id in cursor.fetchall()]
#
#
#def get_activity_for_identifier(activity_identifier):
#        return landmatrix.models.Activity.objects.using(V2).filter(activity_identifier=activity_identifier)[0]
#        # return landmatrix.models.Activity.objects.using(V2).filter(activity_identifier=activity_identifier).filter(version=_get_latest_version(activity_identifier))[0]
#
#def _get_latest_version(deal_id):
#    from django.db.models import Max
#    return landmatrix.models.Activity.objects.using(V2).filter(activity_identifier=deal_id).values().aggregate(Max('version'))['version__max']
#