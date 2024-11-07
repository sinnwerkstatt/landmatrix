from django.urls import reverse
from rest_framework import status

from apps.landmatrix.quality_indicators import DEAL_QIS, INVESTOR_QIS


# Don't know if this makes sense tbh
def test_permissions(api_client, anybody2, reporter2, editor2, admin2):
    for url in [
        reverse("qi-specs"),
        reverse("qi-deal-counts"),
        reverse("qi-investor-counts"),
        reverse("qi-deals"),
        reverse("qi-investors"),
    ]:
        for user in [anybody2]:
            api_client.force_authenticate(user=user)
            response = api_client.get(url)
            assert response.status_code == status.HTTP_403_FORBIDDEN

        for user in [reporter2, editor2, admin2]:
            api_client.force_authenticate(user=user)
            response = api_client.get(url)
            assert response.status_code != status.HTTP_403_FORBIDDEN


def test_specs_response(api_client, admin2):
    url = reverse("qi-specs")
    api_client.force_authenticate(user=admin2)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "deal" in response.data
    assert "investor" in response.data


def test_deals_response(api_client, admin2):
    url = reverse("qi-deals")
    api_client.force_authenticate(user=admin2)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content == b"Invalid qi"

    response = api_client.get(f"{url}?qi=invalid")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content == b"Invalid qi"

    response = api_client.get(f"{url}?qi={DEAL_QIS[0].key}")
    assert response.status_code == status.HTTP_200_OK
    assert type(response.data) == list


def test_investors_response(api_client, admin2):
    url = reverse("qi-investors")
    api_client.force_authenticate(user=admin2)

    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content == b"Invalid qi"

    response = api_client.get(f"{url}?qi=invalid")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content == b"Invalid qi"

    response = api_client.get(f"{url}?qi={INVESTOR_QIS[0].key}")
    assert response.status_code == status.HTTP_200_OK
    assert type(response.data) == list
