// Handles related-objects functionality: lookup link for raw_id_fields
// and Add Another links.

function html_unescape(text) {
    // Unescape a string that was escaped using django.utils.html.escape.
    text = text.replace(/&lt;/g, '<');
    text = text.replace(/&gt;/g, '>');
    text = text.replace(/&quot;/g, '"');
    text = text.replace(/&#39;/g, "'");
    text = text.replace(/&amp;/g, '&');
    return text;
}

// IE doesn't accept periods or dashes in the window name, but the element IDs
// we use to generate popup window names may contain them, therefore we map them
// to allowed characters in a reversible way so that we can locate the correct
// element when the popup window is dismissed.
function id_to_windowname(text) {
    text = text.replace(/\./g, '__dot__');
    text = text.replace(/\-/g, '__dash__');
    return text;
}

function windowname_to_id(text) {
    text = text.replace(/__dot__/g, '.');
    text = text.replace(/__dash__/g, '-');
    return text;
}

function showAddInvestorPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^add_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href;
    if (href.indexOf('?') == -1) {
        href += '?popup=1';
    } else {
        href += '&popup=1';
    }
    var win = window.open(href, name);
    win.focus();
    return false;
}

function dismissAddInvestorPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = $("#" + name);

    if (elem) {
        if (elem[0].nodeName == 'SELECT') {
            elem.append($('<option></option>').val(newId).html(newRepr));
            elem.val(newId);
            // update list of secondary investors
            $.get("/ajax/widget/values", {key_id:  "secondary_investor", name: "investor", time: $.now() }, function (data) {
              $("ul.form.empty .field.investor div").html(data);
              $(elem).change(); // trigger change
            });
        }
    } else {
        console.log("Could not get input id for win " + name);
    }

    win.close();
}

function showChangeInvestorPopup(triggeringLink) {
    var name = triggeringLink.id.replace(/^change_/, '');
    name = id_to_windowname(name);
    href = triggeringLink.href;
    if (href.indexOf('?') == -1) {
        href += '?popup=1';
    } else {
        href  += '&popup=1';
    }
    var win = window.open(href, name);
    win.focus();
    return false;
}

function dismissChangeInvestorPopup(win, newId, newRepr) {
    // newId and newRepr are expected to have previously been escaped by
    newId = html_unescape(newId);
    newRepr = html_unescape(newRepr);
    var name = windowname_to_id(win.name);
    var elem = $("#" + name);

    if (elem) {
        if (elem[0].nodeName == 'SELECT') {
            $(elem).find("option[value=" + newId + "]").html(newRepr);
            // update list of secondary investors
            $.get("/ajax/widget/values", {key_id:  "secondary_investor", name: "investor", time: $.now() }, function (data) {
              $("ul.form.empty .field.investor div").html(data);
              $(elem).change(); // trigger change
            });
        }
    } else {
        console.log("Could not get input id for win " + name);
    }

    win.close();
}

function initializeDataSource(form) {
    form.find('.type select').change(function () {
        if ( ["Personal information", "Crowdsourcing"].indexOf($(this).val()) > -1){
            form.find(".name, .company, .email, .phone").slideDown("fast");
        } else {
            form.find(".name, .company, .email, .phone").slideUp("fast");
        }
        if (["Media report", "Research Paper / Policy Report", "Government sources", "Company sources", "Contract", "Contract (contract farming agreement)"].indexOf($(this).val()) > -1) {
            form.find(".publication_title").slideDown("fast");
        } else {
            form.find(".publication_title").slideUp("fast");
        }
        if ($(this).val() == "Contract") {
            form.find(".open_land_contracts_id").slideDown("fast");
        } else {
            form.find(".open_land_contracts_id").slideUp("fast");
        }
    }).change();
}
$(document).ready(function(){
    /* Overall: Enable checkboxes again on checking the parent input */
    $("input#id_intention_0,input#id_intention_1,input#id_source_of_water_extraction_1").click(function(){
        if($(this).is(":checked")) {
          $(this).parent().parent().children("ul").find("input:checkbox").prop("disabled",false);
        }
        else {
          $(this).parent().parent().children("ul").find("input:checkbox").prop("disabled",true).prop("checked",false);
        }
      });

    /* Overall: Deselecting radio buttons */
    $(":radio").click( function(e){
        var itsOn = $(this).hasClass("on");
        $(":radio[name="+ this.name + "]").removeClass("on");
        if(itsOn){
          $(this).removeAttr('checked');
          $(this).siblings().filter("[value='']").attr('checked', true);
        } else {
          $(this).addClass("on");
        }
      }).filter(":checked").addClass("on");

    /* Overall: Disable checkboxes on "change" pages */
    if($("input#id_intention_0, input#id_intention_1, input#id_source_of_water_extraction_1").is(":checked")) {
      $("input#id_intention_0:checked, input#id_intention_1:checked, input#id_source_of_water_extraction_1:checked").parent().parent().children("ul").find("input:checkbox").prop("disabled",false);
    }
    else {
      $("input#id_intention_0, input#id_intention_1, input#id_source_of_water_extraction_1").parent().parent().children("ul").find("input:checkbox").prop("disabled",true);
    }

    /* Spatial data: Initialize map */
    $(".form:visible .field.location .map").each(function (i) {
      initializeMap(this.id);
      init_google_maps($(this).prev("input"), i);
    });
    //$("#add-spatial-data").click(function () {
    //  var index = $(".spatial :input[name=spatial_data-TOTAL_FORMS]").val() - 1;
    //  initializeMap($(".form:visible .field.location .map").last()[0], index);
    //  init_google_maps($(".form:visible .field.location input").last(), index);
    //});
    /* Data sources: Hide fields if option not selected */
    //$("select[id*=data_sources]").each(function(){
    //  if ( $(this).find("option:eq(5), option:eq(6)").is(":selected") ){
    //  $(this).parents(".form").find("li.name, li.company, li.email, li.phone").show();
    //  } else {
    //    $(this).parents(".form").find("li.name, li.company, li.email, li.phone").hide();
    //  }
    //});
    /* Data sources: Show fields based on selection */
    $(".data_sources_form").each(function (form){
      initializeDataSource(form)
    });
    /* Data sources: Enable hide-show for new boxes */
    //$("a#add-data-source").click(function (){
    //  $("select[id*=data_sources]").change(function (){
    //    if ( $(this).find("option:eq(6), option:eq(5)").is(":selected") ){
    //      $(this).parents(".form").find("li.name, li.company, li.email, li.phone").slideDown("fast");
    //    }
    //    else {
    //      $(this).parents(".form").find("li.name, li.company, li.email, li.phone").slideUp("fast");
    //    }
    //  });
    //});

    /* General information: Leasing fees area only visible if "for specified area" is selected */
    $("div.annual_leasing_fee_area, div.purchase_price_area").css("display","none");
    $("select#id_purchase_price_type").change(function (){
      if ( $(this).find("option:eq(2)").is(":selected") ){
        $("div.purchase_price_area").slideDown("fast");
      }
      else {
        $("div.purchase_price_area").slideUp("fast");
        $("div.purchase_price_area div input").val("");
      }
    });
    $("select#id_annual_leasing_fee_type").change(function (){
      if ( $(this).find("option:eq(2)").is(":selected") ){
        $("div.annual_leasing_fee_area").slideDown("fast");
      }
      else {
        $("div.annual_leasing_fee_area").slideUp("fast");
        $("div.annual_leasing_fee_area div input").val("");
      }
    });

    /* General information: Contract farming everything invisible until "Yes" selected */
    if( !$("input#id_contract_farming_0").is(":checked") ){
      $("div.on_the_lease, div.off_the_lease, div.lease_type, div.on_the_lease_area, div.on_the_lease_farmers, div.on_the_lease_households, div.off_the_lease_area, div.off_the_lease_farmers, div.off_the_lease_households").css("display", "none");
    }
    $("input#id_contract_farming_0").click(function (){
      if ( $(this).is(":checked")){
        $("div.on_the_lease, div.off_the_lease, div.lease_type").slideDown("fast");
      }
      else {
        $("div.on_the_lease, div.off_the_lease, div.lease_type").slideUp("fast");
      }
    });
    $("input#id_contract_farming_1").click(function (){
      $("div.on_the_lease, div.off_the_lease, div.lease_type, div.on_the_lease_area, div.on_the_lease_farmers, div.on_the_lease_households, div.off_the_lease_area, div.off_the_lease_farmers, div.off_the_lease_households").slideUp("fast");
    });

    /* General information: Toggle On/Off the lease subfields */
    if( !$("input#id_on_the_lease").is(":checked") ){
      $("div.on_the_lease_area, div.on_the_lease_farmers, div.on_the_lease_households").css("display", "none");
    }
    $("input#id_on_the_lease").click(function (){
      if ( $(this).is(":checked")){
        $("div.on_the_lease_area, div.on_the_lease_farmers, div.on_the_lease_households").slideDown("fast");
      }
      else {
        $("div.on_the_lease_area, div.on_the_lease_farmers, div.on_the_lease_households").slideUp("fast");
      }
    });
    if( !$("input#id_off_the_lease").is(":checked") ){
      $("div.off_the_lease_area, div.off_the_lease_farmers, div.off_the_lease_households").css("display", "none");
    }
    $("input#id_off_the_lease").click(function (){
      if ( $(this).is(":checked")){
        $("div.off_the_lease_area, div.off_the_lease_farmers, div.off_the_lease_households").slideDown("fast");
      }
      else {
        $("div.off_the_lease_area, div.off_the_lease_farmers, div.off_the_lease_households").slideUp("fast");
      }
    });

    /* Employment: Toggle visibility of subfields on click*/
    if($("body").hasClass("public")) {
      if(!$('#id_total_jobs_created').is(":checked")) {
        $('#id_total_jobs_created').parent().parent().nextAll().slice(0,2).css("display","none");
      }
      if(!$('#id_foreign_jobs_created').is(":checked")) {
        $('#id_foreign_jobs_created').parent().parent().nextAll().slice(0,2).css("display","none");
      }
      if(!$('#id_domestic_jobs_created').is(":checked")) {
        $('#id_domestic_jobs_created').parent().parent().nextAll().slice(0,2).css("display","none");
      }
      $('#id_total_jobs_created, #id_foreign_jobs_created, #id_domestic_jobs_created').click(function() {
        $(this).parent().parent().nextAll().slice(0,2).slideToggle('fast');
      });
    } else {
      if(!$('#id_total_jobs_created').is(":checked")) {
        $('#id_total_jobs_created').parent().parent().nextAll().slice(0,7).css("display","none");
      }
      if(!$('#id_foreign_jobs_created').is(":checked")) {
        $('#id_foreign_jobs_created').parent().parent().nextAll().slice(0,7).css("display","none");
      }
      if(!$('#id_domestic_jobs_created').is(":checked")) {
        $('#id_domestic_jobs_created').parent().parent().nextAll().slice(0,7).css("display","none");
      }
      $('#id_total_jobs_created, #id_foreign_jobs_created, #id_domestic_jobs_created').click(function() {
        $(this).parent().parent().nextAll().slice(0,7).slideToggle('fast');
      });
    }

    /* Employment: Update totals */
    $('#id_total_jobs_planned_employees,#id_total_jobs_planned_daily_workers').change(function () {
      var field = $('#id_total_jobs_planned'),
          total = parseInt($('#id_total_jobs_planned_employees').val() || 0) + parseInt($('#id_total_jobs_planned_daily_workers').val() || 0);
      if (field.val() == '' || parseInt(field.val() || 0) < total) {
        field.val(total);
      }
    });
    $('#id_foreign_jobs_planned_employees,#id_foreign_jobs_planned_daily_workers').change(function () {
      var field = $('#id_foreign_jobs_planned'),
        total = parseInt($('#id_foreign_jobs_planned_employees').val() || 0) + parseInt($('#id_foreign_jobs_planned_daily_workers').val() || 0);
      if (field.val() == '' || parseInt(field.val() || 0) < total) {
        field.val(total);
      }
    });
    $('#id_domestic_jobs_planned_employees,#id_domestic_jobs_planned_daily_workers').change(function () {
      var field = $('#id_domestic_jobs_planned'),
        total = parseInt($('#id_domestic_jobs_planned_employees').val() || 0) + parseInt($('#id_domestic_jobs_planned_daily_workers').val() || 0);
      if (field.val() == '' || parseInt(field.val() || 0) < total) {
        field.val(total);
      }
    });

    /* Collapse existing investor fields on page load */
    $(".form.existing-investor:not(.empty) li.investor div ul li a:not(.selected-investor)").hide();

    /* submit form-wizard only once */
    $('.form-wizard button[type="submit"].btn-success, .form-wizard button[type="submit"].btn-danger').one("click", function(e) {
        e.preventDefault();
        $(this).click();
        $('.form-wizard button[type="submit"].btn-success, .form-wizard button[type="submit"].btn-danger').prop('disabled','disabled');
        return false;
    });

    $('#id_not_public').click(function(){
        if ($(this).is(":checked")) {
            $(".field.control-group.not_public_reason ").slideDown("fast");
        } else {
            $(".field.control-group.not_public_reason ").slideUp("fast");
        }
    });
    if ($('#id_not_public').is(':checked')) {
        $(".field.control-group.not_public_reason ").show();
    } else {
        $(".field.control-group.not_public_reason ").hide();
    }

    $('#id_assign_to_user').change(function() {
        if($(this).find("option:selected").val()){
            $(".field.control-group.tg_feedback_comment ").slideDown("fast");
        } else {
            $(".field.control-group.tg_feedback_comment ").slideUp("fast");
        }
    });
    if($('#id_assign_to_user option:selected').val()) {
        $(".field.control-group.tg_feedback_comment ").slideDown("fast");
    } else {
        $(".field.control-group.tg_feedback_comment ").slideUp("fast");
    }

    $('.crops select,.animals select,.minerals select,.contract_farming_crops select,.contract_farming_animals select,.assign_to_user select').select2();

    $('.negotiation_status select').change(function () {
      var val = $(this).find('option:selected').val();
      if (val == 70) {
        $('.sold_as_deal').show();
      } else {
        $('.sold_as_deal').hide();
      }
    }).change();

    // Prevent submit on enter
    $('form input').on('keyup keypress', function(e) {
      var keyCode = e.keyCode || e.which;
      if (keyCode === 13) { 
        e.preventDefault();
        return false;
      }
    });
});
