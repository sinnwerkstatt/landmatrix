import coreapi
import coreschema
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from django.views import View
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView

from apps.api.filters import Filter, PresetFilter
from apps.api.serializers import FilterPresetSerializer
from apps.grid.views.browse_filter_conditions import get_activity_field_label, get_investor_field_label
from apps.landmatrix.models.filter import FilterPreset as FilterPresetModel


class FilterDocTypeMixin(View):

    doc_type = ''

    def dispatch(self, request, *args, **kwargs):
        if 'doc_type' in kwargs:
            self.doc_type = kwargs.get('doc_type')
        return super().dispatch(request, *args, **kwargs)


class FilterCreateView(FilterDocTypeMixin,
                       APIView):
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
        return self.request.session.get('%s:filters' % self.doc_type, {})

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
            name = 'filter_%s' % get_random_string()

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
            except KeyError as err:  # pragma: no cover
                raise serializers.ValidationError(
                    {err.args[0]: _("This field is required.")})
            # Check for duplicates
            for filter_name, stored_filter in stored_filters.items():
                if (stored_filter.get('variable', '') == variable and
                   stored_filter.get('operator', '') == operator and
                   stored_filter.get('value', '') == value):
                    return Response(stored_filters)
            # Remove filters for same variable
            if request_data.get('replace_variable', ''):
                stored_filters = dict((k, v) for k, v in stored_filters.items() if v.get('variable') != variable)
            if self.doc_type == 'investor':
                label = get_investor_field_label(variable)
            else:
                label = get_activity_field_label(variable)
            new_filter = Filter(
                variable=variable, operator=operator, value=value,
                label=label, name=name, display_value=display_value)
        # print(stored_filters)
        stored_filters[new_filter.name] = new_filter
        # print(stored_filters)
        # Convert default filters to custom filters
        stored_filters = dict((k.replace('default_', ''), v)
                              for k, v in stored_filters.items())
        # Disable default filters
        request.session['%s:set_default_filters' % self.doc_type] = False
        request.session['%s:filters' % self.doc_type] = stored_filters

        return Response(stored_filters)


class FilterDeleteView(FilterDocTypeMixin,
                       APIView):
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
        return self.request.session.get('%s:filters' % self.doc_type, {})

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
            name = 'filter_%i' % (len(request.session.get('%s:filters' % self.doc_type, [])) + 1)


        try:
            del stored_filters[name]
            # Convert default filters to custom filters
            stored_filters = dict((k.replace('default_', ''), v)
                for k, v in stored_filters.items())
            # Disable default filters
            request.session['%s:set_default_filters' % self.doc_type] = False
        except KeyError:
            pass
        request.session['%s:filters' % self.doc_type] = stored_filters

        return Response(stored_filters)


class SetDefaultFiltersView(FilterDocTypeMixin,
                            APIView):
    """
    Set default filters for current session cookie.
    Used within the filter section of map, data and chart views.
    """

    def post(self, request, *args, **kwargs):
        if request.POST.get('set_default_filters', False):
            request.session['%s:filters' % self.doc_type] = {}
            request.session['%s:set_default_filters' % self.doc_type] = True
        else:
            request.session['%s:set_default_filters' % self.doc_type] = False

        return Response({})


class FilterListView(FilterDocTypeMixin,
                     APIView):
    """
    List filters in current session cookie.
    Used within the filter section of map, data and chart views.
    """

    def get_object(self):
        return self.request.session.get('%s:filters' % self.doc_type, {})

    def get(self, request, *args, **kwargs):
        """
        Show filters of current session cookie.
        Used within the filter section of map, data and chart views.
        """
        filters = self.get_object()
        return Response(filters)


class FilterClearView(FilterDocTypeMixin,
                      APIView):

    def get_object(self):
        return self.request.session.get('%s:filters' % self.doc_type, {})

    def get(self, request, *args, **kwargs):
        """
        Show filters of current session cookie.
        Used within the filter section of map, data and chart views.
        """
        request.session['%s:filters' % self.doc_type] = {}
        filters = self.get_object()
        return Response(filters)


class FilterPresetView(FilterDocTypeMixin,
                       ListAPIView):
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
