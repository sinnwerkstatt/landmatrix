from .models.choices import InvestorClassificationEnum
from .models.country import Country
from .models.investor import InvestorHull, InvestorVersion
from .serializers import SimpleInvestorSerializer


def test_get_simple_investors(api_client):
    investor = InvestorHull.objects.create(id=500)

    res = api_client.get("/api/investors/simple/")
    data = list(res.data)

    assert SimpleInvestorSerializer(data=data, many=True).is_valid()
    assert data == [
        {
            "id": 500,
            "active": False,
            "name": None,
            "name_unknown": None,
            "country_id": None,
            "classification": None,
            "deleted": False,
        }
    ], "Return None as name if neither active nor draft version."

    investor.draft_version = InvestorVersion.objects.create(
        id=501,
        investor=investor,
        name="Unknown",
    )
    investor.save()

    res = api_client.get("/api/investors/simple/")
    data = list(res.data)

    assert SimpleInvestorSerializer(data=data, many=True).is_valid()
    assert data == [
        {
            "id": 500,
            "name": "Unknown",
            "name_unknown": True,
            "country_id": None,
            "classification": None,
            "active": False,
            "deleted": False,
        }
    ], "Return name of draft version if investor has no active version."

    investor.active_version = InvestorVersion.objects.create(
        id=502,
        investor=investor,
        name="Bad Company",
        classification=InvestorClassificationEnum.ASSET_MANAGEMENT_FIRM,
        country=Country.objects.get(id=724, name="Spain"),
    )
    investor.save()

    res = api_client.get("/api/investors/simple/")
    data = list(res.data)

    assert SimpleInvestorSerializer(data=data, many=True).is_valid()
    assert data == [
        {
            "id": 500,
            "name": "Bad Company",
            "name_unknown": False,
            "country_id": 724,
            "classification": InvestorClassificationEnum.ASSET_MANAGEMENT_FIRM,
            "active": True,
            "deleted": False,
        }
    ], "Return active version name if investor has active version."
