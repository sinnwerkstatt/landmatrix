import pytest

from rest_framework import status


@pytest.mark.django_db
def test_deals_toggle_deleted(
    api_client,
    deals,
    anybody2,
    reporter2,
    editor2,
    admin2,
    superuser2,
):
    deal = deals[0]
    url = f"/api/deals/{deal.pk}/toggle_deleted/"

    response = api_client.put(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    deal.refresh_from_db()
    assert not deal.deleted
    assert deal.deleted_comment == ""

    for user in [anybody2, reporter2, editor2]:
        api_client.force_authenticate(user=user)
        response = api_client.put(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user=admin2)
    response = api_client.put(url, {"deleted": True, "comment": "They bribed us."})
    assert response.status_code == status.HTTP_200_OK

    deal.refresh_from_db()
    assert deal.deleted
    assert deal.deleted_comment == "They bribed us."

    response = api_client.put(url, {"deleted": False, "comment": "But we want more."})
    assert response.status_code == status.HTTP_200_OK

    deal.refresh_from_db()
    assert not deal.deleted
    assert deal.deleted_comment == "But we want more."

    api_client.force_authenticate(user=superuser2)
    response = api_client.put(url, {"deleted": True, "comment": "And they agreed."})

    assert response.status_code == status.HTTP_200_OK

    deal.refresh_from_db()
    assert deal.deleted


@pytest.mark.django_db
def test_deals_toggle_confidential(
    api_client,
    deals,
    anybody2,
    reporter2,
    editor2,
    admin2,
    superuser2,
):
    deal = deals[0]
    url = f"/api/deals/{deal.pk}/toggle_confidential/"

    response = api_client.put(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    deal.refresh_from_db()
    assert not deal.confidential
    assert deal.confidential_comment == ""

    for user in [anybody2, reporter2, editor2]:
        api_client.force_authenticate(user=user)
        response = api_client.put(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user=admin2)
    response = api_client.put(url, {"confidential": True, "comment": "They bribed us."})
    assert response.status_code == status.HTTP_200_OK

    deal.refresh_from_db()
    assert deal.confidential
    assert deal.confidential_comment == "They bribed us."

    response = api_client.put(
        url, {"confidential": False, "comment": "But we want more."}
    )
    assert response.status_code == status.HTTP_200_OK

    deal.refresh_from_db()
    assert not deal.confidential
    assert deal.confidential_comment == "But we want more."

    api_client.force_authenticate(user=superuser2)
    response = api_client.put(
        url, {"confidential": True, "comment": "And they agreed."}
    )
    assert response.status_code == status.HTTP_200_OK

    deal.refresh_from_db()
    assert deal.confidential
