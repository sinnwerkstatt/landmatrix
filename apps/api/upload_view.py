import base64
import json
import os

from django.core.files.storage import DefaultStorage, FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.exceptions import PermissionDenied

storage: FileSystemStorage = DefaultStorage()  # type: ignore


def create_storage_layout(s: FileSystemStorage) -> None:
    for dir_name in ["uploads"]:
        dir_path = os.path.join(s.base_location, dir_name)
        if not os.path.isdir(dir_path):
            print(f"Creating storage folder '/{dir_name}'.")
            os.makedirs(dir_path)


create_storage_layout(storage)


@require_POST
def upload_datasource_file(request) -> JsonResponse:
    if not request.user.is_authenticated:
        raise PermissionDenied("MISSING_AUTHORIZATION")

    data = json.loads(request.body)

    _, payload = data["payload"].split(",")
    dec = base64.b64decode(payload)
    fname = storage.get_available_name(f"uploads/{data['filename']}")
    with open(os.path.join(storage.base_location, fname), "wb+") as f:
        f.write(dec)
    return JsonResponse({"name": fname})
