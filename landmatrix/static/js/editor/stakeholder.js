function initInvestorForm(form) {
    // Init buttons
    form.find('.add-form').click(function () {
        form.parents('.panel-body').find('.formset-add-form').trigger('click');
    });
    form.find('.remove-form').click(function () {
        form.find('.formset-remove-form').trigger('click');
    });
    initInvestorField(form.find(".investorfield"), function () {
        generateButtons($(this));
        loadInvestorNetwork($(this).val());
    });
}

function generateButtons(field) {
    var investorId = field.val(),
        investorIdentifier = field.select2('data')[0].investor_identifier,
        addLink = '/investor/add/',
        role = field.attr('name');
    if (investorIdentifier === undefined) {
        // Get initial investor identifier from data attribute
        investorIdentifier = $(field.select2('data')[0].element).data('investor-identifier');
    }
    if (role.indexOf('-') > -1) {
      role = role.split('-');
      role = role[0] + '_' + role[1];
    }
    //var parentId = $('#id_id').val();
    //if (parentId) {
    //    addLink = addLink + '?parent_id=' + parentId;
    //}

    var buttons = '<a id="add_' + $(field).attr("id") + '" class="add-investor" href="' + addLink + '?role=' + role + '" class="noul"><i class="lm lm-plus"></i></a>';
    if (field.val() !== '') {
        buttons += '<a id="change_' + $(field).attr("id") + '" class="change-investor"' +
            ' href="/investor/edit/' + investorIdentifier + '/' + investorId + '/?role=' + role +
            '" class="noul"><i class="lm lm-pencil"></i></a>';
    }
    var wrap = '<span class="investorops">' + buttons + '</span>';
    var parent = field.parent();
    parent.find('.investorops').remove();
    parent.append(wrap);
    //field.parent().parent().parent().append('<div id="chart' + index + '"></div>');

    // Bind handlers
    parent.find('a.add-investor').click(function (e) {
      e.preventDefault();
      showAddInvestorPopup(this);
      return false;
    });
    parent.find('a.change-investor').click(function (e) {
      e.preventDefault();
      showChangeInvestorPopup(this);
      return false;
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
    row.find(".select2").remove();
    row.find(".select2-hidden-accessible").removeClass("select2-hidden-accessible").data('select2', null);
    initInvestorForm(row);
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
    $('.fk_country select').each(function () {
        initCountryField($(this));
    });
});

var treeData = {};

var crossLinksData = [];

var updateReferences = function( data ) {

    var uniqueNodes = {},
        nodes = [ data ];

    while (node = nodes.pop()) {
        var children = {};
        if (Object.keys(node.stakeholders || {}).length > 0) {
            children = node.stakeholders;
        } else if (Object.keys(node._stakeholders || {}).length > 0) {
            children = node._stakeholders;
        }
        // Original?
        if (Object.keys(children).length > 0) {
            if (node.investor_identifier in uniqueNodes) {
                uniqueNodes[node.investor_identifier].original = node;
            } else {
                uniqueNodes[node.investor_identifier] = {
                    original: node,
                    duplicates: []
                };

                for (var investor_identifier in children) {
                  nodes.push(children[investor_identifier]);
                }
            }
        } else {
          // Duplicate
          if (node.investor_identifier in uniqueNodes) {
              uniqueNodes[node.investor_identifier].duplicates.push(node);
          } else {
            uniqueNodes[node.investor_identifier] = {
                original: undefined,
                duplicates: [node]
            };
          }
        }
    }

    for (var investor_identifier in uniqueNodes) {
        var node = uniqueNodes[investor_identifier],
            duplicate;
        if (!node.original) continue;
        for (var i = 0; i < node.duplicates.length; i++) {
            duplicate = node.duplicates[i];
            duplicate.found = "1";
            duplicate.stakeholders = node.original.stakeholders;
            duplicate._stakeholders = node.original._stakeholders;
        }
    }

    return data;
};

// Update children/links in tree
var getLinkedTreeData = function( curRoot, curCrossLinks ) {

    var nodesProcessed = {};

    function getLink( node, childNode, type ) {
        var found = false,
            link;
        // Find link
        for (var i = 0; i < curCrossLinks.length; i++) {
          link = curCrossLinks[i];
          if (link.source.investor_identifier === node.investor_identifier &&
              link.target.investor_identifier === childNode.investor_identifier) {
            // Link already existing? Done.
            found = true;
            break;
          }
        }
        if (!found) {
          // Link doesn't exist yet. Create link.
          link = {
            source: node,
            target: childNode,
            type: type
          }
        }
        return link;
    }

    function getChild( investor_identifier, children ) {
        if (!children) return;

        // Find child
        var child;
        for (var i = 0; i < children.length; i++) {
          child = children[i];
          if (child.investor_identifier === investor_identifier) {
            break;
          }
        }

        return child;
    }

    function getChildrenAndLinks( currentNode, parentNode ) {

        var node = {},
            links = [];

        // Node already processed?
        if (currentNode.investor_identifier in nodesProcessed) {
          links.push(getLink(parentNode, nodesProcessed[currentNode.investor_identifier], currentNode.type));
          // New node
        } else {
          node = currentNode;
          nodesProcessed[currentNode.investor_identifier] = node;
          // Node has children
          if (node.stakeholders && Object.keys(node.stakeholders).length > 0) {
            var children = [],
                childNode;

            // First only check all direct children
            for (var investor_identifier in node.stakeholders) {
              if (!node.stakeholders.hasOwnProperty(investor_identifier)) continue;
              childNode = node.stakeholders[investor_identifier];

              var [childRoot, childCrossLinks] = getChildrenAndLinks(childNode, node);

              if (Object.keys(childRoot).length > 0) {
                children.push(childRoot);
              }
              if (childCrossLinks.length > 0) {
                links.push.apply(links, childCrossLinks)
              }
            }
            node.children = children;

            // Node doesn't have children
          } else {
            // Remove all children
            node.children = [];
          }
          // Also save disabled children, since relations are only saved within the first occurance
          /*if (node._childrenAndLinks && Object.keys(node._childrenAndLinks).length > 0) {
              for (var name in node._childrenAndLinks) {
                  if (!(name in nodesProcessed)) {
                  	nodesProcessed[name] = node._childrenAndLinks[name];
                  }
              }
          }*/
        }

        return [node, links];
    }

    return getChildrenAndLinks( curRoot );
};

var showInvestorModal = function( d, i ) {
    var modal = $('#stakeholder'),
        data = d.data,
        type = (data.type === 1 && "Parent company" || data.type === 2 && "Tertiary investor/lender" || "Operating company");
    modal.find('.modal-header h4').text(data.name);
  	var output = [
  	  data.classification,
  	  data.country,
  	  data.homepage && '<a target="_blank" href="' + data.homepage + '">' + data.homepage + '</a>',
  	  data.opencorporates_link && '<a target="_blank" href="' + data.opencorporates_link + '">' + data.opencorporates_link + '</a>',
  	  data.comment,
  	];
    if (data.involvement) {
    	var inv = data.involvement;
      output.push.apply(output, [
        '<h4>Involvement</h4>' + d.type,
        (inv.percentage && inv.percentage + "%" + (inv.investment_type && " " + inv.investment_type || "") || ""),
        inv.loans_amount && inv.loans_amount + " " + inv.loans_currency + (inv.loans_date && " (" + inv.loans_date + ")"),
        inv.comment,
        inv.parent_relation,
      ]);
    }
    output = output.filter(function (val) {return val;}).join('<br>');
    modal.find('.modal-body p').html(output);
    modal.find('.modal-footer a.investor-link').attr('href', data.url);
    modal.modal("show");
};

// This is a modified version of `d3.svg.diagonal` to draw edges that cross
// tree branches. The edges are shifted so that they do not lie over the curves
// drawn by the normal D3 diagonal. The shift is increased as the distance
// between the nodes increases so that multiple cross edges connecting to the
// same node diverge for clarity.
//
// See https://github.com/mbostock/d3/wiki/SVG-Shapes#diagonal
var crossDiagonal = function() {
    var projection = function( d ) { return [d.y, d.x]; };
    var distance_factor = 10;
    var shift_factor = 2;

    function diagonal( p0, p3, path ) {
        var l = ( p0.x + p3.x ) / 2;
        var m = ( p0.x + p3.x ) / 2;
        var x_shift = 0;
        var y_shift = 0;

        // Self reference
        if ( p0.x === p3.x && p0.y === p3.y ) {
        	return "M" + p0.y + "," + (p0.x+36) + "A24,24 -45,1,1 " + (p0.y+.1) + "," + (p0.x+36.1);
        }
        // Shorten path?
        if (path) {
          var pl = path.getTotalLength();
          var r = 40;
          var d = path.getPointAtLength(Math.round(pl - r));
          p3.x = d.y;
          p3.y = d.x;
        }
        var p = [
            p0,
            p3
        ];
        p = p.map( projection );
        return 'M' + p[0] + 'L' + p[1];
    }

    diagonal.source = function( x ) {
        if ( !arguments.length ) return source;
        source = d3.functor( x );
        return diagonal;
    };

    diagonal.target = function( x ) {
        if ( !arguments.length ) return target;
        target = d3.functor( x );
        return diagonal;
    };

    diagonal.projection = function( x ) {
        if ( !arguments.length ) return projection;
        projection = x;
        return diagonal;
    };

    return diagonal;
};

function diagonal(s, d) {
    return  `M ${s.y} ${s.x} L ${d.y} ${d.x}`;
};

var findNode = function (investor_identifier) {
   return d3.selectAll(".node").filter( function (d) {
       return d && (d.data.investor_identifier === investor_identifier);
   }).datum();
};

var shortenLink = function (node) {
    var s = node;
    var pl = this.getTotalLength();
    var r = 40;
    var d = this.getPointAtLength(Math.round(pl - r));
    return `M ${s.y} ${s.x} L ${d.x} ${d.y}`;
};

// The chart builder function to build a tree with cross links.
// Configuration is excluded for the simplicity of the example.
var linkedTreeChartBuilder = function( parentElement ) {

    var i = 0,
	    duration = 750,
      data;

    // Set up the boundaries.
    var margin = { top: 20, right: 30, bottom: 20, left: 30 };
    var width = 960 - margin.left - margin.right;
    var height = 600 - margin.top - margin.bottom;

    // Assigns parent, children, height, depth
    treeData.x0 = height / 2;
    treeData.y0 = 0;

    var classes = {
    	0: 'operating',
      1: 'parent',
      2: 'tertiary'
    }

    // Create the chart SVG.
    var svg = parentElement.append( 'svg' )
    	  .attr( 'width', width + margin.left + margin.right )
        .attr( 'height', height + margin.top + margin.bottom );

    // Create arrow definitions
    var defs = svg.append( 'defs' );
    defs.append('marker')
        .attr('id', 'arrowhead-parent')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 0)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 6)
        .attr('markerHeight', 6)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#72B0FD')
        .style('stroke', 'none');
    defs.append('marker')
       .attr('id', 'arrowhead-tertiary')
       .attr('viewBox', '-0 -5 10 10')
       .attr('refX', 0)
       .attr('refY', 0)
       .attr('orient', 'auto')
       .attr('markerWidth', 6)
       .attr('markerHeight', 6)
       .attr('xoverflow', 'visible')
       .append('svg:path')
       .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
       .attr('fill', '#F78E8F')
       .style('stroke', 'none');

    var chart = svg.append( 'g' )
        .attr( 'class', 'chart' )
        .attr( 'transform',
        	  'translate(' + margin.left + ',' + margin.top + ')' );

    // Create the helper functions
    var crossLinkDiagonal = crossDiagonal();

    // Assigns the x and y position for the nodes
    var treemap = d3.tree().size( [height, width] );

    // The chart update function that this builder returns.
    var update = function( source ) {

        var [curRoot, curCrossLinksData] = getLinkedTreeData( treeData, crossLinksData );
        curRoot = d3.hierarchy(curRoot, function(d) { return d.children; });

  			// Compute the new tree layout.
        var curTreeData = treemap( curRoot ),
            nodes = curTreeData.descendants(),
  			    links = curTreeData.descendants().slice(1);

        // Normalize for fixed-depth.
        nodes.forEach(function(d){ d.y = d.depth * 180});

        // ****************** Nodes section ***************************
        // Update the nodes…
        var node = chart.selectAll("g.node")
          .data(nodes, function(d) { return d.data.investor_identifier; });

        // Enter any new nodes at the parent's previous position.
        var nodeEnter = node.enter().append("g")
          .attr( 'class', function (d) {
            return 'node ' + classes[d.data.type] + (d.data._stakeholders ? ' has-children' : '');
          } )
          .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
          .on("click", click)
          .on("contextmenu", function (d, i) {
            d3.event.preventDefault();
            showInvestorModal(d, i);
          });

        $('svg .node').tooltip({
          'container': 'body',
          'placement': 'bottom',
          'html': true,
          'title': function() {
            var data = d3.select(this).datum().data,
                name = "<strong>" + data.name + '</strong>',
                meta = [data.country, data.classification].join(", ");
            return name + (meta ? '<br>' + meta : '');
          }
        });

        nodeEnter.append("circle")
          .attr("r", 1e-6);

        nodeEnter.append("text")
          .attr("x", 0)
          .attr("dy", ".35em")
          .text(function(d) { return '#' + d.data.investor_identifier; });

        // UPDATE
        var nodeUpdate = nodeEnter.merge(node);

        // Transition nodes to their new position.
        nodeUpdate//.transition()
          //.duration(duration)
          .attr( 'class', function (d) {
            return 'node ' + classes[d.data.type] + (d.data._stakeholders ? ' has-children' : '');
          } )
          .attr("transform", function(d) {
          	return "translate(" + d.y + "," + d.x + ")"
          });

        nodeUpdate.select("circle")
          .attr("r", 28);

        nodeUpdate.select("text")
          .style("fill-opacity", 1);

        // Transition exiting nodes to the parent's new position.
        var nodeExit = node.exit()//.transition()
          //.duration(duration)
          .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
          .remove();

        nodeExit.select("circle")
          .attr("r", 1e-6);

        nodeExit.select("text")
          .style("fill-opacity", 1e-6);

        // ****************** links section ***************************
        // Update the links
        var link = chart.selectAll("path.link")
          .data(links, function(d) { return d.data.investor_identifier; });

        // Enter any new links at the parent's previous position.
        var linkEnter = link.enter().insert("path", "g")
          .attr("d", function(d) {
            var o = {x: source.x0, y: source.y0};
            return diagonal(o, o);
          });

        // UPDATE
        var linkUpdate = linkEnter.merge(link);

        // Transition links to their new position.
        linkUpdate//.transition()
          //.duration(duration)
          .attr('d', function(d){ return diagonal(d, d.parent) })
          .attr('d', shortenLink)
          .attr( 'class', function (d) {
            return 'link ' + classes[d.data.type];
          })
          .attr('marker-end', function(d) {
          	return 'url(#arrowhead-' + classes[d.data.type] + ')';
          });

        // Transition exiting nodes to the parent's new position.
        var linkExit = link.exit()//.transition()
          //.duration( duration )
          .attr("d", function(d) {
          	var o = {x: source.x, y: source.y};
          	return diagonal(o, o);
          })
          .remove();

        // *************** cross links section ************************
        // The edge lines for the cross-links.
        var crossLink = chart.selectAll( 'path.crosslink' )
          .data( curCrossLinksData, function(d) { return d.target.investor_identifier; });

        var crossLinkEnter = crossLink.enter().insert( "path", "g" )
          .attr("d", function(d) {
            var o = {x: source.x0, y: source.y0};
            return crossLinkDiagonal(o, o);
          });

        // UPDATE
        var crosslinkUpdate = crossLinkEnter.merge(crossLink);

        // Transition cross links to their new position.
        crosslinkUpdate//.transition()
          //.duration( duration )
          .attr( 'class', function (d) {
            return 'crosslink ' + classes[d.type];
          })
          .attr('d', function(d){
          	return crossLinkDiagonal(findNode(d.target.investor_identifier), findNode(d.source.investor_identifier));
          })
          .attr('d', function(d){
          	return crossLinkDiagonal(findNode(d.target.investor_identifier), findNode(d.source.investor_identifier), this);
          })
          .attr('marker-end',function (d) { return 'url(#arrowhead-' + classes[d.type] + ')'; });

			 	// Remove any exiting links
        var crossLinkExit = crossLink.exit()//.transition()
          //.duration( duration )
          .attr("d", function(d) {
          	var o = {x: source.x, y: source.y};
          	return diagonal(o, o);
          })
          .remove();

        // Stash the old positions for transition.
        nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });

        // Toggle children on click.
        function click(d) {
            if (d.data.stakeholders) {
                d.data._stakeholders = d.data.stakeholders;
                d.data.stakeholders = null;
            } else {
                d.data.stakeholders = d.data._stakeholders;
                d.data._stakeholders = null;
            }
            update(d);
        }
    };

    return update;
};

function loadInvestorNetwork(investorId) {
    if (investorId <= 0 || $("#investor-network").size() <= 0) {
        return;
    }
    d3.json("/api/investor_network.json?operational_stakeholder=" + investorId,
        function (data) {
            treeData = data;

            // Build the chart.
            var linkedTreeChart = linkedTreeChartBuilder( d3.select( '#investor-network' ) );

            treeData = updateReferences( treeData );

            // Build a tree and update the chart.
            linkedTreeChart( treeData );
        }
    );
}