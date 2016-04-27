var rx,
    ry,
    m0,
    rotate = 0;
var cluster,
    bundle,
    line,
    div,
    svg;



var splines = [];

function convertToSlug(Text) {
    return Text
        .toLowerCase()
        .replace(/[^\w ]+/g,'')
        .replace(/ +/g,'-')
        ;
}

function init_canvas(width, height) {
    width = typeof width !== 'undefined' ? width : 960;
    height = typeof height !== 'undefined' ? height : 960;
    rx = width / 2;
    ry = height / 2;
    $("div.canvas").empty();
    cluster = d3.layout.cluster()
        .size([360, ry - 120])
        .sort(function(a, b) { return d3.ascending(a.key, b.key); });

    bundle = d3.layout.bundle();

    line = d3.svg.line.radial()
        .interpolate("bundle")
        .tension(.85)
        .radius(function(d) { return d.y; })
        .angle(function(d) { return d.x / 180 * Math.PI; });

    // Chrome 15 bug: <http://code.google.com/p/chromium/issues/detail?id=98951>
    div = d3.select("div.canvas");

    svg = div.append("svg:svg")
        .attr("width", width)
        .attr("height", height)
      .append("svg:g")
        .attr("transform", "translate(" + rx + "," + ry + ")");

    svg.append("svg:path")
        .attr("class", "arc")
        .attr("d", d3.svg.arc().outerRadius(ry - 120).innerRadius(0).startAngle(0).endAngle(2 * Math.PI))
        .on("mousedown", mousedown);
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
        .attr("class", function(d) { return "link source-" + d.source.id + " target-" + d.target.id; })
        .attr("d", function(d, i) { return line(splines[i]); });
    svg.selectAll("g.node")
        .data(nodes.filter(function(n) { return !n.children; }))
      .enter().append("svg:g")
        .attr("class", "node")
        .attr("id", function(d) { return "node-" + d.id; })
        .attr("data-slug", function(d) { return d.slug; })
        .attr("transform", function(d) { return "rotate(" + (d.x - 90) + ")translate(" + d.y + ")"; })
      .append("svg:text")
        .attr("dx", function(d) { return d.x < 180 ? 8 : -8; })
        .attr("dy", ".31em")
        .attr("text-anchor", function(d) { return d.x < 180 ? "start" : "end"; })
        .attr("transform", function(d) { return d.x < 180 ? null : "rotate(180)"; })
        .text(function(d) { return d.key; })
        .on("mouseover", mouseover)
        .on("mouseout", mouseout);

    d3.select("input[type=range]").on("change", function() {
      line.tension(this.value / 100);
      path.attr("d", function(d, i) { return line(splines[i]); });
    });
    callback();
}

function mouse(e) {
  return [e.pageX - rx, e.pageY - ry];
}

function mousedown() {
  m0 = mouse(d3.event);
  d3.event.preventDefault();
}

function mousemove() {
  if (m0) {
    var m1 = mouse(d3.event),
        dm = Math.atan2(cross(m0, m1), dot(m0, m1)) * 180 / Math.PI;
    div.style("-webkit-transform", "translate3d(0," + (ry - rx) + "px,0)rotate3d(0,0,0," + dm + "deg)translate3d(0," + (rx - ry) + "px,0)");
  }
}

function mouseup() {
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
        .attr("dx", function(d) { return (d.x + rotate) % 360 < 180 ? 8 : -8; })
        .attr("text-anchor", function(d) { return (d.x + rotate) % 360 < 180 ? "start" : "end"; })
        .attr("transform", function(d) { return (d.x + rotate) % 360 < 180 ? null : "rotate(180)"; });
  } else {
      // country clicked: show country info box
      var n;
      n = ('toElement' in d3.event && d3.event.toElement.parentElement) || (d3.event.relatedTarget && d3.event.relatedTarget.parentNode) || (d3.event.target.parentNode);
      console.log('Hmm:', n);
      var info = $(".country-info");
      info.hide();
      $(".top-10-countries").hide();
      $(".show-all").removeClass("disabled");
      console.log("Country clicked, working..");
      if (n.id !== "" && parent) {
          console.log("Country selecting..");
          info.find(".country").text(n.textContent);
          // FIXME there should be a more elegent way
          if (typeof(get_query_params) == typeof(Function)) {
            var query_params = get_query_params(get_base_filter(), "country=" + n.id.replace("node-", ""));
          } else {
            var query_params = "?negotiation_status=concluded&deal_scope=transnational&country=" + n.id.replace("node-", "");
          }
          jQuery.getJSON("/api/transnational_deals_by_country.json" + query_params, function(data) {
              var target_regions = "",
                  r;
              if (data.investor_country.length > 1) {
                  for (var i = 0; i < data.investor_country.length; i++) {
                      r = data.investor_country[i];
                      if (data.investor_country.length == 2 && r.region == "Total") continue;
                      target_regions += "<tr><th>" + r.region + "</th><" + (r.region == "Total" && "th" || "td") + " style=\"text-align: right;\">" + numberWithCommas(r.hectares) + " ha (" + r.deals + " deals)</" + (r.region == "total" && "th" || "td") +  "></tr>";

                  }
                  info.find(".target-regions a.inbound").attr("href", "/get-the-detail/by-target-country/" + $(n).data("slug") + "/")
                  info.find(".target-regions").show().find("table").html(target_regions);
              } else {
                  info.find(".target-regions").hide();
              }
              if (data.target_country.length > 1) {
                  var investor_regions = "";
                  for (i = 0; i < data.target_country.length; i++) {
                      r = data.target_country[i];
                      if (data.target_country.length == 2 && r.region == "Total") continue;
                      investor_regions += "<tr><th>" + r.region + "</th><" + (r.region == "Total" && "th" || "td") + " style=\"text-align: right;\">" + numberWithCommas(r.hectares) + " ha (" + r.deals + " deals)</" + (r.region == "total" && "th" || "td") +  "></tr>";
                  }
                  info.find(".investor-regions a.outbound").attr("href", "/get-the-detail/by-investor-country/"  + $(n).data("slug") + "/")
                  info.find(".investor-regions").show().find("table").html(investor_regions);
              } else {
                  info.find(".investor-regions").hide();
              }
              info.show();
          });

  // highlight pathes
  var id = n.id.replace("node-", "");
  //console.log("path.link.source-" + id);
  //console.log( svg.selectAll("path.link.source-" + id));
  // deselect (as in mouseout)
  svg.select("#node-" + clicked).attr("class", "node");
  svg.selectAll("path.link.source-" + clicked)
      .classed("source", false)
      .each(updateNodes("target", false));

  svg.selectAll("path.link.target-" + clicked)
      .classed("target", false)
      .each(updateNodes("source", false));
  // select (as in mouseover)
  svg.select("#node-" + id).attr("class", "node active");
  svg.selectAll("path").style("display", "none")
  svg.selectAll("path.link.target-" + id)
      .classed("target", true)
      .each(updateNodes("source", true))
      .style("display", "block");

  svg.selectAll("path.link.source-" + id)
      .classed("source", true)
      .each(updateNodes("target", true))
      .style("display", "block");
      }
  }
  clicked = id;
}

function mouseover(d) {
  if (clicked) return;
  svg.selectAll("path.link.target-" + d.id)
      .classed("target", true)
      .each(updateNodes("source", true));

  svg.selectAll("path.link.source-" + d.id)
      .classed("source", true)
      .each(updateNodes("target", true));
}

function mouseout(d) {
  if (clicked) return;
  svg.selectAll("path.link.source-" + d.id)
      .classed("source", false)
      .each(updateNodes("target", false));

  svg.selectAll("path.link.target-" + d.id)
      .classed("target", false)
      .each(updateNodes("source", false));
}

function updateNodes(name, value) {
  return function(d) {
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
