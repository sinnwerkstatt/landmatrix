/**
 * Created by riot on 23.03.16.
 */

var currentVariable = "";

function updatePresets(json) {
    if (json === undefined || json.length === 0) {
        console.log("No presets.");
        return
    }

    presets = JSON.parse(json);
    console.log("These are the presets:", presets);
}

function updateFilters(json) {

    var label;
    var data;

    var tags = $("#filterlist");
    tags.empty();

    if (json === undefined || json.length === 0) {
        console.log("No filters.");
        label = '<label>No active filters</label>';
        tags.append(label);

        return
    } else {
        console.log("Json not empty");
        data = JSON.parse(json);
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
    }

    console.log("Filterdata:", data);
    var filternames = [];

    for (var item in data) {
        if ("preset_id" in data[item]) {
            var tag = data[item].name;
            var label = presets[data[item].preset_id];
            console.log("I have a preset in the filters: ", tag, label);
            var finalHtml = '<a class="delete-row" href="javascript:removeFilter(\'' + tag + '\')" title="'

            finalHtml = finalHtml + '">' + label + '<i class="lm lm-times"></i></a>';
            finalHtml = '<span class="label label-filter">' + finalHtml + '</span>';
        } else {
            var tag = data[item].variable[0];

            if (filternames.indexOf(tag) >= 0) {
                tag = data[item].variable[0] + " " + data[item].operator[0];
            }
            filternames.push(tag);
            var finalHtml = '<a class="delete-row" href="javascript:removeFilter(\'' + data[item].name + '\')" title="'
            var filterPopup = data[item].variable[0] + " " + data[item].operator[0] + " " + data[item].value[0];
            finalHtml = finalHtml + filterPopup + '">' + tag + '<i class="lm lm-times"></i></a>';
            finalHtml = '<span class="label label-filter">' + finalHtml + '</span>';
        }
        $(finalHtml).appendTo(tags);
        console.log("Tag appended.", tag, tags);
    }

    $("#filterrow form").hide()
}


function loadPreset(presetId) {
    $.post(
        "/api/filter.json?action=set&preset=" + presetId,
        updateFilters
    );
}

function removeFilter(filterName) {
    $.post(
        "/api/filter.json?action=remove&name=" + filterName,
        updateFilters
    );
}

function createFilter(variable) {
    $("#filterrow form").show()
    get_filter_options($("#filter_operator"), $("#filter_value"), variable);
    $('#filter_variable').val(variable);
    currentVariable = variable;

    $(".filter_active").removeClass('filter_active');
    $("#filter_" + variable).addClass('filter_active');
}


function get_filter_options(operatorfield, variablefield, key_id) {
    var name = variablefield.find(":input").attr("name"),
        op_value = operatorfield.val();

    const request = {key_id: key_id, value: "", name: 'value', operation: op_value};
    $.get("/ajax/widget/values", request, function (data) {
        //console.log('Got this from django:', data);
        variablefield.html(data);
        var is_number = (variablefield.find(":input[type=number]:not(.year-based-year)").length > 0);
        var is_list = (variablefield.find("select,ul").length > 0);
        var is_yearbased = (variablefield.find(".year-based").length > 0);

        //variablefield.find(":first").addClass("filtervalueheight");

        if (is_yearbased == true) {
            variablefield.find('a').each(function(index) {
                $(this).remove();
            });
            variablefield.find('.year-based-year').each(function(index) {
                $(this).remove();
            });
            var valuefield = variablefield.find("#id_value_0");
            valuefield.attr('id', 'id_value');
            valuefield.attr('name', 'value');
            valuefield.removeClass('year-based');
            valuefield.addClass('form-control');
        }

        operatorfield.find('option').each(function (index) {
            if (is_number) {
                var state = (jQuery.inArray($(this).val(), numeric_operators) == -1);
            } else if (is_list) {
                var state = (jQuery.inArray($(this).val(), list_operators) == -1);
            } else {
                var state = (jQuery.inArray($(this).val(), string_operators) == -1);
            }

            $(this).attr("disabled", state);
            if (state == true) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });

        if (operatorfield.find(':selected').attr('disabled')) {
            console.log("Old selected is invalid now - resetting");
            // TODO: This doesn't work
            operatorfield.find('option:first-child:not(hidden)').attr("selected", "selected");
        }
        
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

    // Get initial filter data for this session
    $.get(
        "/api/filter.json?action=list",
        updateFilters
    );

    /*$.get(
        "/api/filter_preset.json?action=list",
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
    $('.toggle-filters').click(function () {
        var text = $(this).data('toggle-text');
        $(this).data('toggle-text', $(this).text()).text(text);
    })


    $("form").submit(function (e) {
        e.preventDefault();
        var form = $(this);
        var data = form.serialize();
        console.log("Filter for transmit: ", data);

        $.post(
            '/api/filter.json?action=set&' + data,
            updateFilters
        );
    });

});