import os

from django.core.management.base import OutputWrapper
from django.test import TestCase

from apps.api.elasticsearch import *
from apps.landmatrix.tests.mixins import (
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    InvestorVentureInvolvementsFixtureMixin,
)


class APIElasticsearchTestCase(
    ActivitiesFixtureMixin,
    InvestorsFixtureMixin,
    InvestorActivityInvolvementsFixtureMixin,
    InvestorVentureInvolvementsFixtureMixin,
    TestCase,
):

    act_fixtures = [
        {"id": 10, "activity_identifier": 1, "attributes": {}},
        {"id": 20, "activity_identifier": 2, "attributes": {}},
        {"id": 21, "activity_identifier": 2, "fk_status_id": 1, "attributes": {}},
    ]
    inv_fixtures = [
        {"id": 10, "investor_identifier": 1},
        {"id": 20, "investor_identifier": 2},
        {"id": 21, "investor_identifier": 2, "fk_status_id": 1},
    ]
    act_inv_fixtures = {"10": "10", "20": "20", "21": "20"}
    inv_inv_fixtures = [{"fk_venture_id": "10", "fk_investor_id": "20"}]

    es_delay = 1

    required_properties = {
        "deal": [
            "id",
            "activity_identifier",
            "historical_activity_id",
            "history_date",
            "status",
            "is_public",
            "deal_scope",
            "deal_size",
            "current_contract_size",
            "current_production_size",
            "current_negotiation_status",
            "current_implementation_status",
            "init_date",
            "top_investors",
        ],
        "location": [
            "id",
            "activity_identifier",
            "historical_activity_id",
            "history_date",
            "status",
            "is_public",
            "deal_scope",
            "deal_size",
            "current_contract_size",
            "current_production_size",
            "current_negotiation_status",
            "current_implementation_status",
            "init_date",
            "top_investors",
        ],
        "data_source": [],
        "contract": [],
        "involvement_size": [
            "deal_id",
            "activity_identifier",
            "target_country",
            "target_country_display",
            "target_region",
            "target_region_display",
            "deal_size",
            "deal_scope",
        ],
        "investor": [
            "id",
            "investor_identifier",
            "top_investors",
            "deal_count",
            "roles",
            "parent_company_of",
            "tertiary_investor_of",
        ],
        "involvement": [],
    }

    def setUp(self):
        super().setUp()
        stdnull = OutputWrapper(open(os.devnull, "w"))
        self.elasticsearch = ElasticSearch(
            index_name="landmatrix_test", stdout=stdnull, stderr=stdnull
        )
        # Recreate index before every test
        self.elasticsearch.create_index()

    def test_get_elasticsearch_properties(self):
        # Check doc types mappings
        doc_types = DOC_TYPES_ACTIVITY + DOC_TYPES_INVESTOR
        for doc_type in doc_types:
            dt_mapping = get_elasticsearch_properties(doc_type)
            self.assertIn("properties", dt_mapping)
            self.assertGreater(len(dt_mapping.get("properties")), 0)

        # Check index mapping
        mapping = get_elasticsearch_properties()
        self.assertEqual(set(doc_types), set(mapping.keys()))
        for doc_type in doc_types:
            dt_mapping = mapping[doc_type]
            self.assertIn("properties", dt_mapping)
            self.assertGreater(len(dt_mapping.get("properties")), 0)

    def test_create_index(self):
        def index_exists():
            try:
                response = self.elasticsearch.conn.send_request(
                    "HEAD", [self.elasticsearch.index_name]
                )
                if response == "":
                    return True
            except ElasticHttpNotFoundError:
                pass
            return False

        self.elasticsearch.create_index()
        self.assertTrue(index_exists())

    def count_documents(self, doc_type, query):
        response = self.elasticsearch.conn.search(
            {"query": {"term": query}},
            index=self.elasticsearch.index_name,
            doc_type=doc_type,
        )
        return response["hits"]["total"]

    def assert_activity_indexed(self, activity_identifier):
        # FIXME: Check all DOC_TYPES_ACTIVITY in the future
        for doc_type in ("deal", "location"):
            self.assertGreater(
                self.count_documents(
                    doc_type, {"activity_identifier": activity_identifier}
                ),
                0,
                msg=f"No documents for doc type '{doc_type}'",
            )

    def assert_activity_not_indexed(self, activity_identifier):
        # FIXME: Check all DOC_TYPES_ACTIVITY in the future
        for doc_type in ("deal", "location"):
            self.assertEqual(
                0,
                self.count_documents(
                    doc_type, {"activity_identifier": activity_identifier}
                ),
                msg=f"Indexed documents for doc type '{doc_type}'",
            )

    def assert_investor_indexed(self, investor_identifier):
        # FIXME: Check all DOC_TYPES_INVESTOR in the future
        for doc_type in ("investor",):
            self.assertGreater(
                self.count_documents(
                    doc_type, {"investor_identifier": investor_identifier}
                ),
                0,
                msg=f"No documents for doc type '{doc_type}'",
            )

    def assert_investor_not_indexed(self, investor_identifier):
        # FIXME: Check all DOC_TYPES_INVESTOR in the future
        for doc_type in ("investor",):
            self.assertEqual(
                0,
                self.count_documents(
                    doc_type, {"investor_identifier": investor_identifier}
                ),
                msg=f"Indexed documents for doc type '{doc_type}'",
            )

    def test_index_activity_with_activity_identifier(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.elasticsearch.index_activity(
            activity_identifier=activity.activity_identifier
        )
        self.elasticsearch.refresh_index()
        self.assert_activity_indexed(activity.activity_identifier)

    def test_index_activity_with_activity_id(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.elasticsearch.index_activity(activity_id=activity.id)
        self.elasticsearch.refresh_index()
        self.assert_activity_indexed(activity.activity_identifier)

    def test_index_activity_with_activity(self):
        activity = HistoricalActivity.objects.get(id=10)
        self.elasticsearch.index_activity(activity=activity)
        self.elasticsearch.refresh_index()
        self.assert_activity_indexed(activity.activity_identifier)

    def test_index_activity_documents_with_activity_identifiers(self):
        self.elasticsearch.index_activity_documents(activity_identifiers=[1])
        self.elasticsearch.refresh_index()
        self.assert_activity_indexed(1)

    def test_index_activity_documents_without_activity_identifiers(self):
        self.elasticsearch.index_activity_documents()
        self.elasticsearch.refresh_index()
        self.assert_activity_indexed(1)

    def test_index_investor_with_investor_identifier(self):
        investor = HistoricalInvestor.objects.get(id=10)
        self.elasticsearch.index_investor(
            investor_identifier=investor.investor_identifier
        )
        self.elasticsearch.refresh_index()
        self.assert_investor_indexed(investor.investor_identifier)

    def test_index_investor_with_investor_id(self):
        investor = HistoricalInvestor.objects.get(id=10)
        self.elasticsearch.index_investor(investor_id=investor.id)
        self.elasticsearch.refresh_index()
        self.assert_investor_indexed(investor.investor_identifier)

    def test_index_investor_with_investor(self):
        investor = HistoricalInvestor.objects.get(id=10)
        self.elasticsearch.index_investor(investor=investor)
        self.elasticsearch.refresh_index()
        self.assert_investor_indexed(investor.investor_identifier)

    def test_index_investor_documents_with_investor_identifiers(self):
        self.elasticsearch.index_investor_documents(investor_identifiers=[1])
        self.elasticsearch.refresh_index()
        self.assert_investor_indexed(1)

    def test_index_investor_documents_without_investor_identifiers(self):
        self.elasticsearch.index_investor_documents()
        self.elasticsearch.refresh_index()
        self.assert_investor_indexed(1)

    def test_get_activity_versions_with_pending(self):
        versions = self.elasticsearch.get_activity_versions(2)
        status = [v.fk_status_id for v in versions]
        self.assertEqual(len(versions), 2)
        self.assertIn(1, status)

    def test_get_activity_versions_without_pending(self):
        versions = self.elasticsearch.get_activity_versions(1)
        status = [v.fk_status_id for v in versions]
        self.assertEqual(len(versions), 1)
        self.assertNotIn(1, status)

    def test_get_activity_documents(self):
        activity = HistoricalActivity.objects.get(id=10)
        # FIXME: Check all DOC_TYPES_ACTIVITY in the future
        for doc_type in ("deal", "location"):
            docs = self.elasticsearch.get_activity_documents(
                activity, doc_type=doc_type
            )
            props = self.required_properties.get(doc_type)
            for doc in docs:
                for prop in props:
                    self.assertIn(
                        prop,
                        doc.keys(),
                        msg=f"Missing property '{prop}' for doc type '{doc_type}'",
                    )

    def test_get_spatial_properties(self):
        doc = {
            "location_count": 2,
            "point_lat": ["foo", "1"],
            "point_lon": ["bar", "1"],
            "target_country": [None, "104"],
        }
        props = self.elasticsearch.get_spatial_properties(doc)
        self.assertEqual(props.get("point_lat"), ["foo", "1"])
        self.assertEqual(props.get("point_lon"), ["bar", "1"])
        self.assertEqual(props.get("geo_point"), ["0,0", "1,1"])
        self.assertEqual(props.get("target_country"), [104])
        self.assertEqual(props.get("target_country_display"), ["Myanmar"])
        self.assertEqual(props.get("target_region"), [142])
        self.assertEqual(props.get("target_region_display"), ["Asia"])

    def test_get_display_properties(self):
        properties = {
            "deal": {
                "current_negotiation_status": [
                    "Under negotiation",
                    "Intended (Under negotiation)",
                ],
                "current_implementation_status": [
                    "Project not started",
                    "Project not started",
                ],
                "is_public": ["True", "Yes"],
                "target_country": ["104", ["Myanmar"]],
            },
            "location": {
                "current_negotiation_status": [
                    "Under negotiation",
                    "Intended (Under negotiation)",
                ],
                "current_implementation_status": [
                    "Project not started",
                    "Project not started",
                ],
                "is_public": ["True", "Yes"],
                "target_country": ["104", ["Myanmar"]],
            },
            "investor": {"fk_country": ["104", "Myanmar"]},
            "involvement": {},
        }
        for doc_type, props in properties.items():
            doc = dict((k, v[0]) for k, v in props.items())
            display_props = self.elasticsearch.get_display_properties(
                doc, doc_type=doc_type
            )
            for key, value in props.items():
                self.assertEqual(
                    value[1],
                    display_props.get(f"{key}_display"),
                    msg=f"Wrong display value for property '{key}' in doc type '{doc_type}'",
                )

    def test_get_investor_versions_with_pending(self):
        versions = self.elasticsearch.get_investor_versions(2)
        status = [v.fk_status_id for v in versions]
        self.assertEqual(len(versions), 2)
        self.assertIn(1, status)

    def test_get_investor_versions_without_pending(self):
        versions = self.elasticsearch.get_investor_versions(1)
        status = [v.fk_status_id for v in versions]
        self.assertEqual(len(versions), 1)
        self.assertNotIn(1, status)

    def test_get_investor_documents(self):
        investor = HistoricalInvestor.objects.get(id=10)
        # FIXME: Check all DOC_TYPES_INVESTOR in the future
        for doc_type in ("investor",):
            docs = self.elasticsearch.get_investor_documents(
                investor, doc_type=doc_type
            )
            props = self.required_properties.get(doc_type)
            for doc in docs:
                for prop in props:
                    self.assertIn(
                        prop,
                        doc.keys(),
                        msg=f"Missing property '{prop}' for doc type '{doc_type}'",
                    )

    def test_search(self):
        self.elasticsearch.index_activity(activity_identifier=1)
        self.elasticsearch.index_activity(activity_identifier=2)
        self.elasticsearch.refresh_index()
        results = self.elasticsearch.search(
            query={"terms": {"activity_identifier": [1, 2]}},
            doc_type="deal",
            sort={"activity_identifier": "desc"},
        )
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0].get("_source", {}).get("activity_identifier"), 2)

    def test_aggregate(self):
        self.elasticsearch.index_activity(activity_identifier=1)
        self.elasticsearch.index_activity(activity_identifier=2)
        self.elasticsearch.refresh_index()
        aggregations = {
            "activity_identifiers": {"terms": {"field": "activity_identifier"}}
        }
        results = self.elasticsearch.search(
            query={"terms": {"activity_identifier": [1, 2]}},
            aggs=aggregations,
            doc_type="deal",
        )
        activity_identifiers = results.get("activity_identifiers", {}).get(
            "buckets", []
        )
        activity_identifiers = set([b["key"] for b in activity_identifiers])
        self.assertEqual(activity_identifiers, {1, 2})

    def test_delete_activity(self):
        self.elasticsearch.index_activity(activity_identifier=1)
        self.elasticsearch.refresh_index()
        self.elasticsearch.delete_historicalactivity(1)
        self.elasticsearch.refresh_index()
        self.assert_activity_not_indexed(activity_identifier=1)

    def test_delete_investor(self):
        self.elasticsearch.index_investor(investor_identifier=1)
        self.elasticsearch.refresh_index()
        self.elasticsearch.delete_historicalinvestor(1)
        self.elasticsearch.refresh_index()
        self.assert_investor_not_indexed(investor_identifier=1)
