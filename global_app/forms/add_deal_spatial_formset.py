__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from .deal_spatial_form import DealSpatialForm, DealSpatialBaseFormSet


class AddDealSpatialFormSet(DealSpatialBaseFormSet):

    def get_taggroups(self, request=None):
        ds_taggroups = []
        for i, form in enumerate(self.forms):
            for j, taggroup in enumerate(form.get_taggroups()):
                taggroup["main_tag"]["value"] += "_" + str(i+1)
                ds_taggroups.append(taggroup)
        return ds_taggroups

    @classmethod
    def get_data(cls, activity):
        taggroups = activity.a_tag_group_set.filter(fk_a_tag__fk_a_value__value__contains="location").order_by("fk_a_tag__fk_a_value__value")
        data = []
        for i, taggroup in enumerate(taggroups):
            data.append(DealSpatialForm.get_data(activity, tg=taggroup))
        return data
