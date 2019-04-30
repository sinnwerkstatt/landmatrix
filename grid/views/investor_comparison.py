import datetime
from dateutil.tz import tzlocal

from django.core.exceptions import ObjectDoesNotExist
from django.forms.formsets import BaseFormSet
from django.views.generic.base import TemplateView

from grid.forms.investor_form import BaseInvestorForm
from grid.forms.parent_investor_formset import ParentCompanyFormSet, ParentInvestorFormSet
from landmatrix.models.investor import HistoricalInvestor


class InvestorComparisonView(TemplateView):

    template_name = 'grid/investor_comparison.html'

    def dispatch(self, request, **kwargs):
        investor_1 = kwargs.get('investor_1')
        investor_2 = kwargs.get('investor_2')

        hinvestor_1 = HistoricalInvestor.objects.get(pk=investor_1)
        if investor_2:
            hinvestor_2 = HistoricalInvestor.objects.get(pk=investor_2)
        else:
            hinvestor_2 = HistoricalInvestor.objects.filter(
                investor_identifier=hinvestor_1.investor_identifier) \
                .filter(history_date__lt=hinvestor_1.history_date).order_by('history_date').last()
        context = super().get_context_data()
        context['investors'] = [hinvestor_1, hinvestor_2]
        context['forms'] = get_comparison(hinvestor_1, hinvestor_2)

        return self.render_to_response(context=context)


def get_comparison(investor_1, investor_2):
    forms_1 = get_forms(investor_1)
    forms_2 = get_forms(investor_2)
    comparison_forms = []
    for i in range(len(forms_1)):
        comparison_forms.append((forms_1[i], forms_2[i], has_changed(forms_1[i], forms_2[i])))

    return comparison_forms


def get_forms(hinvestor):
    return [
        BaseInvestorForm(instance=hinvestor),
        ParentCompanyFormSet(queryset=hinvestor.venture_involvements.filter(role='ST')),
        ParentInvestorFormSet(queryset=hinvestor.venture_involvements.filter(role='IN')),
    ]


def has_changed(form_1, form_2):
    ignore_fields = ('id',)

    if form_1.is_valid() != form_2.is_valid():
        return False

    # OMG this is so hacky but I can't help myself
    # Formsets initialized with a list of forms throw a ValidationError:
    # 'ManagementForm data is missing or has been tampered with'
    # Formset initialized with a dict throw a KeyError in _construct_form
    # So I'm replacing _construct_form with my customized version that
    # catches the KeyError here.
    BaseFormSet._construct_form = _construct_form

    if isinstance(form_1, BaseFormSet):
        if len(form_1) != len(form_2):
            return False
        for i, subform_1 in enumerate(form_1.forms):
            subform_2 = form_2.forms[i]
            for j, field in enumerate(list(subform_1)):
                if field.name in ignore_fields:
                    continue
                if str(field) != str(list(subform_2)[j]):
                    return False
    else:
        for i, field in enumerate(list(form_1)):
            if str(field) != str(list(form_2)[i]):
                return False

    return True


# Hacked version of BaseFormSet._construct_form
def _construct_form(self, i, **kwargs):
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix(i),
            'error_class': self.error_class,
        }
        if self.is_bound:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial and 'initial' not in kwargs:
            try:
                defaults['initial'] = self.initial[i]
            # this is the line that has been changed!
            except (IndexError, KeyError):
                pass
        # Allow extra forms to be empty, unless they're part of
        # the minimum forms.
        if i >= self.initial_form_count() and i >= self.min_num:
            defaults['empty_permitted'] = True
        defaults.update(kwargs)
        form = self.form(**defaults)
        self.add_fields(form, i)
        return form


def investor_from_id(investor_id):
    try:
        if '_' in investor_id:
            return _investor_from_id_and_timestamp(investor_id)
        else:
            return HistoricalInvestor.objects.get(pk=investor_id)
    except ObjectDoesNotExist:
        return None


def _investor_from_id_and_timestamp(id_and_timestamp):
    if '_' not in id_and_timestamp:
        message = 'should contain _ separating investor id and timestamp: {}'.format(id_and_timestamp)
        raise ValueError(message)

    investor_id, timestamp = id_and_timestamp.split('_')

    investor = HistoricalInvestor.objects.get(pk=investor_id)

    history_date = datetime.datetime.fromtimestamp(
        float(timestamp), tz=tzlocal())
    old_version = investor.history.filter(
        history_date__lte=history_date).last()
    if old_version is None:
        raise ObjectDoesNotExist('Historical Investor %s as of timestamp %s' % (investor_id,
                                                                                timestamp))

    return old_version
