__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from global_app.forms.changedealwizard import *
from global_app.forms.adddealwizard import *
from global_app.forms import DealHistoryForm

class BrowseFilterConditions:

    DEBUG = False

    def __init__(self, formset, order_by=None, limit=None):
        if self.DEBUG:
            from pprint import pprint
            pprint(type(formset))
            pprint(vars(formset), width=100, compact=True)
        self.formset = formset
        self.order_by = order_by
        self.limit = limit

    def parse(self):
        self.data = {
            "activity": {},
            "deal_scope": "",
            "investor": {},
            "order_by": [],
            "limit": "",
        }
        self.read_formset()
        self.set_order_by()
        self.set_limit()

        return self.data


    def read_formset(self):
        filters_act, filters_inv = {"tags": {}}, {"tags": {}}
        if not self.formset:
            self.data["activity"] = filters_act
            self.data["investor"] = filters_inv
            return

        for i, form in enumerate(self.formset):
            fl, value = self.get_fl(form, i)
            variable = fl.get("variable")
            op = fl.get("operator")
            values = fl.get("value")
            year = fl.get("year")
            # skip if no variable is selected
            if not variable:
                continue
            # variable is identifier
            if variable == "-1":
                identifier_filter = filters_act.get("identifier", [])
                identifier_filter.append({
                    "value": values[0] or "0",
                    "op": op,
                })
                filters_act["identifier"] = identifier_filter
            elif variable == "-2":
                # deal scope
                if len(values) == 2:
                    self.data["deal_scope"] = "all"
                elif len(values) == 1:
                    self.data["deal_scope"] = values[0] == "10" and "domestic" or values[0] == "20" and "transnational" or ""
            elif "inv_" in variable:
                variable = variable[4:]
                f = get_field_by_sh_key_id(variable)
                values = [
                    year and "%s##!##%s" % (get_display_value_by_field(f, value), year) or get_display_value_by_field(f,
                                                                                                                      value)
                    for value in values]
                if f and "Region" in f.label:
                    # region values not stored at activity/investor
                    variable = "region"
                elif f and "Country" in f.label:
                    # countries are referred by keys
                    values = fl.get("value")
                filters_inv["tags"].update({"%s%s" % (variable, op and "__%s" % op or op): values})
            else:
                f = self.get_field_by_key(variable)
                if year:
                    values = ["%s##!##%s" % (get_display_value_by_field(f, value), year)]
                else:
                    values = [get_display_value_by_field(f, value) for value in values]
                if f:
                    if "Region" in f.label:
                        # region values not stored at activity/investor
                        variable = "region"
                    elif "Country" in f.label or "Crops" in f.label:
                        # countries and crops are referred by keys
                        values = fl.get("value")
                    elif "Negotiation status" in f.label:
                        variable = "pi_negotiation_status"
                filters_act["tags"].update({"%s%s" % (variable, op and "__%s" % op or op): values})

        self.data["activity"] = filters_act
        self.data["investor"] = filters_inv


    def get_fl(self, form, i):
        fl = {}
        for j, (n, f) in enumerate(form.fields.items()):
            key = "%s-%d-%s" % (self.formset.prefix, i, n)
            if n == "value":
                # is ybd field?
                if "%s_0" % key in self.formset.data:
                    # just take the first row of the field
                    value = self.formset.data.getlist("%s_0" % key)
                    year = self.formset.data.get("%s_1" % key)
                    fl.update({n: value, "year": year})
                else:
                    value = self.formset.data.getlist(key)
                    fl.update({n: value})
            else:
                value = self.formset.data.get(key)
                fl.update({n: value})
        return fl, value

    def set_order_by(self):
        if not self.order_by: return
        if not isinstance(self.order_by, list): self.order_by = [self.order_by]
        for field in self.order_by:
            field_pre = ""
            field_GET = ""
            if len(field) > 0 and field[0] == "-":
                field_pre = "-"
                field = field[1:]

            # TODO: fix
            # if "Investor " in field:
            #         form = get_field_by_sh_key_id(SH_Key.objects.get(key=field[9:]).id)
            # else:
            #         form = self.get_field_by_a_key_id(A_Key.objects.get(key=field).id)
            # if isinstance(form, IntegerField):
            #         field_GET = "+0"

            self.data["order_by"].append("%s%s%s" % (field_pre, field, field_GET))


    def set_limit(self):
        if self.limit:
            self.data["limit"] = self.limit


    def get_field_by_key(self, key):

        if key.isnumeric():
            key = get_key_from_id(int(key))

        for i, form in self.CHANGE_FORMS:
            form = hasattr(form, "form") and form.form or form
            if key in form.base_fields:
                return form().fields[key]
        return None

    CHANGE_FORMS = [
        ("spatial_data", ChangeDealSpatialFormSet),
        ("general_information", ChangeDealGeneralForm),
        ("employment", ChangeDealEmploymentForm),
        ("investor_info", DealSecondaryInvestorFormSet),
        ("data_sources", ChangeDealDataSourceFormSet),
        ("local_communities", DealLocalCommunitiesForm),
        ("former_use", DealFormerUseForm),
        ("produce_info", DealProduceInfoForm),
        ("water", DealWaterForm),
        ("gender-related_info", DealGenderRelatedInfoForm),
        ("overall_comment", ChangeDealOverallCommentForm),
        ("action_comment", ChangeDealActionCommentForm),
        ("history", DealHistoryForm),
        ('primary_investor', DealPrimaryInvestorForm)
    ]


def get_key_from_id(id):
    a_keys = {
        5234: 'agreement_duration',                     5261: 'animals',
        5297: 'annual_leasing_fee',                     5304: 'annual_leasing_fee_area',
        5298: 'annual_leasing_fee_currency',            5277: 'annual_leasing_fee_type',
        5243: 'community_benefits',                     5265: 'community_compensation',
        5260: 'community_consultation',                 5279: 'community_reaction',
        5239: 'company',                                5283: 'contract_date',
        5266: 'contract_farming',                       5301: 'contract_number',
        5264: 'contract_size',                          5248: 'crops',
        5259: 'date',                                   5237: 'domestic_jobs_created',
        5270: 'domestic_jobs_current',                  5307: 'domestic_jobs_current_daily_workers',
        5303: 'domestic_jobs_current_employees',        5254: 'domestic_jobs_planned',
        5306: 'domestic_jobs_planned_daily_workers',    5305: 'domestic_jobs_planned_employees',
        5271: 'domestic_use',                           5240: 'email',
        5281: 'export',                                 5263: 'export_country1',
        5299: 'export_country1_ratio',                  5268: 'export_country2',
        5300: 'export_country2_ratio',                  5269: 'export_country3',
        5278: 'file',                                   5235: 'foreign_jobs_created',
        5272: 'foreign_jobs_current',                   5310: 'foreign_jobs_current_employees',
        5236: 'foreign_jobs_planned',                   5309: 'foreign_jobs_planned_employees',
        5249: 'has_domestic_use',                       5262: 'has_export',
        5258: 'implementation_status',                  5242: 'includes_in_country_verified_information',
        5230: 'intended_size',                          5231: 'intention',
        5250: 'in_country_processing',                  5247: 'land_cover',
        5245: 'land_owner',                             5246: 'land_use',
        5226: 'level_of_accuracy',                      5227: 'location',
        5275: 'minerals',                               5225: 'name',
        5232: 'nature',                                 5233: 'negotiation_status',
        5253: 'not_public',                             5311: 'not_public_reason',
        5244: 'number_of_displaced_people',             5273: 'off_the_lease',
        5291: 'off_the_lease_area',                     5294: 'off_the_lease_farmers',
        5229: 'old_reliability_ranking',                5267: 'on_the_lease',
        5292: 'on_the_lease_area',                      5293: 'on_the_lease_farmers',
        5241: 'phone',                                  5256: 'point_lat',
        5257: 'point_lon',                              5282: 'production_size',
        5280: 'project_name',                           5289: 'purchase_price',
        5302: 'purchase_price_area',                    5290: 'purchase_price_currency',
        5276: 'purchase_price_type',                    5252: 'source_of_water_extraction',
        5228: 'target_country',                         5308: 'target_region',
        5284: 'total_jobs_created',                     5288: 'total_jobs_current',
        5296: 'total_jobs_current_daily_workers',       5295: 'total_jobs_current_employees',
        5285: 'total_jobs_planned',                     5287: 'total_jobs_planned_daily_workers',
        5286: 'total_jobs_planned_employees',           5238: 'type',
        5255: 'url',                                    5274: 'water_extraction_amount',
        5251: 'water_extraction_envisaged',
    }
    return a_keys[id]

def get_display_value_by_field(field, value):
    from django import forms
    choices_dict = {}
    if isinstance(field, forms.MultiValueField):
        field = field.fields[0]
    if isinstance(field, forms.ChoiceField):
        if isinstance(field, NestedMultipleChoiceField):
            for k, v, c in field.choices:
                if isinstance(c, (list, tuple)):
                    # This is an optgroup, so look inside the group for options
                    for k2, v2 in c:
                        choices_dict.update({k2:v2})
                choices_dict.update({k:v})
        else:
            choices_dict = dict(field.choices)
        # get displayed value/s?
        dvalue = None
        if isinstance(value, (list, tuple)):
            dvalue = []
            for v in value:
                dvalue.append(str(choices_dict.get(int(value))))
        else:
            dvalue = value and str(choices_dict.get(int(value)))
        return dvalue
    if isinstance(field, forms.BooleanField):
        dvalue = value == "on" and "True" or value == "off" and "False" or None
        return dvalue or value
    return value
