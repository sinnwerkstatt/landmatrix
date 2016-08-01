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


__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityProtocol:
    @print_execution_time_and_num_queries
    def dispatch(self, request, action):
        queryset = ActivityQuerySet(request)
        res = queryset.all()
        output = json.dumps(res)

        return HttpResponse(output, content_type="application/json")

    def update_secondary_investors(self, activity, operational_stakeholder, involvement_stakeholders, request=None):
        activity_identifiers = self._affected_activity_identifiers(activity, operational_stakeholder)

        for activity_identifier in activity_identifiers:
            self._update_stakeholders_for_activity(activity_identifier, involvement_stakeholders, operational_stakeholder)

        #if request:
        #    _add_info_message(activity, activity_identifiers, operational_stakeholder, request)

    def prepare_deal_for_public_interface(self, activity_identifier):
        # order of execution is important, is_public_deal relies on calculated deal size
        pi_values = self.calculate_public_interface_values(activity_identifier)

        activity = Activity.get_latest_activity(activity_identifier)
        activity.is_public = self.is_public_deal(activity_identifier)
        activity.deal_scope = pi_values.get('deal_scope', None)
        activity.negotiation_status = pi_values.get('negotiation_status', None)
        activity.implementation_status = pi_values.get('implementation_status', None)
        activity.deal_size = pi_values.get('deal_size', None)
        activity.save()
        
    def remove_from_lookup_table(self, activity_identifier):
        Activity.objects.filter(activity_identifier=activity_identifier).delete()

    def calculate_public_interface_values(self, activity_identifier):
        pi_values = {}
        # Implementation status (Latest date entered for the deal, then highest id)
        # Null dates go last
        attributes = self.attributes_for_activity(
            activity_identifier, 'implementation_status')
        attributes = attributes.extra(select={'date_is_null': 'date IS NULL'})
        attributes = attributes.extra(
            order_by=['date_is_null', '-date', '-id'])

        if attributes.count() > 0:
            pi_values['implementation_status'] = attributes.first().value
        else:
            pi_values['implementation_status'] = None
        # Negotiation status (Latest date entered for the deal, then highest id)
        # Null dates go last
        attributes = self.attributes_for_activity(
            activity_identifier, 'negotiation_status')
        attributes = attributes.extra(select={'date_is_null': 'date IS NULL'})
        attributes = attributes.extra(
            order_by=['date_is_null', '-date', '-id'])

        if attributes.count() > 0:
            pi_values['negotiation_status'] = attributes.first().value
        else:
            pi_values['negotiation_status'] = None
        # Deal size
        if pi_values['negotiation_status']:
            pi_values['deal_size'] = self._calculate_deal_size(
                activity_identifier, pi_values['negotiation_status']
            )

        # Deal scope (domestic or transnational)
        pi_values['deal_scope'] = self._calculate_deal_scope(activity_identifier)

        return pi_values

    def attributes_for_activity(self, activity_identifier, attribute):
        return ActivityAttribute.objects. \
            filter(fk_activity__activity_identifier=activity_identifier, name=attribute)

    def is_public_deal(self, activity_identifier):
        """
            Important: relies on calculate_public_interface_values result, calculate_public_interface_values should always be executed first.
        """
        activity = Activity.get_latest_active_activity(activity_identifier)
        if not activity:
            return False

        #if _is_public_older_y2k(activity_identifier):
        #    return False

        if not self._is_flag_not_public_off(activity_identifier):
            return False

        #if _is_size_invalid(activity_identifier):
        #    return False

        if not self._is_minimum_information_requirement_satisfied(activity_identifier):
            return False

        involvements = InvestorActivityInvolvement.objects.get_involvements_for_activity(activity.id)

        #if not _has_subinvestors(involvements):
        #    return False

        if not self._has_valid_investors(involvements):
            return False

        #if _is_mining_deal(activity_identifier):
        #    return False

        #if _is_high_income_target_country(activity_identifier):
        #    return False

        return True

    #def _is_high_income_target_country(activity_identifier):
    #        for tc in self.attributes_for_activity(activity_identifier, "target_country"):
    #            country = Country.objects.get(id=tc.value)
    #            if country.high_income:
    #                return True
    #        return False


    #def _is_mining_deal(activity_identifier):
    #    mining = A_Key_Value_Lookup.objects.filter(activity_identifier=activity_identifier, key="intention",
    #                                               value="Mining")
    #    intentions = A_Key_Value_Lookup.objects.filter(activity_identifier=activity_identifier, key="intention")
    #    is_mining_deal = len(mining) > 0 and len(intentions) == 1
    #    return is_mining_deal


    def _has_valid_investors(self, involvements):
        for i in involvements:
            if not i.fk_investor:
                continue
            investor_name = i.fk_investor.name
            invalid_name = "^(unknown|unnamed)( \(([, ]*(unnamed investor [0-9]+)*)+\))?$"
            if investor_name and not re.match(invalid_name, investor_name.lower()):
                return True
        return False


    #def _has_subinvestors(involvements):
    #        if len(involvements) == 1 and not involvements[0].subinvestors.exists():
    #            return False
    #
    #        return len(involvements) > 0


    def _is_minimum_information_requirement_satisfied(self, activity_identifier):
        target_country = self.attributes_for_activity(activity_identifier, "target_country")
        ds_type = self.attributes_for_activity(activity_identifier, "type")
        return len(target_country) > 0 and len(ds_type) > 0


    #def _is_size_invalid(activity_identifier):
    #    intended_size = latest_attribute_value_for_activity(activity_identifier, "intended_size") or 0
    #    contract_size = latest_attribute_value_for_activity(activity_identifier, "contract_size") or 0
    #    production_size = latest_attribute_value_for_activity(activity_identifier, "production_size") or 0
    #    # Filter B2 (area size >= 200ha AND at least one area size is given)
    #    no_size_set = (not intended_size and not contract_size and not production_size)
    #    size_too_small = int(intended_size) < MIN_DEAL_SIZE and int(contract_size) < MIN_DEAL_SIZE and int(production_size) < MIN_DEAL_SIZE
    #    return no_size_set or size_too_small


    def _is_flag_not_public_off(self, activity_identifier):
        # Filter B1 (flag is unreliable not set):
        not_public = self.attributes_for_activity(activity_identifier, "not_public")
        not_public = len(not_public) > 0 and not_public[0].value or None
        return (not not_public) or (not_public in ("False", "off"))


    #def _is_public_older_y2k(activity_identifier):
    #    """
    #    Filter B3
    #    Only drop a deal if we have information that initiation years are < 2000.
    #    Deals with missing year values have to cross the filter to the PI
    #    """
    #    negotiation_stati = self.attributes_for_activity(activity_identifier, "negotiation_status"). \
    #        filter(attributes__contains={
    #                'negotiation_status': [
    #                    "Expression of interest", "Under negotiation", "Oral Agreement",
    #                    "Memorandum of understanding", "Contract signed"
    #                ]
    #            }
    #        ). \
    #        filter(date__lt='2000-01-01')
    #
    #    implementation_stati = self.attributes_for_activity(activity_identifier, "implementation_status"). \
    #        filter(attributes__contains={
    #            'implementation_status': ["Startup phase (no production)", "In operation (production)"]}
    #        ). \
    #        filter(date__lt='2000-01-01')
    #    return len(negotiation_stati) > 0 or len(implementation_stati) > 0


    def _calculate_deal_scope(self, activity_identifier):
        activity = Activity.get_latest_active_activity(activity_identifier)
        # activity could be pending, needs to check
        if not activity:
            return None

        involvements = InvestorActivityInvolvement.objects.get_involvements_for_activity(activity.id)
        target_countries = {c.value for c in self.attributes_for_activity(activity_identifier, "target_country")}
        investor_countries = {i.fk_investor.fk_country for i in involvements}

        if len(target_countries) > 0 and len(investor_countries) > 0:
            if len(target_countries.symmetric_difference(investor_countries)) == 0:
                return "domestic"
            else:
                return "transnational"
        elif len(target_countries) > 0 and len(investor_countries) == 0:
            # treat deals without investor country as transnational
            return "transnational"
        else:
            return None

    def _calculate_deal_size(self, activity_identifier, negotiation_status):
        intended_size = self.nonnull_attributes_for_activity(activity_identifier, "intended_size").order_by("-date")
        intended_size = len(intended_size) > 0 and intended_size[0].value or None
        contract_size = self.nonnull_attributes_for_activity(activity_identifier, "contract_size").order_by("-date")
        contract_size = len(contract_size) > 0 and contract_size[0].value or None
        production_size = self.nonnull_attributes_for_activity(activity_identifier, "production_size").order_by("-date")
        production_size = len(production_size) > 0 and production_size[0].value or None
        if negotiation_status in ("Expression of interest", "Under negotiation", "Memorandum of understanding"):
            # intended deal
            if not intended_size and contract_size:
                intended_size = contract_size
            elif not intended_size and not contract_size and production_size:
                intended_size = production_size
            return intended_size
        elif negotiation_status in ("Oral Agreement", "Contract signed"):
            # concluded deal
            if not contract_size and production_size:
                contract_size = production_size
            return contract_size
        elif negotiation_status == "Negotiations failed":
            # intended but failed deal
            if not intended_size and contract_size:
                intended_size = contract_size
            elif not intended_size and not contract_size and production_size:
                intended_size = production_size
            return intended_size
        elif negotiation_status == "Contract canceled":
            # concluded but failed
            if not contract_size and production_size:
                contract_size = production_size
            return contract_size

    #def attributes_sorted_by_date(activity_identifier, attribute):
    #    return self.attributes_for_activity(activity_identifier, attribute).order_by("-date")
    #
    #
    #def attributes_without_date(activity_identifier, attribute):
    #    return self.attributes_for_activity(activity_identifier, attribute).filter(date__isnull=True)

    #def latest_attribute_value_for_activity(activity_identifier, attribute):
    #        attributes = self.nonnull_attributes_for_activity(activity_identifier, attribute).order_by("-date")
    #        return len(attributes) > 0 and attributes[0].attributes[attribute] or None


    def nonnull_attributes_for_activity(self, activity_identifier, attribute):
        # TODO: This is deprecated, since there shouldn't be any attributes without values anymore
        return self.attributes_for_activity(activity_identifier, attribute).filter(value__isnull=False)


    def _affected_activity_identifiers(self, activity, operational_stakeholder):
        involvements = InvestorActivityInvolvement.objects.filter(fk_investor=operational_stakeholder). \
            exclude(fk_activity__fk_status__name__in=("pending", "to_delete", "deleted", "rejected")). \
            exclude(fk_activity__activity_identifier=activity.activity_identifier)
        return set([i.fk_activity.activity_identifier for i in involvements])


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


    def _skipped_activity_identifiers(self, activity, operational_stakeholder):
        return {
            i.fk_activity.activity_identifier
            for i in InvestorActivityInvolvement.objects.filter(fk_investor=operational_stakeholder).
                filter(fk_activity__fk_status__name="pending").
                exclude(fk_activity__activity_identifier=activity.activity_identifier)
            }


    def _update_stakeholders_for_activity(self, activity_identifier, involvement_stakeholders, operational_stakeholder):

        latest = Activity.get_latest_active_activity(activity_identifier)
        if not latest:
            return

        existing_investors = {
            i.fk_investor.id for i in InvestorActivityInvolvement.objects.get_involvements_for_activity(latest.id)
        }

        for involved_stakeholder in involvement_stakeholders:
            if involved_stakeholder["stakeholder"].id not in existing_investors:
                InvestorVentureInvolvement.objects.create(
                    fk_venture=operational_stakeholder,
                    fk_investor=involved_stakeholder["stakeholder"],
                    investment_ratio=involved_stakeholder["investment_ratio"] or 0,
                )
            else:
                existing_investors.remove(involved_stakeholder["stakeholder"].id)

        if len(existing_investors):
            InvestorVentureInvolvement.objects.filter(fk_venture=operational_stakeholder). \
                filter(fk_investor__in=existing_investors).delete()
