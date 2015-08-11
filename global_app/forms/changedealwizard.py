from django.utils.translation import ugettext_lazy as _

from global_app.forms import *
from global_app.forms.add_investor_form import AddInvestorForm


class ChangeDealOverallCommentForm(BaseForm):

    # Coordinators and reviewers overall comments
    tg_overall = TitleField(required=False, label="", initial=_("Overall comment"))
    tg_overall_comment = forms.CharField(required=False, label="", widget=CommentInput)

    @classmethod
    def get_data(cls, object, tg=None, prefix=""):
        data = super(ChangeDealOverallCommentForm, cls).get_data(object, tg, prefix)
        comments = Comment.objects.filter(fk_a_tag_group__fk_activity=object.id, fk_a_tag_group__fk_a_tag__fk_a_value__value="overall").order_by("-timestamp")
        if comments and len(comments) > 0:
            data["tg_overall_comment"] = comments[0].comment
        return data


class ChangeInvestorForm(AddInvestorForm):

    @classmethod
    def get_data(cls, object, tg=None, prefix=""):
        data = super(ChangeInvestorForm, cls).get_data(object, tg, prefix)
        return data
