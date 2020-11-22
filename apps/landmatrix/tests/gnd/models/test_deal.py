import pytest

from apps.landmatrix.models import Deal, Location


@pytest.mark.django_db
def test_get_deal_size():
    Deal.objects.create(
        id=3,
        intended_size=100.234,
        contract_size=[{"date": "2008", "value": "1000"}],
        production_size=[{"value": "10"}],
        negotiation_status=[{"date": "2008", "value": "EXPRESSION_OF_INTEREST"}],
        modified_at="2020-10-10",
    )
    d3 = Deal.objects.get(id=3)
    assert d3.deal_size == 100
    d3.negotiation_status = [
        {"date": "2008", "value": "EXPRESSION_OF_INTEREST"},
        {"date": "2010", "value": "ORAL_AGREEMENT"},
    ]
    d3.save()
    assert d3.deal_size == 1000
    d3.contract_size = None
    d3.save()
    assert d3.deal_size == 10
    d3.negotiation_status = None
    d3.save()
    assert d3.deal_size == 0


# def test_some_reversion_stuff(db):
#     deal_id = 9998
#     assert not Deal.objects.filter(id=deal_id)
#
#     d9998 = Deal(id=deal_id)
#     d9998.community_consultation_comment = "comm consul comm"
#     d9998.save_revision(status=2)
#     d9998.refresh_from_db()
#
#     assert d9998.community_consultation_comment == "comm consul comm"
#     versions = Version.objects.get_for_object(d9998)
#     assert len(versions) == 1
#
#     d9998.community_consultation_comment = "comm x"
#     d9998.save_revision(status=1)
#     d9998.refresh_from_db()
#     assert d9998.community_consultation_comment == "comm consul comm"
#     versions = Version.objects.get_for_object(d9998)
#     assert len(versions) == 2
#     assert versions[0].field_dict["community_consultation_comment"] == "comm x"
#     assert versions[1].field_dict["community_consultation_comment"] == "comm consul comm"
#
#     with reversion.create_revision():
#         l1 = Location(deal=d9998, name="Berlin", level_of_accuracy="ADMINISTRATIVE_REGION")
#         # reversion.add_to_revision(l1)
#         l1.save()
#
#         reversion.add_to_revision(d9998)
#         # l1.save()
#         # versions = Version.objects.get_for_object(l1)
#         # print(versions)
#
#     print(Version.objects.get_for_model(Location))
#     d9998.refresh_from_db()
#     versions = Version.objects.get_for_object(d9998)
#     print(versions)
#     assert len(versions) == 3
#     rev1 = versions[0].revision
#     print(rev1)
#     print(rev1.version_set.all())
#     print([r.version_set() for r in Revision.objects.all()])
#     # assert d9998.locations.all() == [l1]
#     # versions = Version.objects.get_for_object(d9998)
#     # assert versions[0].field_dict["locations"] == "s"
#     assert False
#
#         # Location(deal=d1)
#         # d1.save_revision(status=1)
