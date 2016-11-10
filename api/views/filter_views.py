from django.utils.translation import ugettext as _
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from landmatrix.models.filter_preset import FilterPreset as FilterPresetModel
from grid.views.save_deal_view import SaveDealView
from api.filters import Filter, PresetFilter
from api.serializers import FilterPresetSerializer
from grid.views.view_aux_functions import get_field_label

__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'


class FilterView(APIView):

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

        action = request_data.get('action', 'nothing').lower()
        name = request_data.get('name', None)
        if not name:
            name = 'filter_%i' % (len(request.session.get('filters', [])) + 1)

        if action == 'set':
            if 'preset' in request_data:
                # Check for duplicates
                for filter_name, stored_filter in stored_filters.items():
                    if stored_filter['preset_id'] == request_data['preset']:
                        return Response(stored_filters)
                new_filter = PresetFilter(request_data['preset'], name=name)
            else:
                try:
                    variable = request_data['variable']
                    operator = request_data['operator']
                    value = request_data['value']
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
        elif action == 'remove':
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
        elif action == 'set_default_filters':
            request.session['set_default_filters'] = 'set_default_filters' in request_data
        request.session['filters'] = stored_filters

        return Response(stored_filters)

    def get(self, request, *args, **kwargs):
        if request.query_params.get('clear') == '1':
            request.session['filters'] = {}

        filters = self.get_object()
        return Response(filters)


class FilterPresetView(ListAPIView):
    '''
    The filter preset view returns a list of presets, filtered by group.
    If the show_groups query param is present, it instead returns a list of
    groups.
    '''
    serializer_class = FilterPresetSerializer

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
