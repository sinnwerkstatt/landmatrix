from apps.landmatrix.forms.deal import DealForm


def test_deal_form():
    assert DealForm({}).errors == {}

    assert DealForm({"locations": [{"id": 12}]}).is_valid()
    assert not DealForm({"locations": [{"id": "12"}]}).is_valid()
    assert DealForm({"locations": [{"id": "abcdef12"}]}).is_valid()
    assert DealForm({"locations": [{"point": {"lat": -89, "lng": 170}}]}).is_valid()
    assert not DealForm(
        {"locations": [{"point": {"lat": -100, "lng": 170}}]}
    ).is_valid()
    assert DealForm({"locations": [{"level_of_accuracy": "COUNTRY"}]}).is_valid()
    assert not DealForm({"locations": [{"level_of_accuracy": "-INVALID-"}]}).is_valid()

    # TODO Contracts
    # TODO DataSources

    assert DealForm({"country": 800}).is_valid()
    assert not DealForm({"country": 8000}).is_valid()

    assert DealForm({"intended_size": 123.23}).errors == {}
    assert DealForm({"intended_size": "123.23"}).errors == {}
    assert not DealForm({"intended_size": "abc"}).errors == {}

    assert DealForm(
        {
            "contract_size": [
                {"current": True, "date": "2022", "area": 23},
            ]
        }
    ).is_valid()
    assert not DealForm({"contract_size": [{"current": "No"}]}).is_valid()
    assert not DealForm({"contract_size": [{"date": "12.12.2022"}]}).is_valid()
    assert not DealForm({"contract_size": [{"area": "100 ha"}]}).is_valid()

    assert DealForm({"land_area_comment": "Hallo"}).is_valid()

    assert DealForm(
        {
            "intention_of_investment": [
                {
                    "current": True,
                    "date": "2022",
                    "area": 23,
                    "choices": ["BIOFUELS", "FOOD_CROPS"],
                }
            ]
        }
    ).is_valid()
    assert DealForm({"intention_of_investment": [{"current": "Yes"}]}).errors == {
        "intention_of_investment": ["data[0].current must be boolean or null"]
    }
    assert DealForm({"intention_of_investment": [{"date": "2022-126"}]}).errors == {
        "intention_of_investment": [
            "data[0].date must match pattern ^\\d{4}(-(0?[1-9]|1[012]))?(-(0?[1-9]|[12][0-9]|3[01]))?$"
        ]
    }
    assert DealForm({"intention_of_investment": [{"area": "ab"}]}).errors == {
        "intention_of_investment": ["data[0].area must be number or null"]
    }
    assert not DealForm(
        {"intention_of_investment": [{"choices": "BIOFUELS"}]}
    ).is_valid()
    assert not DealForm({"intention_of_investment": [{"choices": ["X"]}]}).is_valid()

    assert DealForm({"nature_of_deal": ["OUTRIGHT_PURCHASE", "LEASE"]}).is_valid()
    assert not DealForm({"nature_of_deal": ["XS"]}).is_valid()
    assert DealForm({"nature_of_deal": "OUTRIGHT_PURCHASE"}).is_valid()
    assert not DealForm({"nature_of_deal": "XS"}).is_valid()

    assert DealForm(
        {
            "negotiation_status": [
                {"current": True, "date": "2022", "choice": "EXPRESSION_OF_INTEREST"}
            ]
        }
    ).is_valid()
    assert DealForm(
        {"negotiation_status": [{"choice": "UNDER_NEGOTIATION"}]}
    ).is_valid()
    assert not DealForm(
        {"negotiation_status": ["EXPRESSION_OF_INTEREST", "UNDER_NEGOTIATION"]}
    ).is_valid()
    assert not DealForm({"negotiation_status": [{"current": "No"}]}).is_valid()
    assert not DealForm({"negotiation_status": [{"date": "Yesteryear"}]}).is_valid()
    assert not DealForm({"negotiation_status": [{"choice": "XX"}]}).is_valid()

    assert DealForm({"purchase_price_type": "PER_HA"}).is_valid()
    assert not DealForm({"purchase_price_type": "BLA"}).is_valid()

    assert DealForm({"contract_farming": None}).is_valid()
    assert DealForm({"contract_farming": True}).is_valid()

    assert DealForm(
        {
            "on_the_lease": [
                {
                    "current": True,
                    "date": "2022",
                    "area": 123,
                    "farmers": 100,
                    "households": 200,
                }
            ]
        }
    ).is_valid()

    assert DealForm(
        {
            "total_jobs_current": [
                {"current": True, "jobs": 200, "employees": 300, "workers": 100}
            ]
        }
    ).is_valid()

    assert DealForm(
        {"involved_actors": [{"name": "Sinnwerkstatt", "choice": "BROKER"}]}
    ).is_valid()
    assert not DealForm(
        {"involved_actors": [{"name": "Sinnwerkstatt", "choice": "GEEKS"}]}
    ).is_valid()

    assert (
        DealForm(
            {"crops": [{"current": True, "date": "2022", "choices": ["ACC"]}]}
        ).errors
        == {}
    )
    # TODO
