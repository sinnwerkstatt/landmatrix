from django.utils.translation import ugettext_lazy as _
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.schemas import ManualSchema
import coreapi
import coreschema

from landmatrix.models.filter_preset import FilterPreset as FilterPresetModel
from api.filters import Filter, PresetFilter
from api.serializers import FilterPresetSerializer
from grid.views.browse_filter_conditions import get_field_label


class FilterCreateView(GenericAPIView):
    """
    Add filter (or filter preset) to current session cookie.
    Used within the filter section of map, data and chart views.
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "name",
                required=False,
                location="data",
                description="Internal name (for referral)",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "preset",
                required=False,
                location="data",
                description="Preset ID of new preset",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "variable",
                required=False,
                location="data",
                description="Variable name of new filter (e.g. activity_identifier)",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "operator",
                required=False,
                location="data",
                description="Operator of new filter (lt, gt, lte, gte, is, is_empty, not_in, in OR contains)",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "value",
                required=False,
                location="data",
                description="Value of new filter",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "display_value",
                required=False,
                location="data",
                description="Display value of new filter",
                schema=coreschema.String(),
            ),
        ]
    )

    def get_object(self):
        return self.request.session.get('filters', {})

    def post(self, request, *args, **kwargs):
        # TODO: make this a PATCH, and more RESTful.
        # TODO: use a serializer for param parsing
        stored_filters = self.get_object()

        # TODO: This works, but it's not very standard DRF.
        # Maybe convert to using the POST body for args in future?
        request_data = request.query_params.copy()
        request_data.update(request.data)

        name = request_data.get('name', None)
        if not name:
            name = 'filter_%i' % (len(request.session.get('filters', [])) + 1)

        if 'preset' in request_data:
            # Check for duplicates
            for filter_name, stored_filter in stored_filters.items():
                if stored_filter.get('preset_id', '') == request_data['preset']:
                    return Response(stored_filters)
            new_filter = PresetFilter(request_data['preset'], name=name)
        else:
            try:
                variable = request_data['variable']
                operator = request_data['operator']
                value = request_data.getlist('value')
                if len(value) == 1:
                    value = value[0]
                display_value = request_data.get('display_value', None)
            except KeyError as err:
                raise serializers.ValidationError(
                    {err.args[0]: _("This field is required.")})
            # Check for duplicates
            for filter_name, stored_filter in stored_filters.items():
                if (stored_filter.get('variable', '') == variable and
                   stored_filter.get('operator', '') == operator and
                   stored_filter.get('value', '') == value):
                    return Response(stored_filters)
            label = get_field_label(variable)
            new_filter = Filter(
                variable=variable, operator=operator, value=value,
                label=label, name=name, display_value=display_value)
        stored_filters[new_filter.name] = new_filter
        request.session['filters'] = stored_filters

        return Response(stored_filters)


class FilterDeleteView(GenericAPIView):
    """
    Delete filter (or filter preset) from current session cookie.
    Used within the filter section of map, data and chart views.
    """
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "name",
                required=False,
                location="data",
                description="Internal name (for referral)",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "preset",
                required=False,
                location="data",
                description="Preset ID of new preset",
                schema=coreschema.Integer(),
            ),
            coreapi.Field(
                "variable",
                required=False,
                location="data",
                description="Variable name of new filter (e.g. activity_identifier)",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "operator",
                required=False,
                location="data",
                description="Operator of new filter (lt, gt, lte, gte, is, is_empty, not_in, in OR contains)",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "value",
                required=False,
                location="data",
                description="Value of new filter",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "display_value",
                required=False,
                location="data",
                description="Display value of new filter",
                schema=coreschema.String(),
            ),
        ]
    )

    def get_object(self):
        return self.request.session.get('filters', {})

    def post(self, request, *args, **kwargs):
        # TODO: make this a PATCH, and more RESTful.
        # TODO: use a serializer for param parsing
        stored_filters = self.get_object()

        # TODO: This works, but it's not very standard DRF.
        # Maybe convert to using the POST body for args in future?
        request_data = request.query_params.copy()
        request_data.update(request.data)

        name = request_data.get('name', None)
        if not name:
            name = 'filter_%i' % (len(request.session.get('filters', [])) + 1)


        try:
            del stored_filters[name]
            # Default filter?
            if 'default_preset' in name:
                # Convert default filters to custom filters
                stored_filters = dict((k.replace('default_', ''), v)
                    for k, v in stored_filters.items())
                # Disable default filters
                request.session['set_default_filters'] = False
        except KeyError:
            pass
        request.session['filters'] = stored_filters

        return Response(stored_filters)


class SetDefaultFiltersView(APIView):
    """
    Set default filters for current session cookie.
    Used within the filter section of map, data and chart views.
    """

    def get_object(self):
        return self.request.session.get('filters', {})

    def post(self, request, *args, **kwargs):
        if request.POST.get('set_default_filters', False):
            request.session['set_default_filters'] = True
        else:
            request.session['set_default_filters'] = False

        return Response({})


class FilterListView(GenericAPIView):
    """
    List filters in current session cookie.
    Used within the filter section of map, data and chart views.
    """

    def get_object(self):
        return self.request.session.get('filters', {})

    def get(self, request, *args, **kwargs):
        """
        Show filters of current session cookie.
        Used within the filter section of map, data and chart views.
        """
        filters = self.get_object()
        return Response(filters)


class FilterClearView(GenericAPIView):
    def get_object(self):
        return self.request.session.get('filters', {})

    def get(self, request, *args, **kwargs):
        """
        Show filters of current session cookie.
        Used within the filter section of map, data and chart views.
        """
        request.session['filters'] = {}
        filters = self.get_object()
        return Response(filters)


class FilterPresetView(ListAPIView):
    """
    The filter preset view returns a list of presets, filtered by group.
    If the show_groups query param is present, it instead returns a list of
    groups.
    """
    serializer_class = FilterPresetSerializer
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                "group",
                required=False,
                location="query",
                description="FilterPresetGroup ID",
                schema=coreschema.String(),
            ),
            coreapi.Field(
                "show_groups",
                required=False,
                location="query",
                description="Show groups if set",
                schema=coreschema.String(),
            ),
        ]
    )

    def get_queryset(self):
        queryset = FilterPresetModel.objects.all()
        group_name = self.request.query_params.get('group', None)
        if group_name and 'show_groups' not in self.request.query_params:
            queryset = queryset.filter(group=group_name)

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if 'show_groups' in request.query_params:
            groups = queryset.values_list('group', flat=True).distinct()
            response = Response(groups)
        else:
            serializer = self.get_serializer(queryset, many=True)
            response = Response(serializer.data)

        return response
