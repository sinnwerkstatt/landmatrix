import json

from ariadne.exceptions import HttpBadRequestError
from ariadne_django.views import GraphQLView

from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse


class GraphQLGETView(GraphQLView):
    @staticmethod
    def extract_data_from_get_request(request: HttpRequest):
        get_ret = request.GET.dict()
        get_ret["variables"] = json.loads(get_ret.get("variables", "null"))
        return get_ret

    def get(self, request, *args, **kwargs):
        # show GraphiQL if no GET-parameters are given
        if not request.GET:
            return super().get(request, *args, **kwargs)
        if not self.schema:
            raise ValueError("GraphQLView was initialized without schema.")
        try:
            data = self.extract_data_from_get_request(request)
        except HttpBadRequestError as error:
            return HttpResponseBadRequest(error.message)

        success, result = self.execute_query(request, data)
        status_code = 200 if success else 400
        return JsonResponse(result, status=status_code)
