# TODO: Move out of views
import re
import json
from django.http import HttpResponse
from django.contrib import messages
from django.utils.datastructures import SortedDict

from grid.forms.deal_general_form import DealGeneralForm
from api.query_sets.activity_query_set import ActivityQuerySet
from landmatrix.models.activity import Activity
from landmatrix.models.activity_attribute_group import ActivityAttribute
from landmatrix.models.investor import InvestorActivityInvolvement, InvestorVentureInvolvement
from grid.views.profiling_decorators import print_execution_time_and_num_queries

# FIXME: Most of this has been split into HistoricalActivity model and ActivityQuerySet. Is this layer still necessary?
class ActivityProtocol:
    @print_execution_time_and_num_queries
    def dispatch(self, request, action):
        queryset = ActivityQuerySet(request)
        res = queryset.all()
        output = json.dumps(res)

        return HttpResponse(output, content_type="application/json")

    #def update_secondary_investors(self, activity, operational_stakeholder, involvement_stakeholders, request=None):
    #    activity_identifiers = self._affected_activity_identifiers(activity, operational_stakeholder)
#
    #    for activity_identifier in activity_identifiers:
    #        self._update_stakeholders_for_activity(activity_identifier, involvement_stakeholders, operational_stakeholder)

        #if request:
        #    _add_info_message(activity, activity_identifiers, operational_stakeholder, request)
        
    #def remove_from_lookup_table(self, activity_identifier):
    #    Activity.objects.filter(activity_identifier=activity_identifier).delete()


    #def attributes_sorted_by_date(activity_identifier, attribute):
    #    return self.attributes_for_activity(activity_identifier, attribute).order_by("-date")
    #
    #
    #def attributes_without_date(activity_identifier, attribute):
    #    return self.attributes_for_activity(activity_identifier, attribute).filter(date__isnull=True)

    #def latest_attribute_value_for_activity(activity_identifier, attribute):
    #        attributes = self.nonnull_attributes_for_activity(activity_identifier, attribute).order_by("-date")
    #        return len(attributes) > 0 and attributes[0].attributes[attribute] or None

    #def _affected_activity_identifiers(self, activity, operational_stakeholder):
    #    involvements = InvestorActivityInvolvement.objects.filter(fk_investor=operational_stakeholder). \
    #        exclude(fk_activity__fk_status__name__in=("pending", "to_delete", "deleted", "rejected")). \
    #        exclude(fk_activity__activity_identifier=activity.activity_identifier)
    #    return set([i.fk_activity.activity_identifier for i in involvements])


    #def _add_info_message(self, activity, activity_identifiers, operational_stakeholder, request):
        #if activity_identifiers:
        #    links = [
        #        "<a target=\"_blank\" href=\"/browse/deal/%(id)s/\">#%(id)s</a>" % {"id": i}
        #        for i in activity_identifiers
        #    ]
        #    messages.info(request, "Updated secondary investors for deals: (%s)." % ",".join(links))
    #
        #skipped = self._skipped_activity_identifiers(activity, operational_stakeholder)
        #if skipped:
        #    links = [
        #        "<a target=\"_blank\" href=\"/browse/deal/%(id)s/\">#%(id)s</a>" % {"id": i}
        #        for i in skipped
        #    ]
        #    messages.info(request, "Skipped update of secondary investors for pending deals: (%s)." % ",".join(links))


    #def _skipped_activity_identifiers(self, activity, operational_stakeholder):
    #    return {
    #        i.fk_activity.activity_identifier
    #        for i in InvestorActivityInvolvement.objects.filter(fk_investor=operational_stakeholder).
    #            filter(fk_activity__fk_status__name="pending").
    #            exclude(fk_activity__activity_identifier=activity.activity_identifier)
    #        }


    #def _update_stakeholders_for_activity(self, activity_identifier, involvement_stakeholders, operational_stakeholder):
#
    #    latest = Activity.get_latest_active_activity(activity_identifier)
    #    if not latest:
    #        return
#
    #    existing_investors = {
    #        i.fk_investor.id for i in InvestorActivityInvolvement.objects.get_involvements_for_activity(latest.activity_identifier)
    #    }
#
    #    for involved_stakeholder in involvement_stakeholders:
    #        if involved_stakeholder["stakeholder"].id not in existing_investors:
    #            InvestorVentureInvolvement.objects.create(
    #                fk_venture=operational_stakeholder,
    #                fk_investor=involved_stakeholder["stakeholder"],
    #                investment_ratio=involved_stakeholder["investment_ratio"] or 0,
    #            )
    #        else:
    #            existing_investors.remove(involved_stakeholder["stakeholder"].id)
#
    #    if len(existing_investors):
    #        InvestorVentureInvolvement.objects.filter(fk_venture=operational_stakeholder). \
    #            filter(fk_investor__in=existing_investors).delete()
