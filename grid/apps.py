from django.apps import AppConfig
from collections import OrderedDict


class GridConfig(AppConfig):
    name = 'grid'
    verbose_name = "Grid"

    VARIABLES = None

    def ready(self):
        self.VARIABLES = self.get_variables()

    def get_variables(self):
        from grid.views.save_deal_view import SaveDealView
        from grid.fields import TitleField
        variables = OrderedDict()

        deal_forms = [
            form.form if hasattr(form, 'form') else form
            for form in SaveDealView.FORMS
        ]
        for form in deal_forms:
            for field_name, field in form.base_fields.items():
                if isinstance(field, TitleField):
                    continue
                variables[field_name] = field
        return variables