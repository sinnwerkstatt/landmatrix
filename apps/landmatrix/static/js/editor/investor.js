$(document).ready(function () {
  var $overlay = $('img.loading').hide();
  if ($("#id_primary_investor").find("option:selected").val() == "") {
    $("a.change-investor").hide();
  }
  $('form ul.form.empty :input,form ul.form.empty label').each(function () {
    var id = $(this).attr("id");
    var name = $(this).attr("name");
    var value = $(this).attr("value");
    var for_str = $(this).attr("for");
    if (id) {
      $(this).attr("id", id.replace("id_investor_info-__prefix__-", ""));
    }
    if (name) {
      $(this).attr("name", name.replace("investor_info-__prefix__-", ""));
    }
    if (value) {
      $(this).attr("value", value.replace("investor_info-__prefix__-", ""));
    }
    if (for_str) {
      $(this).attr("for", for_str.replace("id_investor_info-__prefix__-", ""));
    }
  })
  $("form ul.form.empty").formset({
      prefix: 'investor_info',
      addText: '<i class="icon-plus"></i> {% trans "Add investor" %}',
      addCssClass: 'btn add-row',
      deleteText: '<i class="icon-remove"></i> {% trans "Remove investor" %}',
          deleteCssClass: 'btn delete-row',
      formTemplate: '.empty',
      added: function (row) {
        $(row).removeClass('empty').show();
        init_livesearch($(row).find("a.livesearch"));
      }
  });
  $(".add-row:not(.new-investor):not(.existing-investor)").addClass("trigger").hide();
  $(".add-row.existing-investor").click(function () {
    $(".add-row.trigger").click();
  })
  $(".add-row.new-investor").click(function () {
    $(".add-row.trigger").click();
    $("form ul.form:last").removeClass("existing-investor").addClass("new-investor");
    // deselecting radio buttons
    $("form ul.form:last :radio").click( function(e){
      var itsOn = $(this).hasClass("on");
      $(":radio[name="+ this.name + "]").removeClass("on");
      if(itsOn){
        $(this).removeAttr('checked');
        $(this).siblings().filter("[value='']").attr('checked', true);
      } else {
        $(this).addClass("on");
      }
    }).filter(":checked").addClass("on");
  })
  // Change primary investor
  $("#id_primary_investor").change(function () {
    // Load secondary investors
    var c_self = this;
    if ($(c_self).find("option:selected").val() != "") {
      $(".forms .form:not(.empty)").remove();
    }
    $overlay.show();
    var params;
    $("#id_investor_info-TOTAL_FORMS").val("0");
    $.get("/ajax/investor/", {primary_investor_id: $(c_self).val()}, function (data) {
      var investors = JSON.parse(data)["secondary_investors"];
      if (investors && investors.length > 0) {
          $("h3.secondary-investors").show();
          for (var i=0; i<investors.length; i++){
              // Create secondary investor
              $(".existing-investor").click();
              var inv_id = investors[i]["id"];
              $("#investor_info-"+i+"-tg_general_comment").val(investors[i]["groups"][0]["comment"]);
              // Select secondary investor
              $("li.investor div ul li a[href=#"+inv_id+"]:last").click();
              if ("investment_ratio" in investors[i]) {
                $("#investor_info-"+i+"-investment_ratio").val(investors[i]["investment_ratio"]);
              }
          }
      } else {
          $("h3.secondary-investors").hide();
          $(".forms .form:not(.empty)").remove();
      }
      // Hide/show add and remove buttons for secondary investors
      if ($(c_self).find("option:selected").val() == "") {
        $("#investors-add-links .add-row,.delete-row").show();
        $("a.change-investor").hide();
      } else {
        $("#investors-add-links .add-row,.delete-row").hide();
        $("a.change-investor").show();
      }
      $overlay.hide();

    });
  });
  // init existing secondary investors when page reloads
  $("ul.form.existing-investor:not(.empty)").each(function () {
    init_livesearch($(this).find("a.livesearch"));
  });
  if ($("ul.form.existing-investor:not(.empty)").length > 0) {
    $("h3.secondary-investors").show();
  };
});
