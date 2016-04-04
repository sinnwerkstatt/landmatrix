function openInvestorPopup(investorId) {
    if (typeof investorId === 'undefined') {
        investorId = 'add';
    }
    window.open("/en/stakeholder/" + investorId);
}

function generateButtons(field, index) {
    var investorId = field.val();

    field.on("change", function() {
        reloadSankey(index);
    });

    var buttons = '<a onClick="openInvestorPopup()" href="javascript:void(0);" class="noul"><i class="lm lm-plus"></i></a>';
    if (field.val() !== '') {
        buttons += '<a onClick="openInvestorPopup(' + investorId + ')" href="javascript:void(0);" class="noul"><i class="lm lm-pencil"></i></a>';
    }
    var wrap = '<span class="investorops">' + buttons + '</span>';

    field.parent().find('.investorops').remove();
    field.parent().append(wrap);
    field.parent().parent().parent().append('<div id="chart' + index + '"></div>');

}

function reloadSankey(index) {
    // TODO: This should grab the new Investor data from the api and feed it to the sankey d3
    console.log("New loading of sankey api data not implemented yet.")
}

function setupSankey(index) {
    return;
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
    var data = {
        "nodes": [
            {"name": "Investors"},
            {"name": "Stakeholders"},
            {"name": "Foo Corp"},
            {"name": "Bar Industries"},
            {"name": "Qux Ltd."},
            {"name": "Baz GmbH"}
        ],
        "links": [
            {"source": 0, "target": 2, "value": 50.0},
            {"source": 0, "target": 3, "value": 25.0},
            {"source": 0, "target": 5, "value": 25.0},
            {"source": 1, "target": 2, "value": 70.0},
            {"source": 1, "target": 3, "value": 10.0},
            {"source": 1, "target": 4, "value": 5.0}
        ]
    };

    //d3.json("apiurl", function (data) {
    function setupStatic() {
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
    }  // });
    setupStatic();
}


$(document).ready(function () {
        console.log('Deal Detail js loaded.');

        // TODO: Get Investor ID from Select and replace edit url


        $(".investorfield").each(function (index) {
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
            console.log('Investor:', investorId);

            generateButtons($(this), index);

            $(this).on('change', function () {
                generateButtons($(this), index);
                reloadSankey(index);
            });

            setupSankey(index);

        });
    });
