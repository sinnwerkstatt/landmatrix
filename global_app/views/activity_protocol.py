from landmatrix.models.activity import Activity
from api.query_sets.activity_query_set import ActivityQuerySet

from django.http import HttpResponse
from django.contrib import messages
import json

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityProtocol:

    def dispatch(self, request, action):
        queryset = ActivityQuerySet(request.POST)
        res = queryset.all()
        output = json.dumps(res)

        # return HttpResponse(json.dumps(res,encoding="cp1251"), mimetype="application/json")#FIXME, utf-8 breaks for get-the-detail view
        return HttpResponse(output, content_type="application/json")

    def update_secondary_investors(self, activity, primary_investor, secondary_investor, request=None):
        # query all active involvements of primary investor
        involvements = Involvement.objects.filter(fk_primary_investor=primary_investor)
        involvements = involvements.exclude(fk_activity__fk_status__name__in=("pending", "to_delete", "deleted", "rejected"))
        involvements = involvements.exclude(fk_activity__activity_identifier=activity.activity_identifier)
        # select all efected activity identifier
        a_ids = set([i.fk_activity.activity_identifier for i in involvements])
        for a_id in a_ids:
            latest = Activity.objects._get_latest_active_activity(a_id)
            if latest:
                existing_involvements = set([i.fk_stakeholder.id for i in Involvement.objects.get_involvements_for_activity(latest)])
                for si in secondary_investor:
                    s = si["stakeholder"].id
                    if s not in existing_involvements:
                        # only create if not previously exists
                        involvement = Involvement.objects.create(
                            fk_activity=latest,
                            fk_stakeholder=si["stakeholder"],
                            fk_primary_investor=primary_investor,
                            investment_ratio=si["investment_ratio"] or 0,
                        )
                    else:
                        existing_involvements.remove(s)
                if len(existing_involvements):
                    # delete remaining
                    Involvement.objects.filter(fk_activity=latest, fk_stakeholder__in=existing_involvements).delete()
        if request:
            # add info message when request available
            if a_ids:
                links = ["<a target=\"_blank\" href=\"/browse/deal/%(id)s/\">#%(id)s</a>" % {"id": i} for i in a_ids]
                messages.info(request, "Updated secondary investors for deals: (%s)." % ",".join(links))
            skipped_a_ids = set(i.fk_activity.activity_identifier for i in Involvement.objects.filter(fk_primary_investor=primary_investor, fk_activity__fk_status__name="pending").exclude(fk_activity__activity_identifier=activity.activity_identifier))
            if skipped_a_ids:
                links = ["<a target=\"_blank\" href=\"/browse/deal/%(id)s/\">#%(id)s</a>" % {"id": i} for i in skipped_a_ids]
                messages.info(request, "Skipped update of secondary investors for pending deals: (%s)." % ",".join(links))

    def fill_lookup_table(self, activity_identifier):
        # delete old rows
        a_id = Activity.objects._get_latest_activity(activity_identifier).id
        self.remove_from_lookup_table(activity_identifier)
        tags = A_Tag.objects.filter(fk_a_tag_group__fk_activity=a_id)
        for t in tags:
            group = t.fk_a_tag_group.fk_a_tag.fk_a_value.value
            value = t.fk_a_value.value
            key = t.fk_a_key.key
            if value:
                if key == "crops":
                    value = Crop.objects.get(name=value).id
                elif key == "target_country":
                    value = Country.objects.get(name=value).id
            A_Key_Value_Lookup.objects.create(
                activity_identifier=activity_identifier,
                key=key,
                key_id=t.fk_a_key.id,
                value=value,
                year=t.fk_a_value.year,
                group=group
            )

    """
        Store values for public interface.
        Depends on activity and stakeholder lookup tables.
    """
    def prepare_deal_for_public_interface(self, activity_identifier):
        # order of execution is important, is_public_deal relies on calculated deal size
        self.calculate_public_interface_values(activity_identifier)
        is_public_deal = self.is_public_deal(activity_identifier)
        # delete old rows
        A_Key_Value_Lookup.objects.filter(activity_identifier=activity_identifier, key="pi_deal").delete()
        A_Key_Value_Lookup.objects.create(
            activity_identifier=activity_identifier,
            key="pi_deal",
            key_id=None,
            value=is_public_deal,
            year=None,
        )

    def remove_from_lookup_table(self, activity_identifier):
        A_Key_Value_Lookup.objects.filter(activity_identifier=activity_identifier).delete()
