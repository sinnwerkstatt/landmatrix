from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from apps.landmatrix.models import (
    HistoricalActivity,
    FilterPreset,
    HistoricalInvestorVentureInvolvement,
    HistoricalActivity,
)
from apps.landmatrix.models.investor import HistoricalInvestor, InvestorBase


class FilterPresetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterPreset
        exclude = ("is_default_country", "is_default_global")


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "full_name")


class RegionSerializer(serializers.BaseSerializer):
    """
    Returns a region as a list: [id, slug, title].
    """

    def to_representation(self, obj):
        return [obj.region.id, obj.region.slug, obj.title]


class DealLocationSerializer(serializers.Serializer):
    point_lat = serializers.DecimalField(max_digits=11, decimal_places=8)
    point_lon = serializers.DecimalField(max_digits=11, decimal_places=8)
    contract_area = GeometryField()
    intended_area = GeometryField()
    production_area = GeometryField()

    def to_representation(self, obj):
        """
        Convert our binary polygon representation to a GEOSGeometry.
        """
        # TODO: DRY, we should have a model with a list of these fields
        for geo_field in ("contract_area", "intended_area", "production_area"):
            if geo_field in obj and obj[geo_field]:
                if not isinstance(obj[geo_field], GEOSGeometry):
                    obj[geo_field] = GEOSGeometry(obj[geo_field], srid=4326)

        return super().to_representation(obj)


class DealSerializer(serializers.Serializer):
    """
    Used to serialize the deal list view.
    """

    deal_id = serializers.IntegerField()
    intention = serializers.CharField()
    intended_size = serializers.IntegerField()
    contract_size = serializers.IntegerField()
    production_size = serializers.IntegerField()
    investor = serializers.CharField()
    locations = serializers.ListField(child=DealLocationSerializer())

    def to_representation(self, obj):
        locations = []
        location_fields = self.fields["locations"].child.fields.keys()
        array_elements = [obj[field] for field in location_fields]
        split_elements = [elem.split(";") for elem in array_elements]

        for values in zip(*split_elements):
            location = {}
            for field_name, value in zip(location_fields, values):
                location[field_name] = value or None

            locations.append(location)

        # For our intfields, we sometimes get unexpected floats. Round those.
        for field in ("contract_size", "intended_size", "production_size"):
            value = obj[field]
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = round(float(value))
                    except ValueError:
                        value = None
                obj[field] = value

        obj["locations"] = locations

        return super().to_representation(obj)


class DealInvestorNetworkSerializer(serializers.BaseSerializer):
    """
    This serializer takes an investor and outputs a list of involvements
    formatted like:
    {
        "id": 123,
        "name": "",
        "country": "",
        "classification": "",
        "homepage": "",
        "opencorporates_link": "",
        "comment": "",
        "stakeholders": [
            {
                "id": 345,
                "name": "",
                [...]
                "involvement": [
                    "parent_type": "stakeholder" // or "investor"
                    "percentage": "",
                    "investment_type": "",
                    "loans_amount": "",
                    "loans_currency": "",
                    "loans_date": "",
                    "comment": "",
                ],
                "stakeholders": [],
            },
            [...]
        ],
    }
    This is not REST, but it maintains compatibility with the existing API.
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def _get_investor_data(self, investor, is_root=True):
        investor_identifier = investor.investor_identifier
        country = investor.fk_country
        return {
            "id": f"I{investor_identifier}",
            "type": "investor",
            "name": investor.name,
            "status": investor.fk_status.name,
            "is_root": is_root,
            "identifier": investor_identifier,
            "country": str(country) if country else "",
            "country_code": str(country.code_alpha2) if country else "",
            "classification": investor.get_classification_display(),
            "homepage": investor.homepage,
            "opencorporates_link": investor.opencorporates_link,
            "comment": investor.comment,
            "url": reverse(
                "investor_detail", kwargs={"investor_id": investor_identifier}
            ),
            "investors": [],
        }

    def _get_investor_link_data(self, involvement):
        return {
            "percentage": involvement.percentage,
            "investment_type": involvement.get_investment_type_display(),
            "loans_amount": involvement.loans_amount,
            "loans_currency": str(involvement.loans_currency),
            "loans_date": involvement.loans_date,
            "parent_relation": involvement.get_parent_relation_display(),
            "comment": involvement.comment,
        }

    def to_representation(
        self,
        obj,
        parent_types=["parent_stakeholders", "parent_investors"],
        show_deals=False,
        is_root=True,
    ):
        response = self._get_investor_data(obj, is_root)
        involvements = HistoricalInvestorVentureInvolvement.objects.filter(
            fk_venture=obj
        )
        if self.user and not self.user.is_authenticated:
            involvements = involvements.filter(
                fk_investor__fk_status_id__in=(
                    InvestorBase.STATUS_ACTIVE,
                    InvestorBase.STATUS_OVERWRITTEN,
                )
            )
        for parent_type in parent_types:
            parents = []
            if parent_type == "parent_investors":
                parent_involvements = involvements.investors()
            else:
                parent_involvements = involvements.stakeholders()
            for i, involvement in enumerate(parent_involvements):
                investor_identifier = involvement.fk_investor.investor_identifier
                # Always get latest version of parent investor
                parent_investor = HistoricalInvestor.objects.filter(
                    investor_identifier=investor_identifier
                )
                if self.user and not self.user.is_authenticated:
                    parent_investor = parent_investor.filter(
                        fk_status_id__in=(
                            InvestorBase.STATUS_ACTIVE,
                            InvestorBase.STATUS_OVERWRITTEN,
                        )
                    )
                parent_investor = parent_investor.latest()
                parent = self.to_representation(
                    parent_investor, parent_types, is_root=False
                )
                parent["type"] = (
                    "tertiary" if parent_type == "parent_investors" else "parent"
                )
                parent["involvement"] = self._get_investor_link_data(involvement)
                parents.append(parent)
            response["investors"].extend(parents)

        return response


class InvestorNetworkSerializer(serializers.BaseSerializer):
    """
    This serializer takes an investor and outputs a list of involvements
    formatted like:
    {
        "id": "I123",
        "name": "",
        "country": "",
        "classification": "",
        "homepage": "",
        "opencorporates_link": "",
        "comment": "",
        "investors": [
            {
                "id": "I345",
                "name": "",
                [...]
                "involvement": [
                    "parent_type": "stakeholder" // or "investor"
                    "percentage": "",
                    "investment_type": "",
                    "loans_amount": "",
                    "loans_currency": "",
                    "loans_date": "",
                    "comment": "",
                ],
                "investors": [],
            },
        ],
        "deals": [
            {
                "id": "D123",
                "type": 2,
                "name": 123,
                "status": "active",
                "identifier": 123,
                "country": "Cambodia",
                "country_code": "CD",
                "intention": "",
                "nature": "",
                "negotiation_status": "",
                "implementation_status": "",
                "intended_size": "",
                "contract_size": "",
                "production_size": "",
                "url": "",
            },
        ]
    }
    This is not REST, but it maintains compatibility with the existing API.
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def _get_investor_data(self, investor, is_root=False):
        investor_identifier = investor.investor_identifier
        country = investor.fk_country
        return {
            "id": f"I{investor_identifier}",
            "type": "investor",
            "name": investor.name,
            "status": investor.fk_status.name,
            "is_root": is_root,
            "identifier": investor_identifier,
            "country": str(country) if country else "",
            "country_code": str(country.code_alpha2) if country else "",
            "classification": investor.get_classification_display(),
            "homepage": investor.homepage,
            "opencorporates_link": investor.opencorporates_link,
            "comment": investor.comment,
            "url": reverse(
                "investor_detail", kwargs={"investor_id": investor_identifier}
            ),
            "investors": [],
            "deals": [],
        }

    def _get_deal_data(self, activity):
        activity_identifier = activity.activity_identifier
        target_country = activity.target_country
        return {
            "id": f"D{activity_identifier}",
            "type": "deal",
            "name": str(activity_identifier),
            "status": activity.fk_status.name,
            "identifier": activity_identifier,
            "country": str(target_country) if target_country else "",
            "country_code": str(target_country.code_alpha2) if target_country else "",
            "intention": activity.get_current("intention"),
            "nature": activity.get_current("nature"),
            "negotiation_status": activity.get_negotiation_status(),
            "implementation_status": activity.get_implementation_status(),
            "intended_size": activity.get_intended_size(),
            "contract_size": activity.get_contract_size(),
            "production_size": activity.get_production_size(),
            "url": reverse("deal_detail", kwargs={"deal_id": activity_identifier}),
        }

    def _get_investor_link_data(self, involvement, investor_identifier):
        ROLE_MAP = {
            HistoricalInvestorVentureInvolvement.STAKEHOLDER_ROLE: "parent",
            HistoricalInvestorVentureInvolvement.INVESTOR_ROLE: "tertiary",
        }
        if involvement.fk_investor.investor_identifier == investor_identifier:
            direction = "parent"
        else:
            direction = "child"
        return {
            "dir": direction,
            "type": ROLE_MAP.get(involvement.role, "operating"),
            "percentage": involvement.percentage,
            "investment_type": involvement.get_investment_type_display(),
            "loans_amount": involvement.loans_amount,
            "loans_currency": str(involvement.loans_currency),
            "loans_date": involvement.loans_date,
            "parent_relation": involvement.get_parent_relation_display(),
            "comment": involvement.comment,
        }

    def _has_next_level(self, investor):
        return investor.venture_involvements.count() > 0

    def to_representation(
        self, obj, show_deals=True, depth=1, is_root=True, processed=None
    ):
        response = self._get_investor_data(obj, is_root)

        # Skip next level if maximum depth reached or investor already processed
        investor_identifier = obj.investor_identifier

        if processed is None:
            processed = {"investors": set(), "involvements": set()}
        if depth == 0 or investor_identifier in processed["investors"]:
            return response
        processed["investors"].add(investor_identifier)

        # Get parent investors (where current investor is "parent" or "child")
        if self.user and self.user.is_authenticated:
            status = HistoricalInvestor.PUBLIC_STATUSES + \
                     (HistoricalInvestor.STATUS_PENDING,)
        else:
            status = HistoricalInvestor.PUBLIC_STATUSES
        involvements = HistoricalInvestorVentureInvolvement.objects.latest_only(status)
        involvements = involvements.filter(
            Q(fk_venture__investor_identifier=investor_identifier)
            | Q(fk_investor__investor_identifier=investor_identifier)
        ).distinct()

        investors = []
        for i, involvement in enumerate(involvements):
            inv_key = f"{involvement.fk_venture.investor_identifier}-{involvement.fk_investor.investor_identifier}"
            if inv_key in processed["involvements"]:
                continue
            processed["involvements"].add(inv_key)
            if involvement.fk_investor.investor_identifier != investor_identifier:
                related_identifier = involvement.fk_investor.investor_identifier
            else:
                related_identifier = involvement.fk_venture.investor_identifier
            # Always get latest version of parent investor
            related_investor = HistoricalInvestor.objects.latest_only(status)
            related_investor = related_investor.filter(
                investor_identifier=related_identifier
            ).latest()
            related = self.to_representation(
                related_investor,
                show_deals=show_deals,
                depth=depth - 1,
                is_root=False,
                processed=processed,
            )
            related["involvement"] = self._get_investor_link_data(
                involvement, investor_identifier
            )
            investors.append(related)
        response["investors"].extend(investors)

        # Get deals (where current investor is an operating company)
        if show_deals:
            deals = []
            # Create deal node and links
            activities = HistoricalActivity.objects.latest_only(status)
            activities = activities.filter(
                involvements__fk_investor__investor_identifier=investor_identifier
            ).distinct()
            for activity in activities:
                deals.append(self._get_deal_data(activity))
            response["deals"].extend(deals)

        return response
