__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms
from django.utils.safestring import mark_safe


class SelectAllCheckboxSelectMultiple(forms.CheckboxSelectMultiple):

    def render(self, name, value, attrs={}, choices=()):
        output = u"""
          <label for="select-all-%(id)s">
          <input type="checkbox" name="select-all-%(id)s" class="select" id="select-all-%(id)s">
           Select all
          </label>
          <script type="text/javascript">
            $("#select-all-%(id)s").click(function() {
            $(this).parents(".input-group").find("ul :checkbox").attr("checked", this.checked);
            });
            $(document).ready(function () {
                var checked = $("#select-all-%(id)s").parents(".input-group").find("ul :checked").length;
                var all = $("#select-all-%(id)s").parents(".input-group").find("ul :checkbox").length
                if (checked == all) {
                    $("#select-all-%(id)s").attr("checked", "checked");
                }
            });

          </script>
        """ % {
            "id": attrs.get("id"),
        }
        output += super(SelectAllCheckboxSelectMultiple, self).render(name, value, attrs)
        return mark_safe(output)
