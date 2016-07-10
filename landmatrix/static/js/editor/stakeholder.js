/**
 * Created by riot on 13.04.16.
 */

var sankeydata = [];

function init_investor_form(form) {
    // Init buttons
    form.find('.add-form').click(function () {
        $(this).parents('.row').find('.formset-add-form').trigger('click');
    });
    form.find('.remove-form').click(function () {
        form.find('.formset-remove-form').trigger('click');
    });


    function formatInvestor (investor) {
        console.log(investor);
        return investor.text;
    }
    function formatInvestorSelection (investor) {
        console.log(investor);
        return investor.text;
    }

    form.find('select.investorfield').select2({
        ajax: {
            url: '/api/investors.json',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                console.log(params);
                return {
                    q: params.term
                };
            },
            processResults: function (data) {
                console.log(data);
                return {
                    results: data
                };
            },
            cache: true
        },
        escapeMarkup: function (markup) { return markup; },
        minimumInputLength: 3,
        templateResult: formatInvestor,
        templateSelection: formatInvestorSelection
    }).on('change', function () {
        generateButtons($(this));
        //    loadSankey(index, $(this).val());
    });
    generateButtons(form.find('select.investorfield'));

    form.find('.loans_amount input').attr('placeholder', 'Loans');
    form.find('.loans_date input').attr('placeholder', 'YYYY-MM-DD');
}

function generateButtons(field) {
    var investorId = field.val();
    console.log("Setting up buttons!");

    var buttons = '<a id="add_' + $(field).attr("id") + '" class="add-investor" href="/stakeholder/add/" class="noul"><i class="lm lm-plus"></i></a>';
    if (field.val() !== '') {
        buttons += '<a id="change_' + $(field).attr("id") + '" class="change-investor" href="/stakeholder/' + investorId + '/" class="noul"><i class="lm lm-pencil"></i></a>';
    }
    var wrap = '<span class="investorops">' + buttons + '</span>';

    field.parent().find('.investorops').remove();
    field.parent().append(wrap);
    //field.parent().parent().parent().append('<div id="chart' + index + '"></div>');

    // Bind handlers
    $('a.add-investor').click(function (e) {
      e.preventDefault()
      showAddInvestorPopup(this);
      return False;
    });
    $('a.change-investor').click(function (e) {
      e.preventDefault()
      showChangeInvestorPopup(this);
      return False;
    });

}

function addSankeyData(data, response, jqxhdr) {
    console.log(data, response, jqxhdr);

    var network = {nodes: data.nodes, links: data.links};
    console.log(network);
    sankeydata[data.index] = network;
    setupSankey(data.index);

}

function loadSankey(index, investorId) {
    if (investorId > 0) {
        console.log("Loading new Investornetwork diagram data");

        $.get(
            "/api/investor_network.json?operational_stakeholder=" + investorId + '&operational_stakeholder_diagram=' + index,
            addSankeyData
        );
    }
}

function setupSankey(index) {
    var data = sankeydata[index];
    if (typeof data === 'undefined') {
        return;
    }
    var margin = {top: 1, right: 1, bottom: 6, left: 1},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;


    var d3_lmcolors = [
        "#fc941f", "#b9d635", "#4bbb87", "#179961", "#7c9a61",
        "#c6c6c6", "#919191", "#ebebeb"
    ];


    function landmatrixInvestorColors() {
        return d3.scale.ordinal().range(d3_lmcolors);
    }

    var formatNumber = d3.format(",.0f"),
        format = function (d) {
            return formatNumber(d) + " %";
        },
        color = landmatrixInvestorColors();

    console.log("Appending d3 sankey chart for index ", index);

    var chart = $("#chart" + index).empty();

    var svg = d3.select("#chart" + index).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var sankey = d3.sankey()
        .nodeWidth(15)
        .nodePadding(10)
        .size([width, height]);

    var path = sankey.link();


    function setupData(data) {

        sankey
            .nodes(data.nodes)
            .links(data.links)
            .layout(32);

        var link = svg.append("g").selectAll(".link")
            .data(data.links)
            .enter().append("path")
            .attr("class", "link")
            .attr("d", path)
            .style("stroke-width", function (d) {
                return Math.max(1, d.dy);
            })
            .sort(function (a, b) {
                return b.dy - a.dy;
            });

        link.append("title")
            .text(function (d) {
                return d.source.name + " → " + d.target.name + "\n" + format(d.value);
            });

        var node = svg.append("g").selectAll(".node")
            .data(data.nodes)
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            })
            .call(d3.behavior.drag()
                .origin(function (d) {
                    return d;
                })
                .on("dragstart", function () {
                    this.parentNode.appendChild(this);
                })
                .on("drag", dragmove));

        node.append("rect")
            .attr("height", function (d) {
                return d.dy;
            })
            .attr("width", sankey.nodeWidth())
            .style("fill", function (d) {
                return d.color = color(d.name.replace(/ .*/, ""));
            })
            .style("stroke", function (d) {
                return d3.rgb(d.color).darker(0.5);
            })
            .style("stroke-width", 2)
            .append("title")
            .text(function (d) {
                return d.name + "\n" + format(d.value);
            });

        node.append("text")
            .attr("x", -6)
            .attr("y", function (d) {
                return d.dy / 2;
            })
            .attr("dy", ".35em")
            .attr("text-anchor", "end")
            .attr("transform", null)
            .text(function (d) {
                return d.name;
            })
            .filter(function (d) {
                return d.x < width / 2;
            })
            .attr("x", 6 + sankey.nodeWidth())
            .attr("text-anchor", "start");

        function dragmove(d) {
            d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
            sankey.relayout();
            link.attr("d", path);
        }
    }

    setupData(data);
}


$(document).ready(function () {
    // Erm, this should probably be called more locally. We'll see.
    $('.country select').select2();
    $('.parent-stakeholder-form').formset({
        prefix: 'parent-stakeholder-form',
        addText: '<i class="fa fa-plus"></i> {% trans "Add another" %}',
        addCssClass: 'formset-add-form hidden',
        deleteText: '<i class="fa fa-minus"></i> {% trans "Remove" %}',
        deleteCssClass: 'formset-remove-form hidden',
        added: function (row) {
            // Unselect selected options
            row.find("option:selected").removeAttr("selected");
            init_investor_form(row);
        }
    }).each(function () { init_investor_form($(this)); });
    $('.parent-investor-form').formset({
        prefix: 'parent-investor-form',
        addText: '<i class="fa fa-plus"></i> {% trans "Add another" %}',
        addCssClass: 'formset-add-form hidden',
        deleteText: '<i class="fa fa-minus"></i> {% trans "Remove" %}',
        deleteCssClass: 'formset-remove-form hidden',
        added: function (row) {
            // Unselect selected options
            row.find("option:selected").removeAttr("selected");
            init_investor_form(row);
        },
    }).each(function () { init_investor_form($(this)); });

    // Init operational company field (deal add/edit)
    $(".investorfield").each(function (index) {
        console.log("Initializing investorfield with select and sankey.");
        var investorId = $(this).val();
        $(this).select2({
            placeholder: 'Select Investor'
        });
        /*
         var investorId = $(this).val();
         $(this).select2({
         placeholder: 'Select Investor',
         ajax: {
         url: '/api/investors.json',
         cache: true
         }
         });
         */
        generateButtons($(this), index);
        $(this).on('change', function () {
            generateButtons($(this), index);
        //    loadSankey(index, $(this).val());
        });
        //loadSankey(index, investorId);
    });
});
