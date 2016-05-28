from django.utils.translation import ugettext as _
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from landmatrix.models.filter_preset import FilterPreset as FilterPresetModel
from api.filters import Filter, PresetFilter
from api.serializers import FilterPresetSerializer
from grid.views.save_deal_view import SaveDealView

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

        action = request_data.get('action', 'nothing')
        name = request_data.get('name', None)

        if action.lower() == 'set':
            if 'preset' in request_data:
                label = FilterPresetModel.objects.get(id=request_data['preset']).name
                new_filter = PresetFilter(request_data['preset'],
                    label=label, name=name)
            else:
                try:
                    label = ''
                    for form in SaveDealView.FORMS:
                        # FormSet (Spatial Data und Data source)
                        if hasattr(form, 'form'):
                            form = form.form
                        if request_data['variable'] in form.base_fields:
                            label = str(form.base_fields[request_data['variable']].label)
                            break
                    new_filter = Filter(variable=request_data['variable'],
                                        operator=request_data['operator'],
                                        value=request_data['value'],
                                        label=label,
                                        name=name)
                except KeyError as err:
                    raise serializers.ValidationError(
                        {err.args[0]: _("This field is required.")})

            stored_filters[new_filter.name] = new_filter
        elif action.lower() == 'remove':
            try:
                del stored_filters[name]
            except KeyError:
                pass

        request.session['filters'] = stored_filters

        return Response(stored_filters)

    def get(self, request, *args, **kwargs):
        if 'clear' in request.query_params:
            filters = {}
            request.session['filters'] = filters
        else:
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


class DashboardFilterView(APIView):

    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.session.get('dashboard_filters', {})

    def post(self, request, *args, **kwargs):
        '''
        TODO: use PATCH/DELETE here
        '''
        new_filters = {}

        request_data = request.query_params.copy()
        request_data.update(request.data)

        action = request_data.get('action', 'clear').lower()

        if action == 'set':
            if 'country' in request_data:
                new_filters['country'] = list(filter(lambda i: i, request_data.getlist('country')))
            elif 'region' in request_data:
                new_filters['region'] = list(filter(lambda i: i, request_data.getlist('region')))
            elif 'user' in request_data:
                new_filters['user'] = list(filter(lambda i: i, request_data.getlist('user')))

        self.request.session['dashboard_filters'] = new_filters

        return Response(new_filters)

    def get(self, request, *args, **kwargs):
        if 'clear' in request.query_params:
            filters = {}
            request.session['dashboard_filters'] = filters
        else:
            filters = self.get_object()

        return Response(filters)
