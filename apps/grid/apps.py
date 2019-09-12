from collections import OrderedDict

from django.apps import AppConfig


class GridConfig(AppConfig):
    name = 'apps.grid'
    verbose_name = "Grid"

    VARIABLES = None

    def ready(self):
        self.VARIABLES = self.get_variables()

    def get_variables(self):
        from apps.grid.views.deal import DealBaseView
        from apps.grid.fields import TitleField
        variables = OrderedDict()

        deal_forms = [
            form.form if hasattr(form, 'form') else form
            for form in DealBaseView.FORMS
        ]
        for form in deal_forms:
            for field_name, field in form.base_fields.items():
                if isinstance(field, TitleField):
                    continue
                variables[field_name] = field
        return variables
