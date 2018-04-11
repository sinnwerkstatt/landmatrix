var rx,
    ry,
    m0,
    m0obj,
    rotate = 0;
var cluster,
    bundle,
    line,
    link,
    node,
    div,
    svg;


var splines = [];

function convertToSlug(Text) {
    return Text
        .toLowerCase()
        .replace(/[^\w ]+/g, '')
        .replace(/ +/g, '-')
        ;
}

function create_d3(diameter) {
    var radius = diameter / 2,
        innerRadius = radius - 120;

    var cluster = d3.layout.cluster()
        .size([360, innerRadius])
        .sort(null)
        .value(function (d) {
            return d.size;
        });

    var bundle = d3.layout.bundle();

    var line = d3.svg.line.radial()
        .interpolate("bundle")
        .tension(.85)
        .radius(function (d) {
            return d.y;
        })
        .angle(function (d) {
            return d.x / 180 * Math.PI;
        });

    div = d3.select("div.canvas");

    svg = div.append("svg")
        .attr("width", diameter)
        .attr("height", diameter)
        .append("g")
        .attr("transform", "translate(" + radius + "," + radius + ")");

    link = svg.append("g").selectAll(".link");
    node = svg.append("g").selectAll(".node");

    get_top_10();
    var query_params = "?deal_scope=transnational";
    var json_query = "/api/transnational_deals.json" + query_params;

    d3.json(json_query, function (error, classes) {
        if (error) {
            throw error;
        }

        var nodes = cluster.nodes(packageHierarchy(classes)),
            links = packageImports(nodes);

        link = link
            .data(bundle(links))
            .enter().append("path")
            .each(function (d) {
                d.source = d[0], d.target = d[d.length - 1];
            })
            .attr("class", function (d) {
                return "link source-" + d.source.id + " target-" + d.target.id;
            })
            .attr("d", line);

        node = node
            .data(nodes.filter(function (n) {
                return !n.children;
            }))
            .enter().append("text")
            .attr("class", "node")
            .attr("id", function (d) {
                return "node-" + d.id;
            })
            .attr("dy", ".31em")
            .attr("transform", function (d) {
                return "rotate(" + (d.x - 90) + ")translate(" + (d.y + 8) + ",0)" + (d.x < 180 ? ""
                        : "rotate(180)");
            })
            .style("text-anchor", function (d) {
                return d.x < 180 ? "start" : "end";
            })
            .text(function (d) {
                return d.key;
            })
            .on("mouseover", mouseovered)
            .on("mouseout", mouseouted)
            .on("mouseup", mouseup)
            .on("mousedown", mousedown)
            .on("mousemove", mousemove)
    });

    function mouseovered(d) {
        if (clicked) return;
        highlightCountry();
    }

    function mouseouted(d) {
        if (clicked) return;
        link
            .classed("link--target", false)
            .classed("link--source", false);

        node
            .classed("node--target", false)
            .classed("node--source", false);
    }

    d3.select(self.frameElement).style("height", diameter + "px");

    // Lazily construct the package hierarchy from class names.
    function packageHierarchy(classes) {
        var map = {};

        function find(name, data) {
            var node = map[name], i;
            if (!node) {
                node = map[name] = data || {name: name, children: []};
                if (name.length) {
                    node.parent = find(name.substring(0, i = name.lastIndexOf(".")));
                    node.parent.children.push(node);
                    node.key = name.substring(i + 1);
                }
            }
            return node;
        }

        classes.forEach(function (d) {
            find(d.name, d);
        });

        return map[""];
    }

    // Return a list of imports for the given array of nodes.
    function packageImports(nodes) {
        var map = {},
            imports = [];

        // Compute a map from name to node.
        nodes.forEach(function (d) {
            map[d.name] = d;
        });

        // For each import, construct a link from the source to target node.
        nodes.forEach(function (d) {
            if (d.imports) d.imports.forEach(function (i) {
                imports.push({source: map[d.name], target: map[i]});
            });
        });

        return imports;
    }
}

function init_canvas() {
    const diameter = Math.min($('#chartarea').width(), 1000);
    var width = height = diameter,
        center = diameter / 2;
    rx = center;
    ry = center;

    //var diameter = Math.min(width, height);

    var box = $(".chart-box");
    var boxwidth = diameter * 0.5,
        boxleft = chartwidth / 2 - boxwidth / 2,
        boxheight = diameter * 1 / 3,
        boxtop = diameter * 2 / 3;
    $("div.canvas").empty();
    $(".chart-box")
        .css("left", boxleft)
        .css("top", -boxtop)
        .css("height", boxheight)
        .css("width", boxwidth);

    create_d3(diameter);

    $('.show-all').on('click', deselectCountry);

    //cluster = d3.layout.cluster()
    //    .size([360, ry - 120])
    //    .sort(function(a, b) { return d3.ascending(a.key, b.key); });

    //bundle = d3.layout.bundle();

    /*line = d3.svg.line.radial()
     .interpolate("bundle")
     .tension(.85)
     .radius(function(d) { return d.y; })
     .angle(function(d) { return d.x / 180 * Math.PI; }); */

    // Chrome 15 bug: <http://code.google.com/p/chromium/issues/detail?id=98951>
    //div = d3.select("div.canvas");

    /*svg = div.append("svg:svg")
     .attr("width", width)
     .attr("height", height)
     .append("svg:g")
     .attr("transform", "translate(" + rx + "," + ry + ")");

     svg.append("svg:path")
     .attr("class", "arc")
     .attr("d", d3.svg.arc().outerRadius(ry - 120).innerRadius(0).startAngle(0).endAngle(2 * Math.PI))
     .on("mousedown", mousedown);*/
}

function draw_transnational_deals(callback, classes) {
    if (classes.length == 0) {
        callback();
        return;
    } else {
        $(".top-10-countries").show();
    }
    var nodes = cluster.nodes(packages.root(classes)),
        links = packages.imports(nodes),
        splines = bundle(links);

    var path = svg.selectAll("path.link")
        .data(links)
        .enter().append("svg:path")
        .attr("class", function (d) {
            return "link source-" + d.source.id + " target-" + d.target.id;
        })
        .attr("d", function (d, i) {
            return line(splines[i]);
        });
    svg.selectAll("g.node")
        .data(nodes.filter(function (n) {
            return !n.children;
        }))
        .enter().append("svg:g")
        .attr("class", "node")
        .attr("id", function (d) {
            return "node-" + d.id;
        })
        .attr("data-slug", function (d) {
            return d.slug;
        })
        .attr("transform", function (d) {
            return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")";
        })
        .append("svg:text")
        .attr("dx", function (d) {
            return d.x < 180 ? 8 : -8;
        })
        .attr("dy", ".31em")
        .attr("text-anchor", function (d) {
            return d.x < 180 ? "start" : "end";
        })
        .attr("transform", function (d) {
            return d.x < 180 ? null : "rotate(180)";
        })
        .text(function (d) {
            return d.key;
        })
        //.on("mouseover", mouseover)
        //.on("mouseout", mouseout);

    d3.select("input[type=range]").on("change", function () {
        line.tension(this.value / 100);
        path.attr("d", function (d, i) {
            return line(splines[i]);
        });
    });
    callback();
}

function mouse(e) {
    return [e.clientX, e.clientY];
}

function mousedown(d) {
    m0 = mouse(d3.event);
    m0obj = d;
    d3.event.preventDefault();
}

function mousemove() {
    if (m0) {
        var m1 = mouse(d3.event),
            dm = Math.atan2(cross(m0, m1), dot(m0, m1)) * 180 / Math.PI;
        div.style("-webkit-transform", "translate3d(0," + (ry - rx) + "px,0)rotate3d(0,0,0," + dm + "deg)translate3d(0," + (rx - ry) + "px,0)");
    }
}

function deselectCountry() {
    $(".show-all").addClass("disabled");
    $(".country-info").hide();

    link.classed("link--target", false)
        .classed("link--source", false)
        .style('display', 'block');

    node.classed("node--target", false)
        .classed("node--source", false)
        .each(function (n) {
            n.target = n.source = false;
        });
    $(".top-10-countries").show();
}

function mouseup(d) {
    if (m0) {
        var m1 = mouse(d3.event),
            dm = Math.atan2(cross(m0, m1), dot(m0, m1)) * 180 / Math.PI;
        rotate += dm;
        if (rotate > 360) rotate -= 360;
        else if (rotate < 0) rotate += 360;
        m0 = null;

        div.style("-webkit-transform", "rotate3d(0,0,0,0deg)");

        svg
            .attr("transform", "translate(" + rx + "," + ry + ")rotate(" + rotate + ")")
            .selectAll("g.node text")
            .attr("dx", function (d) {
                return (d.x + rotate) % 360 < 180 ? 8 : -8;
            })
            .attr("text-anchor", function (d) {
                return (d.x + rotate) % 360 < 180 ? "start" : "end";
            })
            .attr("transform", function (d) {
                return (d.x + rotate) % 360 < 180 ? null : "rotate(180)";
            });
    } else {
        // country clicked: show country info box
        var n;
        n = m0obj; // ('toElement' in d3.event && d3.event.toElement.parentElement) || (d3.event.relatedTarget && d3.event.relatedTarget.parentNode) || (d3.event.target.parentNode);
        var info = $(".country-info");
        info.hide();
        $(".top-10-countries").hide();
        $(".show-all").removeClass("disabled");
        if (n.id !== "" && parent) {
            info.find(".country").text(n.key);

            var jsonquery = "/api/transnational_deals_by_country.json?country=" + n.id;

            jQuery.getJSON(jsonquery, function (data) {
                var target_regions = "",
                    investor_regions = "",
                    r;
                if (data.investor_country.length > 1) {
                    var total_deals = 0,
                        total_hectares = 0;
                    for (var i = 0; i < data.investor_country.length; i++) {
                        r = data.investor_country[i];
                        target_regions += "<tr><th>" + r.region + "</th>";
                        target_regions += "<td style=\"text-align: right;\">";
                        target_regions += numberWithCommas(r.hectares) + " ha (";
                        target_regions += r.deals + " deals)</td></tr>";
                        total_deals += r.deals;
                        total_hectares += r.hectares;
                    }
                    target_regions += "<tr><th><strong>Total<strong></th>";
                    target_regions += "<th style=\"text-align: right;\"><strong>";
                    target_regions += numberWithCommas(total_hectares) + " ha (";
                    target_regions += total_deals + " deals)</strong></th></tr>";
                    info.find("a.inbound").attr("href", "/data/by-target-country/" + n.slug + "/");
                    info.find("table.inbound tbody").html(target_regions);
                    info.find(".inbound").show();
                } else {
                    info.find(".inbound").hide();
                }
                if (data.target_country.length > 1) {
                    var total_deals = 0,
                        total_hectares = 0;

                    for (var i = 0; i < data.target_country.length; i++) {
                        r = data.target_country[i];
                        investor_regions += "<tr><th>" + r.region + "</th>";
                        investor_regions += "<td style=\"text-align: right;\">";
                        investor_regions += numberWithCommas(r.hectares) + " ha (";
                        investor_regions += r.deals + " deals)</td></tr>";
                        total_deals += r.deals;
                        total_hectares += r.hectares;
                    }
                    investor_regions += "<tr><th><strong>Total<strong></th>";
                    investor_regions += "<th style=\"text-align: right;\"><strong>";
                    investor_regions += numberWithCommas(total_hectares) + " ha (";
                    investor_regions += total_deals + " deals)</strong></th></tr>";
                    info.find("a.outbound").attr("href", "/data/by-investor-country/" + n.slug + "/");
                    info.find("table.outbound tbody").html(investor_regions);
                    info.find(".outbound").show()
                } else {
                    info.find(".outbound").hide()
                }
                info.show();
            });

            // highlight pathes and nodes
            clicked = n.id;
            deselectCountry();
            mouseovered(n);
        }
    }
}

function updateNodes(name, value) {
    return function (d) {
        if (value) this.parentNode.appendChild(this);
        svg.select("#node-" + d[name].id).classed(name, value);
    };
}

function cross(a, b) {
    return a[0] * b[1] - a[1] * b[0];
}

function dot(a, b) {
    return a[0] * b[0] + a[1] * b[1];
}
