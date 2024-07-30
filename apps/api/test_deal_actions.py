import pytest

from rest_framework import status

from apps.landmatrix.models.new import DealHull


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
    pk = deals[0].pk
    url = f"/api/deals/{pk}/toggle_deleted/"

    response = api_client.put(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    for user in [anybody2, reporter2, editor2]:
        api_client.force_authenticate(user=user)
        response = api_client.put(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user=admin2)
    response = api_client.put(url, {"deleted": True, "comment": "They bribed us."})
    assert response.status_code == status.HTTP_200_OK

    assert DealHull.objects.get(pk=pk).deleted
    assert DealHull.objects.get(pk=pk).deleted_comment == "They bribed us."

    response = api_client.put(url, {"deleted": False, "comment": "But we want more."})
    assert response.status_code == status.HTTP_200_OK

    assert not DealHull.objects.get(pk=pk).deleted
    assert DealHull.objects.get(pk=pk).deleted_comment == "But we want more."

    api_client.force_authenticate(user=superuser2)
    response = api_client.put(url, {"deleted": True, "comment": "And they agreed."})

    assert response.status_code == status.HTTP_200_OK
    assert DealHull.objects.get(pk=pk).deleted


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
    pk = deals[0].pk
    url = f"/api/deals/{pk}/toggle_confidential/"

    response = api_client.put(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    for user in [anybody2, reporter2, editor2]:
        api_client.force_authenticate(user=user)
        response = api_client.put(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    api_client.force_authenticate(user=admin2)
    response = api_client.put(url, {"confidential": True, "comment": "They bribed us."})
    assert response.status_code == status.HTTP_200_OK

    assert DealHull.objects.get(pk=pk).confidential
    assert DealHull.objects.get(pk=pk).confidential_comment == "They bribed us."

    response = api_client.put(
        url, {"confidential": False, "comment": "But we want more."}
    )
    assert response.status_code == status.HTTP_200_OK

    assert not DealHull.objects.get(pk=pk).confidential
    assert DealHull.objects.get(pk=pk).confidential_comment == "But we want more."

    api_client.force_authenticate(user=superuser2)
    response = api_client.put(
        url, {"confidential": True, "comment": "And they agreed."}
    )
    assert response.status_code == status.HTTP_200_OK
    assert DealHull.objects.get(pk=pk).confidential
