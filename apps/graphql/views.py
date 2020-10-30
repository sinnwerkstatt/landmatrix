import json

from ariadne.contrib.django.views import GraphQLView
from ariadne.exceptions import HttpBadRequestError
from django.http import HttpResponseBadRequest, JsonResponse, HttpRequest


class GraphQLGETView(GraphQLView):
    @staticmethod
    def extract_data_from_get_request(request: HttpRequest):
        get_ret = request.GET.dict()
        get_ret["variables"] = json.loads(get_ret.get("variables", {}))
        return get_ret

    def get(self, request, *args, **kwargs):
        if not self.schema:
            raise ValueError("GraphQLView was initialized without schema.")
        try:
            data = self.extract_data_from_get_request(request)
        except HttpBadRequestError as error:
            return HttpResponseBadRequest(error.message)

        success, result = self.execute_query(request, data)
        status_code = 200 if success else 400
        return JsonResponse(result, status=status_code)
