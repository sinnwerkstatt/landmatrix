var inv_margin = { top: 20, right: 30, bottom: 20, left: 30 },
    inv_width = 960 - inv_margin.left - inv_margin.right,
    inv_height = 500 - inv_margin.top - inv_margin.bottom,
    inv_svg, inv_node, inv_inv_node, inv_deal_node,
    inv_link, inv_edgepaths, inv_defs, inv_simulation;

function loadInvestorNetwork(investorId, depth) {
    if (investorId <= 0) {
        return;
    }
    d3.json("/api/investor_network.json?history_id=" + investorId + "&depth=" + depth,
        function (data) {
          drawInvestorNetwork(data.links, data.nodes);
        }
    );
}

var inv_classes = {
  0: 'operating',
  1: 'parent',
  2: 'tertiary',
  3: 'deal'
};


var showInvestorModal = function( data, i ) {
    var modal = $('#stakeholder'),
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
        '<h4>Involvement</h4>' + type,
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

var showDealModal = function( data, i ) {
    var modal = $('#deal');
    modal.find('.modal-header h4').text('#' + data.name);
  	var output = [
  	  data.country
  	];
    output = output.filter(function (val) {return val;}).join('<br>');
    modal.find('.modal-body p').html(output);
    modal.find('.modal-footer a.deal-link').attr('href', data.url);
    modal.modal("show");
};

function wordwrap(str, width) {
  var width = width || 20;
  if (!str) {
    return str;
  }
  var regex = '.{1,' +width+ '}(\\s|$)';
  return str.match( RegExp(regex, 'g') );
}

function drawInvestorNetwork(links, nodes) {
  d3.select("#investor-network").select("svg").remove();
  inv_svg = d3.select("#investor-network").append("svg")
      .attr("width", inv_width + inv_margin.left + inv_margin.right)
      .attr("height", inv_height + inv_margin.top + inv_margin.bottom)
    .append("g");

  inv_defs = inv_svg.append('defs');
  inv_defs.append('marker')
    .attr('id', 'arrowhead-parent')
    .attr('viewBox', '-0 -5 10 10')
    .attr('refX', 32)
    .attr('refY', 0)
    .attr('orient', 'auto')
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('xoverflow', 'visible')
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .attr('fill', '#72B0FD')
    .style('stroke','none');
  inv_defs.append('marker')
    .attr('id', 'arrowhead-tertiary')
    .attr('viewBox', '-0 -5 10 10')
    .attr('refX', 32)
    .attr('refY', 0)
    .attr('orient', 'auto')
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('xoverflow', 'visible')
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .attr('fill', '#F78E8F')
    .style('stroke','none');

  inv_simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) {return d.id;})
      .distance(500)
      .strength(0))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(inv_width / 2, inv_height / 2));
    //.stop();

  // inv_simulation.force("link")
  //  .links(links);

  // for (var i = 0; i < 300; ++i) inv_simulation.tick();

  inv_link = inv_svg.selectAll(".link")
    .data(links)
    .enter()
    .append("line")
    .attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; })
    .attr("class", function (d) { return "link " + inv_classes[d.type]; })
    .attr('marker-end',function (d) { return 'url(#arrowhead-' + inv_classes[d.type] + ')'; });

  inv_edgepaths = inv_svg.selectAll(".edgepath")
    .data(links)
    .enter()
    .append('path')
    .attr('class', 'edgepath')
    .attr('fill-opacity', 0)
    .attr('stroke-opacity', 0)
    .attr('id', function (d, i) {return 'edgepath' + i})
    .style("pointer-events", "none");

  inv_node = inv_svg.selectAll(".node")
    .data(nodes)
    .enter()
    .append("g")
    .attr("cx", function(d) { return d.x; })
    .attr("cy", function(d) { return d.y; })
    .attr("class", function (d) {
      var cls =  'node';
      cls += d.type === 1 ? ' investor' : ' deal';
      cls += d.is_root ? ' is-root' : '';
      cls += d.has_next_level ? ' has-children' : '';
      return cls;
    })
    .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    );

  inv_node.append("circle")
    .attr("r", 28);

  // Investor nodes
  inv_inv_node = inv_svg.selectAll(".node.investor")
    // .on("click", click)
    .on("contextmenu", function (d, i) {
      d3.event.preventDefault();
      showInvestorModal(d, i);
    });

  $('svg .node.investor').tooltip({
    'container': 'body',
    'placement': 'bottom',
    'html': true,
    'title': function() {
      var data = d3.select(this).datum(),
          name = "<strong>" + data.name + '</strong>',
          meta = [data.country, data.classification].filter(function (val) {return val;}).join(", ");
      return name + (meta ? '<br>' + meta : '');
    }
  });

  inv_inv_node.append("text")
    .attr("dy", "-1.1em")
    .attr("class", "subtitle")
    .text(function (d) {return '#' + d.identifier;});

  inv_inv_node.append("text")
    .attr("dy", "-.1em")
    .text(function (d) {
      if (d.name.length > 20) {
        return wordwrap(d.name)[0];
      } else {
        return '';
      }
    });

  inv_inv_node.append("text")
    .attr("dy", ".9em")
    .text(function (d) {
      if (d.name.length <= 40) {
        return d.name.length > 20 ? wordwrap(d.name)[1] : d.name;
      } else {
        return wordwrap(d.name)[1] + '...';
      }
    });

  inv_inv_node.append("text")
    .attr("dy", "1.9em")
    .attr("class", "subtitle")
    .text(function (d) {return d.country_code;});

  // Deal nodes
  inv_deal_node = inv_svg.selectAll(".node.deal")
    // .on("click", click)
    .on("contextmenu", function (d, i) {
      d3.event.preventDefault();
      showDealModal(d, i);
    });

  $('svg .node.deal').tooltip({
    'container': 'body',
    'placement': 'bottom',
    'html': true,
    'title': function() {
      var data = d3.select(this).datum(),
          name = "<strong>#" + data.name + '</strong>';
      return name + '<br>' + data.country;
    }
  });

  inv_deal_node.append("text")
    .attr("dy", ".35em")
    .text(function (d) {return '#' + d.identifier;});

  inv_deal_node.append("text")
    .attr("dy", "1.9em")
    .attr("class", "subtitle")
    .text(function (d) {return d.country_code;});

  inv_simulation
    .nodes(nodes)
    .on("tick", ticked);

  inv_simulation.force("link")
    .links(links);
}

function ticked() {
  inv_link
    .attr("x1", function (d) {return d.source.x;})
    .attr("y1", function (d) {return d.source.y;})
    .attr("x2", function (d) {return d.target.x;})
    .attr("y2", function (d) {return d.target.y;});

  inv_node
    .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});

  inv_edgepaths.attr('d', function (d) {
    return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x + ' ' + d.target.y;
  });

  inv_edgepaths.attr('transform', function (d) {
    if (d.target.x < d.source.x) {
      var bbox = this.getBBox();

      rx = bbox.x + bbox.width / 2;
      ry = bbox.y + bbox.height / 2;
      return 'rotate(180 ' + rx + ' ' + ry + ')';
    }
    else {
      return 'rotate(0)';
    }
  });
}

function dragstarted(d) {
  // if (!d3.event.active) simulation.alphaTarget(0.2).restart()
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
	// if (!d3.event.active) simulation.alphaTarget(0);
	d.fx = undefined;
	d.fy = undefined;
}
