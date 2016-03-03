from grid.forms.add_deal_general_form import AddDealGeneralForm
from landmatrix.models.activity import Activity
from api.query_sets.activity_query_set import ActivityQuerySet

from django.http import HttpResponse
from django.contrib import messages
import json

from landmatrix.models.activity_attribute_group import ActivityAttributeGroup
from landmatrix.models.investor import InvestorActivityInvolvement, InvestorVentureInvolvement
from landmatrix.models.public_interface_cache import PublicInterfaceCache

from grid.views.profiling_decorators import print_execution_time_and_num_queries

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class ActivityProtocol:

    @print_execution_time_and_num_queries
    def dispatch(self, request, action):
        queryset = ActivityQuerySet(request.POST)
        res = queryset.all()
        output = json.dumps(res)

        return HttpResponse(output, content_type="application/json")

    def update_secondary_investors(self, activity, operational_stakeholder, involvement_stakeholders, request=None):
        activity_identifiers = _affected_activity_identifiers(activity, operational_stakeholder)

        for activity_identifier in activity_identifiers:
            _update_stakeholders_for_activity(activity_identifier, involvement_stakeholders, operational_stakeholder)

        if request:
            _add_info_message(activity, activity_identifiers, operational_stakeholder, request)

    def prepare_deal_for_public_interface(self, activity_identifier):
        # order of execution is important, is_public_deal relies on calculated deal size
        pi_values = self.calculate_public_interface_values(activity_identifier)

        PublicInterfaceCache.objects.filter(fk_activity__activity_identifier=activity_identifier).delete()
        PublicInterfaceCache.objects.create(
            fk_activity=Activity.get_latest_activity(activity_identifier),
            is_deal=is_public_deal(activity_identifier),
            negotiation_status=pi_values['negotiation_status'].attributes['negotiation_status'],
            implementation_status=pi_values['implementation_status'].attributes['implementation_status'],
            deal_size=pi_values['deal_size']
        )

    def remove_from_lookup_table(self, activity_identifier):
        PublicInterfaceCache.objects.filter(fk_activity__activity_identifier=activity_identifier).delete()

    NEGOTIATION_STATUS_ORDER = dict([(str(c[1]), c[0]) for c in AddDealGeneralForm().fields["negotiation_status"].choices])
    IMPLEMENTATION_STATUS_ORDER = dict([(str(c[1]), c[0]) for c in AddDealGeneralForm().fields["implementation_status"].choices])

    def calculate_public_interface_values(self, activity_identifier):
        pi_values = {
            'implementation_status': _most_current_state(
                activity_identifier, 'implementation_status', self.IMPLEMENTATION_STATUS_ORDER
            ),
            'negotiation_status': _most_current_state(
                activity_identifier, 'negotiation_status', self.NEGOTIATION_STATUS_ORDER
            )
        }

        if pi_values['negotiation_status']:
            pi_values['deal_size'] = _calculate_deal_size(
                activity_identifier, pi_values['negotiation_status'].attributes['negotiation_status']
            )

        # check if deal is domestic or transnational
        pi_values['deal_scope'] = _calculate_deal_scope(activity_identifier)

        return pi_values


def is_public_deal(activity_identifier):
    """
        Important: relies on calculate_public_interface_values result, calculate_public_interface_values should always be executed first.
    """
    activity = Activity.get_latest_active_activity(activity_identifier)
    if not activity:
        return False

    if _is_deal_older_y2k(activity_identifier):
        return False

    if not _is_flag_not_public_off(activity_identifier):
        return False

    if _is_size_invalid(activity_identifier):
        return False

    if not _is_minimum_information_requirement_satisfied(activity_identifier):
        return False

    involvements = InvestorActivityInvolvement.objects.get_involvements_for_activity(activity)

    if not _has_subinvestors(involvements):
        return False

    if not _has_valid_investors(involvements):
        return False

    if _is_mining_deal(activity_identifier):
        return False

    if _is_high_income_target_country(activity_identifier):
        return False

    return True


def _most_current_state(activity_identifier, attribute, order):
    states_without_year = attributes_without_date(activity_identifier, attribute)
    states_sorted_by_year = attributes_sorted_by_date(activity_identifier, attribute)
    return get_most_current_state(states_without_year, states_sorted_by_year, order, attribute)


def _is_high_income_target_country(activity_identifier):
        for tc in attributes_for_activity(activity_identifier, "target_country"):
            country = Country.objects.get(id=tc.value)
            if country.high_income:
                return True
        return False


def _is_mining_deal(activity_identifier):
    mining = A_Key_Value_Lookup.objects.filter(activity_identifier=activity_identifier, key="intention",
                                               value="Mining")
    intentions = A_Key_Value_Lookup.objects.filter(activity_identifier=activity_identifier, key="intention")
    is_mining_deal = len(mining) > 0 and len(intentions) == 1
    return is_mining_deal


def _has_valid_investors(involvements):
    has_investor = False
    for i in involvements:
        if not i.fk_stakeholder:
            continue
        investor = SH_Key_Value_Lookup.objects.filter(
            stakeholder_identifier=i.fk_stakeholder.stakeholder_identifier, key="investor_name")
        if len(investor) > 0:
            investor_name = investor[0].value
            if investor_name and ("Unnamed" not in investor_name and "Unknown" not in investor_name):
                has_investor = True
    primary_investor_name = involvements[0].fk_primary_investor.name or ""
    # filter Unknown (Unnamed Investor, Unnamed Investor 32)
    invalid_primary_investor_name = re.match("^(unknown|unnamed)( \(([, ]*(unnamed investor [0-9]+)*)+\))?$",
                                             primary_investor_name.lower())
    return has_investor or (primary_investor_name and not invalid_primary_investor_name)


def _has_subinvestors(involvements):
        if len(involvements) == 1 and not involvements[0].get_subinvestors():
            return False

        return len(involvements) > 0


def _is_minimum_information_requirement_satisfied(activity_identifier):
    target_country = attributes_for_activity(activity_identifier, "target_country")
    ds_type = attributes_for_activity(activity_identifier, "type")
    return len(target_country) > 0 and len(ds_type) > 0


def _is_size_invalid(activity_identifier):
    intended_size = latest_attribute_value_for_activity(activity_identifier, "intended_size") or 0
    contract_size = latest_attribute_value_for_activity(activity_identifier, "contract_size") or 0
    production_size = latest_attribute_value_for_activity(activity_identifier, "production_size") or 0
    # Filter B2 (area size >= 200ha AND at least one area size is given)
    no_size_set = (not intended_size and not contract_size and not production_size)
    size_too_small = int(intended_size) < 200 and int(contract_size) < 200 and int(production_size) < 200
    return no_size_set or size_too_small


def _is_flag_not_public_off(activity_identifier):
    # Filter B1 (flag is unreliable not set):
    not_public = attributes_for_activity(activity_identifier, "not_public")
    not_public = len(not_public) > 0 and not_public[0].attributes['not_public'] or None
    return (not not_public) or (not_public in ("False", "off"))


def _is_deal_older_y2k(activity_identifier):
    """
    Filter B3
    Only drop a deal if we have information that initiation years are < 2000.
    Deals with missing year values have to cross the filter to the PI
    """
    negotiation_stati = attributes_for_activity(activity_identifier, "negotiation_status"). \
        filter(attributes__contains={
                'negotiation_status': [
                    "Intended (Expression of interest)", "Intended (Under negotiation)", "Concluded (Oral Agreement)",
                    "Concluded (Contract signed)"
                ]
            }
        ). \
        filter(date__lt='2000-01-01')

    implementation_stati = attributes_for_activity(activity_identifier, "implementation_status"). \
        filter(attributes__contains={
            'implementation_status': ["Startup phase (no production)", "In operation (production)"]}
        ). \
        filter(date__lt='2000-01-01')
    return len(negotiation_stati) > 0 or len(implementation_stati) > 0


def _calculate_deal_scope(activity_identifier):
    activity = Activity.get_latest_active_activity(activity_identifier)
    # activity could be pending, needs to check
    if not activity:
        return None

    involvements = InvestorActivityInvolvement.objects.get_involvements_for_activity(activity)
    target_countries = _get_target_countries(activity_identifier)
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


def _get_target_countries(activity_identifier):
    return {c.attributes['target_country'] for c in attributes_for_activity(activity_identifier, "target_country")}


def _calculate_deal_size(activity_identifier, negotiation_status):
    intended_size = nonnull_attributes_for_activity(activity_identifier, "intended_size").order_by("-date")
    intended_size = len(intended_size) > 0 and intended_size[0].value or None
    contract_size = nonnull_attributes_for_activity(activity_identifier, "contract_size").order_by("-date")
    contract_size = len(contract_size) > 0 and contract_size[0].value or None
    production_size = nonnull_attributes_for_activity(activity_identifier, "production_size").order_by("-date")
    production_size = len(production_size) > 0 and production_size[0].value or None
    if negotiation_status in ("Intended (Expression of interest)", "Intended (Under negotiation)"):
        # intended deal
        if not intended_size and contract_size:
            intended_size = contract_size
        elif not intended_size and not contract_size and production_size:
            intended_size = production_size
        return intended_size
    elif negotiation_status in ("Concluded (Oral Agreement)", "Concluded (Contract signed)"):
        # concluded deal
        if not contract_size and production_size:
            contract_size = production_size
        return contract_size
    elif negotiation_status == "Failed (Negotiations failed)":
        # intended but failed deal
        if not intended_size and contract_size:
            intended_size = contract_size
        elif not intended_size and not contract_size and production_size:
            intended_size = production_size
        return intended_size
    elif negotiation_status == "Failed (Contract canceled)":
        # concluded but failed
        if not contract_size and production_size:
            contract_size = production_size
        return contract_size


def get_most_current_state(states_without_year, states_sorted_by_year, state_ranking, attr):
    most_current_state = None
    deal_state = None
    ranking = 0
    # find stati without year and highest ranking
    for n in states_without_year:
        r = state_ranking.get(n.attributes[attr])
        if r > ranking:
            ranking = r
            deal_state = n
    # select most current  status (highest year and highest ranking)
    for n in states_sorted_by_year:
        if not most_current_state:
            most_current_state = n
        elif most_current_state.date == n.date:
            if state_ranking.get(n.attributes[attr]) > state_ranking.get(most_current_state.attributes[attr]):
                most_current_state = n
        else:
            break
    if most_current_state:
        # prioritize stati without year and higher ranking
        if state_ranking.get(most_current_state.attributes[attr]) > ranking:
            deal_state = most_current_state
    return deal_state


def attributes_sorted_by_date(activity_identifier, attribute):
    return attributes_for_activity(activity_identifier, attribute).order_by("-date")


def attributes_without_date(activity_identifier, attribute):
    return attributes_for_activity(activity_identifier, attribute).filter(date__isnull=True)


def latest_attribute_value_for_activity(activity_identifier, attribute):
        attributes = nonnull_attributes_for_activity(activity_identifier, attribute).order_by("-date")
        return len(attributes) > 0 and attributes[0].attributes[attribute] or None

def nonnull_attributes_for_activity(activity_identifier, attribute):
    return attributes_for_activity(activity_identifier, attribute).filter(attributes__isnull={attribute: True})


def attributes_for_activity(activity_identifier, attribute):
    return ActivityAttributeGroup.objects. \
        filter(fk_activity__activity_identifier=activity_identifier). \
        filter(attributes__contains=[attribute])


def _affected_activity_identifiers(activity, operational_stakeholder):
    involvements = _active_involvements_except_activity(activity, operational_stakeholder)
    return set([i.fk_activity.activity_identifier for i in involvements])


def _add_info_message(activity, activity_identifiers, operational_stakeholder, request):

    if activity_identifiers:
        links = [
            "<a target=\"_blank\" href=\"/browse/deal/%(id)s/\">#%(id)s</a>" % {"id": i}
            for i in activity_identifiers
        ]
        messages.info(request, "Updated secondary investors for deals: (%s)." % ",".join(links))

    skipped = _skipped_activity_identifiers(activity, operational_stakeholder)
    if skipped:
        links = [
            "<a target=\"_blank\" href=\"/browse/deal/%(id)s/\">#%(id)s</a>" % {"id": i}
            for i in skipped
        ]
        messages.info(request, "Skipped update of secondary investors for pending deals: (%s)." % ",".join(links))


def _skipped_activity_identifiers(activity, operational_stakeholder):
    return {
        i.fk_activity.activity_identifier
        for i in InvestorActivityInvolvement.objects.filter(fk_investor=operational_stakeholder).
            filter(fk_activity__fk_status__name="pending").
            exclude(fk_activity__activity_identifier=activity.activity_identifier)
        }


def _update_stakeholders_for_activity(activity_identifier, involvement_stakeholders, operational_stakeholder):

    latest = Activity.get_latest_active_activity(activity_identifier)
    if not latest:
        return

    existing_investors = {
        i.fk_investor.id for i in InvestorActivityInvolvement.objects.get_involvements_for_activity(latest)
    }

    for involved_stakeholder in involvement_stakeholders:
        _create_venture_involvement_or_update_investor_list(
            existing_investors, involved_stakeholder, operational_stakeholder
        )

    _remove_orphaned_venture_involvements(existing_investors, operational_stakeholder)


def _create_venture_involvement_or_update_investor_list(existing_investors, involved_stakeholder, operational_stakeholder):
    if involved_stakeholder["stakeholder"].id not in existing_investors:
        InvestorVentureInvolvement.objects.create(
            fk_venture=operational_stakeholder,
            fk_investor=involved_stakeholder["stakeholder"],
            investment_ratio=involved_stakeholder["investment_ratio"] or 0,
        )
    else:
        existing_investors.remove(involved_stakeholder["stakeholder"].id)


def _remove_orphaned_venture_involvements(existing_investors, operational_stakeholder):
    if len(existing_investors):
        InvestorVentureInvolvement.objects.filter(fk_venture=operational_stakeholder). \
            filter(fk_investor__in=existing_investors).delete()


def _active_involvements_except_activity(activity, operational_stakeholder):
    return InvestorActivityInvolvement.objects.filter(fk_investor=operational_stakeholder). \
        exclude(fk_activity__fk_status__name__in=("pending", "to_delete", "deleted", "rejected")). \
        exclude(fk_activity__activity_identifier=activity.activity_identifier)
