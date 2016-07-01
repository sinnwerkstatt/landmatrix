__author__ = 'Lene Preuss <lp@sinnwerkstatt.com>'

from django import forms


class PrimaryInvestorSelect(forms.Select):

    def render(self, name, value, attrs={}, choices=()):
        output = super(PrimaryInvestorSelect, self).render(name, value, attrs, choices)
        output += """
            <a class="btn change-investor" id="change_id_primary_investor" target="_blank" href='/browse/primary-investor/%(value)s/'><i class="icon-pencil"></i> Edit Primary-Investor</a>
            <a class="btn add-investor" id="add_id_primary_investor" target="_blank" href='/add/primary-investor/'><i class="icon-plus"></i> Add Primary-Investor</a>
            <script type="text/javascript">
            // Update change link href
            $(".%(name)s select").change(function () {
                var l = $(this).parent().find("a.change-investor");
                var v = $(this).find("option:selected").val();
                if (v != "") {
                  l.attr("href", l.attr("href").replace(/\d+/, v));
                }
            });
            // Handler for change link
            $("a.change-investor").click(function (e) {
              e.preventDefault();
              showChangeInvestorPopup(this);
              return false;
            });
            // Handler for add link
            $("a.add-investor").click(function (e) {
              e.preventDefault();
              showAddInvestorPopup(this);
              return false;
            });
            </script>
        """ % {
            "value": value and value or "0",
            "name": name
        }
        return output
