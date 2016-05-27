/**
 * Created by riot on 02.05.16.
 */

var datatype = 'size',
    dataSwitch;

var d3_lmcolors = [
    "#fc941f", "#b9d635", "#4bbb87", "#179961", "#7c9a61",
    "#c6c6c6", "#919191", "#ebebeb"
];


function LMColor() {
    return d3.scale.ordinal().range(d3_lmcolors);
}


function buildAreaChart() {
    var data1 = [{value: "42", label: "parturient montes", valueSuffix: " things"}, {
        value: "69",
        label: "id, mollis nec",
        valueSuffix: " things"
    }, {value: "29", label: "lacus. Ut", valueSuffix: " things"}, {
        value: "52",
        label: "a ultricies adipiscing",
        valueSuffix: " things"
    }];
    var config1 = rectangularAreaChartDefaultSettings();
    config1.colorsScale = LMColor();
    config1.maxValue = 100;

    loadRectangularAreaChart("AreaChart", data1, config1);
    /*
     var data2 = [{value: "78", label: "Duis", valuePrefix: "Area of "}, {
     value: "37",
     label: "Cras",
     valuePrefix: "Area of "
     }, {value: "55", label: "elit sed consequat", valuePrefix: "Area of "}];
     var config2 = rectangularAreaChartDefaultSettings();
     config2.colorsScale = d3.scale.ordinal().range(["#fc8d59", "#ffffbf", "#91bfdb"]); //palette from colorbrewer https://github.com/mbostock/d3/tree/master/lib/colorbrewer
     config2.textColorScale = d3.scale.ordinal().range(["#444", "#333", "#222"]);
     config2.labelAlignDiagonal = true;
     config2.valueTextAlignDiagonal = true;
     config2.valueTextPadding.right = 18;
     config2.animateDelay = 1000;
     config2.animateDelayBetweenBoxes = 0;
     config2.valueTextCountUp = false;
     loadRectangularAreaChart("rectangularareachart2", data2, config2);

     var data3 = [{value: "40", label: "massa. Quisque"}, {value: "34", label: "rhoncus. Proin nisl"}, {
     value: "45",
     label: "ipsum nunc"
     }, {value: "64", label: "pharetra"}, {value: "95", label: "parturient montes"}, {
     value: "87",
     label: "pede, ultrices"
     }, {value: "80", label: "nascetur"}];
     var config3 = rectangularAreaChartDefaultSettings();
     config3.expandFromLeft = false;
     config3.expandFromTop = true;
     config3.maxValue = 100;
     config3.colorsScale = d3.scale.ordinal().range(["#fff7fb", "#ece2f0", "#d0d1e6", "#a6bddb", "#67a9cf", "#3690c0", "#02818a", "#016c59", "#014636"]);  //palette from colorbrewer https://github.com/mbostock/d3/tree/master/lib/colorbrewer
     config3.textColorScale = d3.scale.ordinal().range(["#555", "#777", "#999", "#aaa", "#ddd", "#fff", "#fff"]);
     config3.animateDelay = 2000;
     loadRectangularAreaChart("rectangularareachart3", data3, config3);

     var data4 = [{value: "32", label: "consectetuer adipiscing"}, {value: "62", label: "ipsum"}];
     var config4 = rectangularAreaChartDefaultSettings();
     config4.expandFromLeft = true;
     config4.expandFromTop = true;
     config4.maxValue = 100;
     config4.labelAlignDiagonal = true;
     config4.animateDelay = 3500;
     config4.displayValueText = false;
     config4.animateDelayBetweenBoxes = 0;
     config4.colorsScale = d3.scale.ordinal().range(["#7570b3", "#e7298a", "#66a61e"]);  //palette from colorbrewer https://github.com/mbostock/d3/tree/master/lib/colorbrewer
     config4.textColorScale = d3.scale.ordinal().range(["#e7298a", "#7570b3", "#66a61e"]);
     loadRectangularAreaChart("rectangularareachart4", data4, config4);*/
}

function buildTreeChart() {

    var w = 1280 - 80,
        h = 800 - 180,
        x = d3.scale.linear().range([0, w]),
        y = d3.scale.linear().range([0, h]),
        color = LMColor(),
        root,
        node;

    var treemap = d3.layout.treemap()
        .round(false)
        .size([w, h])
        .sticky(true)
        .value(function (d) {
            return d.size;
        });

    var svg = d3.select("#TreeChart").append("div")
        .attr("class", "chart")
        .style("width", w + "px")
        .style("height", h + "px")
        .append("svg:svg")
        .attr("width", w)
        .attr("height", h)
        .append("svg:g")
        .attr("transform", "translate(.5,.5)");

    const TreeData = {
        "name": "",
        "children": [
            {
                "name": "Animals",
                "color": "#fc941f",
                "children": [
                    {"name": "Birds", "size": 3938},
                    {"name": "Apes", "size": 3812},
                    {"name": "Sheep", "size": 6714},
                    {"name": "Mules", "size": 743}
                ]
            },
            {
                "name": "Minerals",
                "color": "#4bbb87",
                "children": [
                    {"name": "Iron", "size": 17010},
                    {"name": "Aluminium", "size": 5842},
                    {"name": "Titanium", "size": 1041},
                    {"name": "Gold", "size": 5176}
                ]
            },
            {
                "name": "Crops",
                "color": "#b9d635",
                "children": [
                    {"name": "Salad", "size": 721},
                    {"name": "Carrots", "size": 4294},
                    {"name": "Peas", "size": 9800},
                    {"name": "Cabbage", "size": 1314},
                    {"name": "Radish", "size": 2220}
                ]
            }
        ]
    };

    d3.json("", function (data) {
        node = root = TreeData;

        var nodes = treemap.nodes(root)
            .filter(function (d) {
                return !d.children;
            });

        var cell = svg.selectAll("g")
            .data(nodes)
            .enter().append("svg:g")
            .attr("class", "cell")
            .attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            })
            .on("click", function (d) {
                return zoom(node == d.parent ? root : d.parent);
            });

        cell.append("svg:rect")
            .attr("width", function (d) {
                return d.dx - 1;
            })
            .attr("height", function (d) {
                return d.dy - 1;
            })
            .style("fill", function (d) {
                console.log("The colorbook says: ", d.parent.color);
                return color(d.parent.color);
            });

        cell.append("svg:text")
            .attr("x", function (d) {
                return d.dx / 2;
            })
            .attr("y", function (d) {
                return d.dy / 2;
            })
            .attr("dy", ".35em")
            .attr("text-anchor", "middle")
            .text(function (d) {
                return d.name;
            })
            .style("opacity", function (d) {
                d.w = this.getComputedTextLength();
                return d.dx > d.w ? 1 : 0;
            });

        d3.select(window).on("click", function () {
            zoom(root);
        });

        d3.select("select").on("change", function () {
            treemap.value(this.value == "size" ? size : count).nodes(root);
            zoom(node);
        });
    });

    function size(d) {
        return d.size;
    }

    function count(d) {
        return 1;
    }

    function zoom(d) {
        var kx = w / d.dx, ky = h / d.dy;
        x.domain([d.x, d.x + d.dx]);
        y.domain([d.y, d.y + d.dy]);

        var t = svg.selectAll("g.cell").transition()
            .duration(d3.event.altKey ? 7500 : 750)
            .attr("transform", function (d) {
                return "translate(" + x(d.x) + "," + y(d.y) + ")";
            });

        t.select("rect")
            .attr("width", function (d) {
                return kx * d.dx - 1;
            })
            .attr("height", function (d) {
                return ky * d.dy - 1;
            });

        t.select("text")
            .attr("x", function (d) {
                return kx * d.dx / 2;
            })
            .attr("y", function (d) {
                return ky * d.dy / 2;
            })
            .style("opacity", function (d) {
                return kx * d.dx > d.w ? 1 : 0;
            });

        node = d;
        d3.event.stopPropagation();
    }
}

function buildPieChart() {
    var data = [
        {label: 'On The Lease', value: 0.3},
        {label: 'Off The Lease', value: 0.35},
        {label: 'Pure Contract Farming', value: 0.1},
        {label: 'Both', value: 0.15},
        {label: 'None', value: 0.1}
    ];

    var w = 800,                        //width
        h = 500,                            //height
        r = 180;                            //radius
    color = LMColor();     //builtin range of colors

    $("#PieChart").empty();

    var vis = d3.select("#PieChart")
        .append("svg:svg")              //create the SVG element inside the <body>
        .data([data])                   //associate our data with the document
        .attr("width", w)           //set the width and height of our visualization (these will be attributes of the <svg> tag
        .attr("height", h)
        .append("svg:g")                //make a group to hold our pie chart
        .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");    //move the center of the pie chart from 0, 0 to radius, radius

    var arc = d3.svg.arc()              //this will create <path> elements for us using arc data
        .outerRadius(r);

    var pie = d3.layout.pie()           //this will create arc data for us given a list of values
        .value(function (d) {
            return d.value;
        });    //we must tell it out to access the value of each element in our data array

    var arcs = vis.selectAll("g.slice")     //this selects all <g> elements with class slice (there aren't any yet)
        .data(pie)                          //associate the generated pie data (an array of arcs, each having startAngle, endAngle and value properties)
        .enter()                            //this will create <g> elements for every "extra" data element that should be associated with a selection. The result is creating a <g> for every object in the data array
        .append("svg:g")                //create a group to hold each slice (we will have a <path> and a <text> element associated with each slice)
        .attr("class", "slice");    //allow us to style things in the slices (like text)

    arcs.append("svg:path")
        .attr("fill", function (d, i) {
            return color(i);
        }) //set the color for each slice to be chosen from the color function defined above
        .attr("d", arc);                                    //this creates the actual SVG path using the associated data (pie) with the arc drawing function

    arcs.append("svg:text")                                     //add a label to each slice
        .attr("transform", function (d) {                    //set the label's origin to the center of the arc
            //we have to make sure to set these before calling arc.centroid
            d.innerRadius = r;
            d.outerRadius = r + 20;
            return "translate(" + arc.centroid(d) + ")";        //this gives us a pair of coordinates like [50, 50]
        })
        .attr("text-anchor", "middle")                          //center the text on it's origin
        .text(function (d, i) {
            return data[i].label;
        });        //get the label from our original data array

    arcs.append("svg:text")                                     //add percentage to each label
        .attr("transform", function (d) {                    //set the label's origin to the center of the arc
            //we have to make sure to set these before calling arc.centroid
            d.innerRadius = r;
            d.outerRadius = r + 20;
            var coords = arc.centroid(d);
            coords[1] = coords[1] + 14;
            return "translate(" + coords + ")";        //this gives us a pair of coordinates like [50, 50]
        })
        .attr("text-anchor", "middle")                          //center the text on it's origin
        .text(function (d, i) {
            return "(" + data[i].value * 100 + "%)";
        });        //get the label from our original data array

}

function buildDotChart() {
    function truncate(str, maxLength, suffix) {
        if (str.length > maxLength) {
            str = str.substring(0, maxLength + 1);
            str = str.substring(0, Math.min(str.length, str.lastIndexOf(" ")));
            str = str + suffix;
        }
        return str;
    }

    $("#DotChart").empty();

    var margin = {top: 20, right: 200, bottom: 0, left: 20},
        width = 300,
        height = 650;

    var x_start = 0,
        x_end = 2;

    var c = LMColor(); //d3.scale.category20c();

    var x = d3.scale.linear()
        .domain([0, 2])
        .range([0, width]);

    var xlabels = d3.scale.quantize()
        .domain([0, 2])
        .range([0, width]);

    var xAxis = d3.svg.axis()
        .scale(xlabels)
        .orient("top");

    var svg = d3.select("#DotChart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .style("margin-left", margin.left + "px")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var dataset = [{
        "articles": [[2010, 6], [2011, 10], [2012, 11], [2013, 23], [2006, 1]],
        "total": 51,
        "name": "The Journal of neuroscience : the official journal of the Society for Neuroscience"
    }, {
        "articles": [[2008, 1], [2010, 3], [2011, 4], [2012, 17], [2013, 10]],
        "total": 35,
        "name": "Nature neuroscience"
    }, {
        "articles": [[2009, 1], [2010, 2], [2011, 8], [2012, 13], [2013, 11]],
        "total": 35,
        "name": "PloS one"
    }, {
        "articles": [[2007, 1], [2009, 3], [2010, 5], [2011, 7], [2012, 9], [2013, 9]],
        "total": 34,
        "name": "Nature"
    }, {
        "articles": [[2009, 2], [2010, 3], [2011, 4], [2012, 8], [2013, 9]],
        "total": 26,
        "name": "Neuron"
    }, {
        "articles": [[2009, 2], [2010, 2], [2011, 3], [2012, 9], [2013, 7]],
        "total": 23,
        "name": "Proceedings of the National Academy of Sciences of the United States of America"
    }, {
        "articles": [[2008, 1], [2010, 5], [2011, 10], [2012, 3], [2013, 3]],
        "total": 22,
        "name": "Nature methods"
    }, {
        "articles": [[2007, 1], [2009, 1], [2010, 3], [2011, 4], [2012, 4], [2013, 8]],
        "total": 21,
        "name": "Current opinion in neurobiology"
    }, {
        "articles": [[2006, 1], [2009, 3], [2010, 4], [2011, 1], [2012, 2], [2013, 7]],
        "total": 18,
        "name": "Science (New York, N.Y.)"
    }, {
        "articles": [[2010, 2], [2011, 4], [2012, 6], [2013, 4], [2007, 1]],
        "total": 17,
        "name": "Current biology : CB"
    }, {
        "articles": [[2010, 1], [2011, 3], [2012, 8], [2013, 3]],
        "total": 15,
        "name": "Journal of neurophysiology"
    }, {
        "articles": [[2009, 1], [2012, 4], [2013, 9]],
        "total": 14,
        "name": "Frontiers in neural circuits"
    }, {
        "articles": [[2012, 1], [2013, 13]],
        "total": 14,
        "name": "Brain research"
    }, {
        "articles": [[2009, 2], [2010, 1], [2011, 2], [2013, 8]],
        "total": 13,
        "name": "Frontiers in molecular neuroscience"
    }, {
        "articles": [[2008, 1], [2010, 2], [2011, 3], [2012, 3], [2013, 4]],
        "total": 13,
        "name": "The Journal of biological chemistry"
    }, {
        "articles": [[2009, 1], [2010, 1], [2011, 8], [2012, 2]],
        "total": 12,
        "name": "Conference proceedings : ... Annual International Conference of the IEEE Engineering in Medicine and Biology Society. IEEE Engineering in Medicine and Biology Society. Conference"
    }, {
        "articles": [[2012, 12]],
        "total": 12,
        "name": "Progress in brain research"
    }, {
        "articles": [[2009, 1], [2010, 1], [2012, 4], [2013, 6]],
        "total": 12,
        "name": "Journal of neuroscience methods"
    }, {
        "articles": [[2011, 3], [2012, 5], [2013, 3]],
        "total": 11,
        "name": "Journal of visualized experiments : JoVE"
    }, {
        "articles": [[2011, 1], [2012, 2], [2013, 8]],
        "total": 11,
        "name": "Neuroscience research"
    }, {
        "articles": [[2008, 1], [2010, 2], [2011, 5], [2012, 2]],
        "total": 10,
        "name": "Cell"
    }, {
        "articles": [[2012, 10]],
        "total": 10,
        "name": "Biological psychiatry"
    }, {
        "articles": [[2009, 1], [2011, 1], [2012, 5], [2013, 1]],
        "total": 8,
        "name": "The Journal of physiology"
    }, {
        "articles": [[2010, 2], [2012, 4], [2013, 1]],
        "total": 7,
        "name": "Nature protocols"
    }, {"articles": [[2013, 7]], "total": 7, "name": "Behavioural brain research"}, {
        "articles": [[2011, 5], [2013, 1]],
        "total": 6,
        "name": "Experimental physiology"
    }, {
        "articles": [[2011, 1], [2012, 1], [2013, 4]],
        "total": 6,
        "name": "Neuropharmacology"
    }, {
        "articles": [[2011, 1], [2012, 2], [2013, 2]],
        "total": 5,
        "name": "Neuroscience"
    }, {
        "articles": [[2011, 2], [2013, 3]],
        "total": 5,
        "name": "Nature communications"
    }, {"articles": [[2009, 1], [2010, 1], [2011, 1], [2012, 1], [2013, 1]], "total": 5, "name": "Neurosurgery"}];

    var dataset = [{
        "intentions": [[0, 10], [1, 6], [2, 4]],
        "total": 20,
        "name": "Agriculture"
    }, {
        "intentions": [[0, 5], [1, 6], [2, 1]],
        "total": 12,
        "name": "Forestry"
    }, {
        "intentions": [[0, 4], [1, 5], [2, 1]],
        "total": 10,
        "name": "Mining"
    }, {
        "intentions": [[0, 4], [1, 8], [2, 3]],
        "total": 15,
        "name": "Tourism"
    }];

    d3.json(dataset, function (data) {
        data = dataset;
        console.log("Data:", data);
        x.domain([x_start, x_end]);
        var xScale = d3.scale.linear()
            .domain([x_start, x_end])
            .range([0, width]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + 0 + ")")
            .call(xAxis);

        for (var j = 0; j < data.length; j++) {
            var g = svg.append("g").attr("class", "journal");


            console.log("Appending DotChartStuff");


            var circles = g.selectAll("circle")
                .data(data[j]['intentions'])
                .enter()
                .append("circle");

            var text = g.selectAll("text")
                .data(data[j]['intentions'])
                .enter()
                .append("text");

            var rScale = d3.scale.linear()
                .domain([0, d3.max(data[j]['intentions'], function (d) {
                    return d[1];
                })])
                .range([2, 9]);

            circles
                .attr("cx", function (d, i) {
                    return xScale(d[0]);
                })
                .attr("cy", j * 20 + 20)
                .attr("r", function (d) {
                    return rScale(d[1]);
                })
                .style("fill", function (d) {
                    return c(j);
                });

            text
                .attr("y", j * 20 + 25)
                .attr("x", function (d, i) {
                    return xScale(d[0]) - 5;
                })
                .attr("class", "value")
                .text(function (d) {
                    return d[1];
                })
                .style("fill", function (d) {
                    return c(j);
                })
                .style("display", "none");

            g.append("text")
                .attr("y", j * 20 + 25)
                .attr("x", width + 20)
                .attr("class", "label")
                .text(truncate(data[j]['name'], 30, "..."))
                .style("fill", function (d) {
                    return c(j);
                })
                .on("mouseover", mouseover)
                .on("mouseout", mouseout);
        }

        function mouseover(p) {
            var g = d3.select(this).node().parentNode;
            d3.select(g).selectAll("circle").style("display", "none");
            d3.select(g).selectAll("text.value").style("display", "block");
        }

        function mouseout(p) {
            var g = d3.select(this).node().parentNode;
            d3.select(g).selectAll("circle").style("display", "block");
            d3.select(g).selectAll("text.value").style("display", "none");
        }
    });
}

function buildBarChart() {
    var data = {
        labels: [
            'resilience', 'maintainability', 'accessibility',
            'uptime', 'functionality', 'impact'
        ],
        series: [
            {
                label: '2012',
                values: [4, 8, 15, 16, 23, 42]
            },
            {
                label: '2013',
                values: [12, 43, 22, 11, 73, 25]
            },
            {
                label: '2014',
                values: [31, 28, 14, 8, 15, 21]
            },]
    };

    var chartWidth = 300,
        barHeight = 20,
        groupHeight = barHeight * data.series.length,
        gapBetweenGroups = 10,
        spaceForLabels = 150,
        spaceForLegend = 150;

// Zip the series data together (first values, second values, etc.)
    var zippedData = [];
    for (var i = 0; i < data.labels.length; i++) {
        for (var j = 0; j < data.series.length; j++) {
            zippedData.push(data.series[j].values[i]);
        }
    }

// Color scale
    var color = d3.scale.category20();
    var chartHeight = barHeight * zippedData.length + gapBetweenGroups * data.labels.length;

    var x = d3.scale.linear()
        .domain([0, d3.max(zippedData)])
        .range([0, chartWidth]);

    var y = d3.scale.linear()
        .range([chartHeight + gapBetweenGroups, 0]);

    var yAxis = d3.svg.axis()
        .scale(y)
        .tickFormat('')
        .tickSize(0)
        .orient("left");

// Specify the chart area and dimensions
    var chart = d3.select("#BarChart")
        .attr("width", spaceForLabels + chartWidth + spaceForLegend)
        .attr("height", chartHeight);

// Create bars
    var bar = chart.selectAll("g")
        .data(zippedData)
        .enter().append("g")
        .attr("transform", function (d, i) {
            return "translate(" + spaceForLabels + "," + (i * barHeight + gapBetweenGroups * (0.5 + Math.floor(i / data.series.length))) + ")";
        });

// Create rectangles of the correct width
    bar.append("rect")
        .attr("fill", function (d, i) {
            return color(i % data.series.length);
        })
        .attr("class", "bar")
        .attr("width", x)
        .attr("height", barHeight - 1);

// Add text label in bar
    bar.append("text")
        .attr("x", function (d) {
            return x(d) - 3;
        })
        .attr("y", barHeight / 2)
        .attr("fill", "red")
        .attr("dy", ".35em")
        .text(function (d) {
            return d;
        });

// Draw labels
    bar.append("text")
        .attr("class", "label")
        .attr("x", function (d) {
            return -10;
        })
        .attr("y", groupHeight / 2)
        .attr("dy", ".35em")
        .text(function (d, i) {
            if (i % data.series.length === 0)
                return data.labels[Math.floor(i / data.series.length)];
            else
                return ""
        });

    chart.append("g")
        .attr("class", "y axis")
        .attr("transform", "translate(" + spaceForLabels + ", " + -gapBetweenGroups / 2 + ")")
        .call(yAxis);

// Draw legend
    var legendRectSize = 18,
        legendSpacing = 4;

    var legend = chart.selectAll('.legend')
        .data(data.series)
        .enter()
        .append('g')
        .attr('transform', function (d, i) {
            var height = legendRectSize + legendSpacing;
            var offset = -gapBetweenGroups / 2;
            var horz = spaceForLabels + chartWidth + 40 - legendRectSize;
            var vert = i * height - offset;
            return 'translate(' + horz + ',' + vert + ')';
        });

    legend.append('rect')
        .attr('width', legendRectSize)
        .attr('height', legendRectSize)
        .style('fill', function (d, i) {
            return color(i);
        })
        .style('stroke', function (d, i) {
            return color(i);
        });

    legend.append('text')
        .attr('class', 'legend')
        .attr('x', legendRectSize + legendSpacing)
        .attr('y', legendRectSize - legendSpacing)
        .text(function (d) {
            return d.label;
        });

}

function buildBiBarChart() {

    var randomNumbers = function () {
        var numbers = [];
        for (var i = 0; i < 20; i++) {
            numbers.push(parseInt(Math.random() * 19) + 1);
        }
        return numbers;
    };
    var randomNames = function () {
        var names = [];
        for (var i = 0; i < 20; i++) {
            names.push(String.fromCharCode(65 + Math.random() * 25) + String.fromCharCode(65 + Math.random() * 25) + String.fromCharCode(65 + Math.random() * 25));
        }
        return names;
    };
    var names = randomNames();
    var leftData = randomNumbers();
    var rightData = randomNumbers();
    for (var i = 0; i < names.length; i++) {
        console.log(names[i] + " from: " + leftData[i] + " to: " + rightData[i]);
    }
    var labelArea = 160;
    var width = 400,
        bar_height = 20,
        height = bar_height * (names.length);
    var rightOffset = width + labelArea;
    var chart = d3.select("#BiBarChart")
        .append('svg')
        .attr('class', 'chart')
        .attr('width', labelArea + width + width)
        .attr('height', height);

    var xFrom = d3.scale.linear()
        .domain([0, d3.max(leftData)])
        .range([0, width]);
    var y = d3.scale.ordinal()
        .domain(names)
        .rangeBands([10, height]);
    var yPosByIndex = function (d, index) {
        return y(index);
    }
    chart.selectAll("rect.left")
        .data(leftData)
        .enter().append("rect")
        .attr("x", function (pos) {
            return width - xFrom(pos);
        })
        .attr("y", yPosByIndex)
        .attr("class", "left")
        .attr("width", xFrom)
        .attr("height", y.rangeBand());
    chart.selectAll("text.leftscore")
        .data(leftData)
        .enter().append("text")
        .attr("x", function (d) {
            return width - xFrom(d);
        })
        .attr("y", function (d, z) {
            return y(z) + y.rangeBand() / 2;
        })
        .attr("dx", "20")
        .attr("dy", ".36em")
        .attr("text-anchor", "end")
        .attr('class', 'leftscore')
        .text(String);
    chart.selectAll("text.name")
        .data(names)
        .enter().append("text")
        .attr("x", (labelArea / 2) + width)
        .attr("y", function (d) {
            return y(d) + y.rangeBand() / 2;
        })
        .attr("dy", ".20em")
        .attr("text-anchor", "middle")
        .attr('class', 'name')
        .text(String);
    var xTo = d3.scale.linear()
        .domain([0, d3.max(rightData)])
        .range([0, width]);
    chart.selectAll("rect.right")
        .data(rightData)
        .enter().append("rect")
        .attr("x", rightOffset)
        .attr("y", yPosByIndex)
        .attr("class", "right")
        .attr("width", xTo)
        .attr("height", y.rangeBand());
    chart.selectAll("text.score")
        .data(rightData)
        .enter().append("text")
        .attr("x", function (d) {
            return xTo(d) + rightOffset;
        })
        .attr("y", function (d, z) {
            return y(z) + y.rangeBand() / 2;
        })
        .attr("dx", -5)
        .attr("dy", ".36em")
        .attr("text-anchor", "end")
        .attr('class', 'score')
        .text(String);
}

function buildAgriculturalPies() {
    RGraph.ObjectRegistry.Clear();
    var query_params = get_query_params(get_base_filter(), get_filter());
    var json_query = "/api/agricultural-produce.json" + query_params;
    jQuery.getJSON(json_query, function (data) {
        // show/hide data availability
        var sum = 0;
        $(data).each(function (i) {
            sum += data[i].available + data[i].not_available;
        });
        sum && $(".data-availability, .data").show() || $(".data-availability, .data").hide();

        var pie_data = [];
        for (var i = 0; i < data.length; i++) {
            pie_data = [];
            $('#pie-' + data[i]["region"]).parent().next().find('.food-crop').text(data[i]["agricultural_produce"]["food_crop"] + "%" + " (" + numberWithCommas(data[i]["hectares"]["food_crop"]) + " ha)");
            $('#pie-' + data[i]["region"]).parent().next().find('.non-food-crop').text(data[i]["agricultural_produce"]["non_food"] + "%" + " (" + numberWithCommas(data[i]["hectares"]["non_food"]) + " ha)");
            $('#pie-' + data[i]["region"]).parent().next().find('.flex-crop').text(data[i]["agricultural_produce"]["flex_crop"] + "%" + " (" + numberWithCommas(data[i]["hectares"]["flex_crop"]) + " ha)");
            $('#pie-' + data[i]["region"]).parent().next().find('.multiple-crop').text(data[i]["agricultural_produce"]["multiple_use"] + "%" + " (" + numberWithCommas(data[i]["hectares"]["multiple_use"]) + " ha)");
            var sum = data[i]["hectares"]["food_crop"] + data[i]["hectares"]["non_food"] + data[i]["hectares"]["flex_crop"] + data[i]["hectares"]["multiple_use"];
            $('#pie-' + data[i]["region"]).closest(".row").prev().find("h2 span").text("(" + numberWithCommas(sum) + " ha)");
            pie_data.push(data[i]["agricultural_produce"]["food_crop"]);
            pie_data.push(data[i]["agricultural_produce"]["non_food"]);
            pie_data.push(data[i]["agricultural_produce"]["flex_crop"]);
            pie_data.push(data[i]["agricultural_produce"]["multiple_use"]);

            var pie = new RGraph.Pie('pie-' + data[i]["region"], pie_data);
            pie.Set('chart.colors', ['#060c0f', '#225559', '#46b2bf', '#acd4dc']);
            pie.Set('chart.strokestyle', '#bbb');
            pie.Set('chart.text.font', 'Open Sans');
            pie.Set('chart.text.size', '9');
            if (data[i]["region"] == "overall") {
                pie.Set('chart.radius', 209);
                pie_data = []
                pie_data.push(data[i]["available"]);
                pie_data.push(data[i]["not_available"]);
                var pie2 = new RGraph.Pie('pie-availability', pie_data);
                pie2.Set('chart.colors', ['#1e1e1e', '#828282;']);
                pie2.Set('chart.radius', 15);
                pie2.Set('chart.strokestyle', '#bbb');
                pie2.Set('chart.text.font', 'Open Sans');
                pie2.Set('chart.text.size', '9');
                RGraph.Effects.Fade.In(pie2, {'duration': 250});
                var sum = data[i]["available"] + data[i]["not_available"],
                    available_per = parseInt(data[i]["available"] / sum * 100, 10),
                    not_available_per = parseInt(data[i]["not_available"] / sum * 100, 10);
                $("ul.legend:first li:first span").text(" (" + numberWithCommas(data[i]["available"]) + " hectares, " + available_per + "%)");
                $("ul.legend:first li:last span").text(" (" + numberWithCommas(data[i]["not_available"]) + " hectares, " + not_available_per + "%)");
            } else {
                pie.Set('chart.radius', 45);
            }
            RGraph.Effects.Fade.In(pie, {'duration': 250});
        }
    });
}