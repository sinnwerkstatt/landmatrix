/**
 * Created by riot on 23.03.16.
 */

var currentVariable = "";

//function updatePresets(json) {
//    if (json === undefined || json.length === 0) {
//        console.log("No presets.");
//        return
//    }
//
//    presets = JSON.parse(json);f
//    console.log("These are the presets:", presets);
//}

function updateFilters(data) {
    var label;

    var tags = $("#filterlist");
    tags.empty();

    if (data === undefined || data.length === 0) {
        console.log("No filters.");
        label = '<label>No active filters</label>';
        tags.append(label);

        return
    } else {
        try {
            if (Object.keys(data).length > 0) {
                console.log("Filters: ",data);
                label = '<label>Active Filters:</label>';
                tags.append(label);
            } else {
                console.log("No filters: ", data);
                label = '<label>No active filters</label>';
                tags.append(label);
                return
            }
        } catch(err) {
            console.log("Exception during filterjson evaluation: ", err, json);
        }

    }

    console.log("Filterdata:", data);
    var filternames = [];

    var title_prefix = 'Global';
    for (var item in data) {
        if ("preset_id" in data[item]) {
            if (data[item].hidden) {
                continue;
            }
            var tag = data[item].name,
                label = data[item].label,
                disabled = data[item].disabled && ' disabled' || '',
                finalHtml = '<a class="delete-row toggle-tooltip' + disabled + '" href="javascript:removeFilter(\'' + item + '\')" title="'

            finalHtml = finalHtml + '">' + label + '<i class="lm lm-times"></i></a>';
            finalHtml = '<span class="label label-filter">' + finalHtml + '</span>';
        } else {
            var tag = data[item].variable
                label = data[item].label;

            if (filternames.indexOf(tag) >= 0) {
                tag = data[item].variable + " " + data[item].operator;
            }
            filternames.push(tag);
            var finalHtml = '<a class="delete-row toggle-tooltip" href="javascript:removeFilter(\'' + item + '\')" title="'
            var filterPopup = data[item].label + " " + data[item].operator + " " + data[item].display_value;
            finalHtml = finalHtml + filterPopup + '">' + label + '<i class="lm lm-times"></i></a>';
            finalHtml = '<span class="label label-filter">' + finalHtml + '</span>';
            // Update title for target country/region
            if (tag == 'target_country' || tag == 'target_region') {
                title_prefix = data[item].display_value;
            }
        }
        $(finalHtml).appendTo(tags);
    }
    $('h1 span').text(title_prefix + ': ' + $('h1 span').text());
    $('#filters .toggle-tooltip:not(.left,.bottom)').tooltip({placement: "top", html: true});

    $("#filterrow .filtercontrolbox,#filterrow .filtervaluebox").hide()
}


function loadPreset(presetId, label) {
    $.post(
        "/api/filter/" + doc_type + "/add/",
        {preset: presetId},
        function () {
            window.location.reload();
        }
    );
}

function removeFilter(filterName) {
    $.post(
        "/api/filter/" + doc_type + "/delete/",
        {name: filterName},
        function () {
            // Check if querystring params contain removed filter
            var url = window.location.href.split("?");
            if (url[1] && url[1].indexOf(filterName) > -1) {
                window.location.replace(url[0]);
            } else {
                window.location.reload();
            }
        }
    );
}

function createFilter(variable, label) {
    $("#filterrow .filtercontrolbox,#filterrow .filtervaluebox").show();
    $("#filter_operator").val("is");
    get_filter_options($("#filter_operator"), $("#filter_value"), variable);
    $('#filter_variable').val(variable);
    currentVariable = variable;
    $('#filter_label').val(label);

    $(".filter_active").removeClass('filter_active');
    $("#filter_" + variable).addClass('filter_active');
}


function get_filter_options(operatorfield, variablefield, key_id) {
    var name = variablefield.find(":input").attr("name"),
        op_value = operatorfield.val();

    const request = {key_id: key_id, value: "", name: 'value', operation: op_value};
    $.get("/ajax/widget/" + doc_type + "/", request, function (data) {
        //console.log('Got this from django:', data);
        variablefield.html(data.widget);

        //if (is_yearbased == true) {
        //    variablefield.find('a').each(function(index) {
        //        $(this).remove();
        //    });
        //    variablefield.find('.year-based-year').each(function(index) {
        //        $(this).remove();
        //    });
        //    var valuefield = variablefield.find("#id_value_0");
        //    valuefield.attr('id', 'id_value');
        //    valuefield.attr('name', 'value');
        //    valuefield.removeClass('year-based');
        //    valuefield.addClass('form-control');
        //}

        operatorfield.find('option').each(function (index) {
            var state = (jQuery.inArray($(this).val(), data.allowed_operations) == -1);
            $(this).attr("disabled", state);
            if (state == true) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
        operatorfield.find('option:not([disabled=disabled])').first().attr('selected', 'selected');

        // Init investor widget
        variablefield.find('.investorfield').each(function () {
            initInvestorField($(this));
        });
        // Init country widget
        variablefield.find('.countryfield').each(function () {
            initCountryField($(this));
        });
    });
}

$(document).ready(function () {
    /*
     // add sticky header to table
     var offset = $('.navbar').height();
     //$("#summary").stickyTableHeaders({fixedOffset: offset});
     // enable popover for intention of investment
     $('a.intention-icon').popover({trigger: "hover", placement: "top"});
     init_form_condition($("ul.form:not(.empty) .field:first-child select"));
     */
    var filter_variable = $('#filter_variable').select2({
        placeholder: "Select a variable",
    }).on('change', function(e) {
        createFilter($(this).val(), $(this).find(':selected').text());
    });

    // Get initial filter data for this session
    $.get(
        "/api/filter/" + doc_type + "/",
        updateFilters
    );

    /*$.get(
        "/api/filter_preset/" + doc_type + "/?action=list",
        updatePresets
    );*/

    // Variable selected, update the widgets
    $('#filter_operator').change(function () {
        get_filter_options($("#filter_operator"), $("#filter_value"), currentVariable)
    });

    /* collapsible filters
     $(".toggle-filter").click(function (e) {
     e.preventDefault();
     $(".collapsible .collapsible-form").toggle();
     var container = $(".collapsible .collapsible-tags");

     if (container.hasClass("collapsed")) {
     container.removeClass("collapsed");
     container.find(".toggle-filter").text("Manage filters");
     container.find(".toggle-tooltip").show();
     } else {
     container.addClass("collapsed");
     container.find(".toggle-filter").text("Hide filters");
     container.find(".toggle-tooltip").hide();
     }
     return false;
     }).click();*/
    $('.toggle-text').click(function () {
        var html = $(this).data('toggle-text');
        if (html) {
            $(this).data('toggle-text', $(this).html()).html(html);
        }
    });


    $("#filterrow form,form#search").submit(function (e) {
        e.preventDefault();
        var data = $(this).serialize(),
            value = $(this).find('[name=value]');
        // display value (for select/radio/checkbox)
        if (value.is('select')) {
            data += '&display_value=' + value.find(':selected').text();
        } else if (value.is(':checkbox,:radio')) {
            data += '&display_value='
            value.filter(':checked').each(function (index, element) {
                if (index !== 0)
                    data += ' or ';
                data += $(element).parent().text().trim();
            });
        }
        $.post(
            "/api/filter/" + doc_type + "/add/",
            data,
            function () {
                window.location.reload();
            }
        );
    });

    $("#id_set_default_filters").click(function (e) {
        var data = $(this).closest('form').serialize();
        $.post(
            "/api/filter/" + doc_type + "/add/default/",
            data,
            function () {
                window.location.reload();
            }
        );
    });

    $("#id_columns,#id_status").select2();
    //    .on('change', function () { $(this).closest("form").find(':submit').show(); });
    
    var selectAllColumns = function (event) {
        event.preventDefault();
        $("#id_columns option").prop("selected", true);
        $("#id_columns").trigger("change");
    };
    var deselectAllColumns = function (event) {
        event.preventDefault();
        $("#id_columns option").prop("selected", false);
        $("#id_columns").trigger("change");
    };

    $("#id_columns").on("change", function(event) {
        event.preventDefault();
        var unselectedColumns = $("#id_columns option:not(:selected)");
        var selectLink = $("#select-all-columns");
        if (unselectedColumns.length) {
            selectLink.text("all columns").off("click").on("click", selectAllColumns);
        }
        else {
            selectLink.text("deselect all columns").off("click").on("click", deselectAllColumns);
        }
        return false;
    });
    $("#select-all-columns").click(selectAllColumns);

    var selectDefaultColumns = function (event) {
        event.preventDefault();
        $("#id_columns option").prop("selected", false);
        $("#id_columns option.default").prop("selected", true);
        $("#id_columns").trigger("change");
        return false;
    };
    $("#select-default-columns").click(selectDefaultColumns);

});