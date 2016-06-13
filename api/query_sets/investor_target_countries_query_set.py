from api.query_sets.fake_query_set_with_subquery import FakeQuerySetFlat


class TargetCountriesForInvestorCountryQuerySet(FakeQuerySetFlat):
    FIELDS = [
        ('country_id', "target_country.value")
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute AS target_country ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
    ]
    APPLY_GLOBAL_FILTERS = False

    def __init__(self, request):
        super().__init__(request)
        self.country = request.GET.get("country", "")

    def all(self):
        if self.country:
            self._additional_wheres.append(
                "operational_stakeholder.fk_country_id = {}".format(self.country)
            )
        return super().all()


class InvestorCountriesForTargetCountryQuerySet(FakeQuerySetFlat):
    FIELDS = [
        ('country_id', 'operational_stakeholder.fk_country_id')
    ]
    ADDITIONAL_JOINS = [
        "LEFT JOIN landmatrix_activityattribute AS target_country ON a.id = target_country.fk_activity_id AND target_country.name = 'target_country'",
    ]
    APPLY_GLOBAL_FILTERS = False

    def __init__(self, request):
        super().__init__(request)
        self.country = request.GET.get("country", "")

    def all(self):
        if self.country:
            self._additional_wheres.append(
                "target_country.value = '%s'" % self.country
            )
        return super().all()
