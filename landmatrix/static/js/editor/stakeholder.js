function init_investor_form(form) {
    // Init buttons
    form.find('.add-form').click(function () {
        $(this).parents('.panel-body').find('.formset-add-form').trigger('click');
    });
    form.find('.remove-form').click(function () {
        form.find('.formset-remove-form').trigger('click');
    });


    function formatInvestor (investor) {
        return investor.text;
    }
    function formatInvestorSelection (investor) {
        return investor.text;
    }

    form.find('select.investorfield').select2({
        ajax: {
            url: '/api/investors.json',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return {
                    q: params.term
                };
            },
            processResults: function (data) {
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
        loadInvestorNetwork($(this).val());
    });
    generateButtons(form.find('select.investorfield'));

    form.find('.loans_date input').attr('placeholder', 'YYYY-MM-DD');
    form.find('.loans_currency select').select2();
}

function generateButtons(field) {
    var investorId = field.val();
    var addLink = '/stakeholder/add/';
    //var parentId = $('#id_id').val();
    //if (parentId) {
    //    addLink = addLink + '?parent_id=' + parentId;
    //}

    var buttons = '<a id="add_' + $(field).attr("id") + '" class="add-investor" href="' + addLink + '" class="noul"><i class="lm lm-plus"></i></a>';
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

function stakeholderAdded(row) {
    // Update form counters
    var form_count = 1;
    row.parent().find('h3 small').each(function () {
        $(this).text('#' + form_count++);
    });
    // Unselect selected options
    row.find("option:selected").removeAttr("selected");
    init_investor_form(row);
    // Scroll to the new row
    $('html, body').animate({
        scrollTop: row.offset().top
    }, 600);
}
function stakeholderRemoved(row) {
    // Update form counters
    var form_count = 1;
    row.parent().find('small').each(function () {
        $(this).text('#' + form_count++);
    });
}

$(document).ready(function () {
    // Erm, this should probably be called more locally. We'll see.
    $('.country select').select2();
            
    $('.parent-companies-form').formset({
        addText: '<i class="fa fa-plus"></i> {% trans "Add another" %}',
        addCssClass: 'formset-add-form hidden',
        deleteText: '<i class="fa fa-minus"></i> {% trans "Remove" %}',
        deleteCssClass: 'formset-remove-form hidden',
        prefix: 'parent-stakeholder-form',
        formCssClass: 'parent-companies-form',
        //extraClasses: ['dynamic-form'],
        added: stakeholderAdded,
        removed: stakeholderRemoved,
    }).each(function () { init_investor_form($(this)); });
    $('.parent-investors-form').formset({
        addText: '<i class="fa fa-plus"></i> {% trans "Add another" %}',
        addCssClass: 'formset-add-form hidden',
        deleteText: '<i class="fa fa-minus"></i> {% trans "Remove" %}',
        deleteCssClass: 'formset-remove-form hidden',
        prefix: 'parent-investor-form',
        formCssClass: 'parent-investors-form',
        //extraClasses: ['dynamic-form'],
        added: stakeholderAdded,
        removed: stakeholderRemoved,
    }).each(function () { init_investor_form($(this)); });


    // Init operational company field (deal add/edit)
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
        generateButtons($(this), index);
        $(this).on('change', function () {
            generateButtons($(this), index);
            loadInvestorNetwork($(this).val());
        });
        loadInvestorNetwork(investorId);
    });
});


// Dimensions of sunburst.
var width = 750;
var height = 600;
var radius = Math.min(width, height) / 2;

// Breadcrumb dimensions: width, height, spacing, width of tip/tail.
var b = {
  w: 75, h: 30, s: 3, t: 10
};

// Mapping of step names to colors.
var colors = {
  "home": "#5687d1",
  "product": "#7b615c",
  "search": "#de783b",
  "account": "#6ab975",
  "other": "#a173d1",
  "end": "#bbbbbb"
};

// Total size of all segments; we set this later, after loading the data.
var totalSize = 0; 

var vis = d3.select("#chart").append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .append("svg:g")
    .attr("id", "container")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var partition = d3.layout.partition()
    .size([2 * Math.PI, radius * radius])
    .value(function(d) { return d.size; });

var arc = d3.svg.arc()
    .startAngle(function(d) { return d.x; })
    .endAngle(function(d) { return d.x + d.dx; })
    .innerRadius(function(d) { return Math.sqrt(d.y); })
    .outerRadius(function(d) { return Math.sqrt(d.y + d.dy); });

function loadInvestorNetwork(investorId) {
    if (investorId <= 0) {
        return;
    }
    d3.json("/api/investor_network.json?operational_stakeholder=" + investorId,
        function (json) {
            json = buildHierarchy(json);
            createInvestorNetwork(json);
        }
    );
}

// Main function to draw and set up the visualization, once we have the data.
function createInvestorNetwork(json) {
    debugger;
  // Basic setup of page elements.
  initializeBreadcrumbTrail();
  drawLegend();
  d3.select("#togglelegend").on("click", toggleLegend);

  // Bounding circle underneath the sunburst, to make it easier to detect
  // when the mouse leaves the parent g.
  vis.append("svg:circle")
      .attr("r", radius)
      .style("opacity", 0);

  // For efficiency, filter nodes to keep only those large enough to see.
  var nodes = partition.nodes(json)
      .filter(function(d) {
      return (d.dx > 0.005); // 0.005 radians = 0.29 degrees
      });

  var path = vis.data([json]).selectAll("path")
      .data(nodes)
      .enter().append("svg:path")
      .attr("display", function(d) { return d.depth ? null : "none"; })
      .attr("d", arc)
      .attr("fill-rule", "evenodd")
      .style("fill", function(d) { return colors[d.name]; })
      .style("opacity", 1)
      .on("mouseover", mouseover);

  // Add the mouseleave handler to the bounding circle.
  d3.select("#container").on("mouseleave", mouseleave);

  // Get total size of the tree = value of root node from partition.
  totalSize = path.node().__data__.value;
 };

// Fade all but the current sequence, and show it in the breadcrumb trail.
function mouseover(d) {

  var percentage = (100 * d.value / totalSize).toPrecision(3);
  var percentageString = percentage + "%";
  if (percentage < 0.1) {
    percentageString = "< 0.1%";
  }

  d3.select("#percentage")
      .text(percentageString);

  d3.select("#explanation")
      .style("visibility", "");

  var sequenceArray = getAncestors(d);
  updateBreadcrumbs(sequenceArray, percentageString);

  // Fade all the segments.
  d3.selectAll("path")
      .style("opacity", 0.3);

  // Then highlight only those that are an ancestor of the current segment.
  vis.selectAll("path")
      .filter(function(node) {
                return (sequenceArray.indexOf(node) >= 0);
              })
      .style("opacity", 1);
}

// Restore everything to full opacity when moving off the visualization.
function mouseleave(d) {

  // Hide the breadcrumb trail
  d3.select("#trail")
      .style("visibility", "hidden");

  // Deactivate all segments during transition.
  d3.selectAll("path").on("mouseover", null);

  // Transition each segment to full opacity and then reactivate it.
  d3.selectAll("path")
      .transition()
      .duration(1000)
      .style("opacity", 1)
      .each("end", function() {
              d3.select(this).on("mouseover", mouseover);
            });

  d3.select("#explanation")
      .style("visibility", "hidden");
}

// Given a node in a partition layout, return an array of all of its ancestor
// nodes, highest first, but excluding the root.
function getAncestors(node) {
  var path = [];
  var current = node;
  while (current.parent) {
    path.unshift(current);
    current = current.parent;
  }
  return path;
}

function initializeBreadcrumbTrail() {
  // Add the svg area.
  var trail = d3.select("#sequence").append("svg:svg")
      .attr("width", width)
      .attr("height", 50)
      .attr("id", "trail");
  // Add the label at the end, for the percentage.
  trail.append("svg:text")
    .attr("id", "endlabel")
    .style("fill", "#000");
}

// Generate a string that describes the points of a breadcrumb polygon.
function breadcrumbPoints(d, i) {
  var points = [];
  points.push("0,0");
  points.push(b.w + ",0");
  points.push(b.w + b.t + "," + (b.h / 2));
  points.push(b.w + "," + b.h);
  points.push("0," + b.h);
  if (i > 0) { // Leftmost breadcrumb; don't include 6th vertex.
    points.push(b.t + "," + (b.h / 2));
  }
  return points.join(" ");
}

// Update the breadcrumb trail to show the current sequence and percentage.
function updateBreadcrumbs(nodeArray, percentageString) {

  // Data join; key function combines name and depth (= position in sequence).
  var g = d3.select("#trail")
      .selectAll("g")
      .data(nodeArray, function(d) { return d.name + d.depth; });

  // Add breadcrumb and label for entering nodes.
  var entering = g.enter().append("svg:g");

  entering.append("svg:polygon")
      .attr("points", breadcrumbPoints)
      .style("fill", function(d) { return colors[d.name]; });

  entering.append("svg:text")
      .attr("x", (b.w + b.t) / 2)
      .attr("y", b.h / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .text(function(d) { return d.name; });

  // Set position for entering and updating nodes.
  g.attr("transform", function(d, i) {
    return "translate(" + i * (b.w + b.s) + ", 0)";
  });

  // Remove exiting nodes.
  g.exit().remove();

  // Now move and update the percentage at the end.
  d3.select("#trail").select("#endlabel")
      .attr("x", (nodeArray.length + 0.5) * (b.w + b.s))
      .attr("y", b.h / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .text(percentageString);

  // Make the breadcrumb trail visible, if it's hidden.
  d3.select("#trail")
      .style("visibility", "");

}

function drawLegend() {

  // Dimensions of legend item: width, height, spacing, radius of rounded rect.
  var li = {
    w: 75, h: 30, s: 3, r: 3
  };

  var legend = d3.select("#legend").append("svg:svg")
      .attr("width", li.w)
      .attr("height", d3.keys(colors).length * (li.h + li.s));

  var g = legend.selectAll("g")
      .data(d3.entries(colors))
      .enter().append("svg:g")
      .attr("transform", function(d, i) {
              return "translate(0," + i * (li.h + li.s) + ")";
           });

  g.append("svg:rect")
      .attr("rx", li.r)
      .attr("ry", li.r)
      .attr("width", li.w)
      .attr("height", li.h)
      .style("fill", function(d) { return d.value; });

  g.append("svg:text")
      .attr("x", li.w / 2)
      .attr("y", li.h / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "middle")
      .text(function(d) { return d.key; });
}

function toggleLegend() {
  var legend = d3.select("#legend");
  if (legend.style("visibility") == "hidden") {
    legend.style("visibility", "");
  } else {
    legend.style("visibility", "hidden");
  }
}

function buildHierarchy(data, parent) {
  var root = {"name": "root", "children": []};
  for (var i = 0; i < data.length; i++) {
    var item = data[i];
    var parts = sequence.split("-");
    var currentNode = root;
    for (var j = 0; j < parts.length; j++) {
      var children = currentNode["children"];
      var nodeName = parts[j];
      var childNode;
      if (j + 1 < parts.length) {
   // Not yet at the end of the sequence; move down the tree.
    var foundChild = false;
    for (var k = 0; k < children.length; k++) {
      if (children[k]["name"] == nodeName) {
        childNode = children[k];
        foundChild = true;
        break;
      }
    }
  // If we don't already have a child node for this branch, create it.
    if (!foundChild) {
      childNode = {"name": nodeName, "children": []};
      children.push(childNode);
    }
    currentNode = childNode;
      } else {
    // Reached the end of the sequence; create a leaf node.
    childNode = {"name": nodeName, "size": size};
    children.push(childNode);
      }
    }
  }
  return root;
};

