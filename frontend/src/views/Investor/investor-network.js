import * as d3 from "d3";
import { hierarchy } from "d3-hierarchy";

import {
  forceCenter,
  forceCollide,
  forceLink,
  forceManyBody,
  forceSimulation,
  forceX,
  forceY,
} from "d3-force";

const invMargin = { top: 20, right: 30, bottom: 20, left: 30 },
  invWidth = 960 - invMargin.left - invMargin.right,
  invHeight = 500 - invMargin.top - invMargin.bottom;
let invSvg;

let invData = {};
const invCrossLinksData = [];

// const showInvestorModal = function(data, i) {
//   const modal = $("#stakeholder"),
//     type =
//       (data.type === "parent" && "Parent company") ||
//       (data.type === "tertiary" && "Tertiary investor/lender") ||
//       "Operating company";
//   modal.find(".modal-header h4").text(data.name + " (#" + data.identifier + ")");
//   let output = [
//     data.classification,
//     data.country,
//     data.homepage &&
//     "<a target=\"_blank\" href=\"" + data.homepage + "\">" + data.homepage + "</a>",
//     data.opencorporates_link &&
//     "<a target=\"_blank\" href=\"" +
//     data.opencorporates_link +
//     "\">" +
//     data.opencorporates_link +
//     "</a>",
//     data.comment
//   ];
//   if (data.involvement) {
//     const inv = data.involvement;
//     output.push.apply(output, [
//       "<h4>Involvement</h4>" + type,
//       (inv.percentage &&
//         inv.percentage +
//         "%" +
//         ((inv.investment_type && " " + inv.investment_type) || "")) ||
//       "",
//       inv.loans_amount &&
//       inv.loans_amount +
//       " " +
//       inv.loans_currency +
//       (inv.loans_date && " (" + inv.loans_date + ")"),
//       inv.comment,
//       inv.parent_relation
//     ]);
//   }
//   output = output
//     .filter(function(val) {
//       return val;
//     })
//     .join("<br>");
//   modal.find(".modal-body p").html(output);
//   modal.find(".modal-footer a.investor-link").attr("href", data.url);
//   modal.modal("show");
// };

// const showDealModal = function(data, i) {
//   const modal = $("#deal");
//   modal.find(".modal-header h4").text("Deal #" + data.name);
//   let output = [
//     data.country,
//     data.intention ? "Intention of investment" + ": " + data.intention : "",
//     data.implementation_status
//       ? "Implementation status" + ": " + data.implementation_status
//       : "",
//     data.intended_size ? "Intended size (in ha)" + ": " + data.intended_size : "",
//     data.contract_size
//       ? "Size under contract (leased or purchased area, in ha)" +
//       ": " +
//       data.contract_size
//       : "",
//     data.production_size
//       ? "Size in operation (production, in ha)" + ": " + data.production_size
//       : ""
//   ];
//   output = output
//     .filter(function(val) {
//       return val;
//     })
//     .join("<br>");
//   modal.find(".modal-body p").html(output);
//   modal.find(".modal-footer a.deal-link").attr("href", data.url);
//   modal.modal("show");
// };

const findNode = function (id) {
  const node = d3.selectAll(".node").filter(function (d) {
    return d && d.data.id === id;
  });
  return node.size() && node.datum();
};

function wordwrap(str, width) {
  width = width || 20;
  if (!str) {
    return str;
  }
  const regex = ".{1," + width + "}(\\s|$)";
  return str.match(RegExp(regex, "g"));
}

// Find references (duplicate nodes) and split original/duplicates
// const updateReferences = function(data) {
//   const uniqueNodes = {},
//     nodes = [data];
//
//   while ((node = nodes.pop())) {
//     let children = [];
//     if (Object.keys(node.investors || node.deals || {}).length > 0) {
//       children = node.investors.concat(node.deals);
//     } else if (Object.keys(node._investors || node._deals || {}).length > 0) {
//       children = node._investors.concat(node._deals);
//     }
//     // Original?
//     if (Object.keys(children).length > 0) {
//       if (node.id in uniqueNodes) {
//         uniqueNodes[node.id].original = node;
//       } else {
//         uniqueNodes[node.id] = {
//           original: node,
//           duplicates: []
//         };
//
//         for (var id in children) {
//           nodes.push(children[id]);
//         }
//       }
//     } else {
//       // Duplicate
//       if (node.id in uniqueNodes) {
//         uniqueNodes[node.id].duplicates.push(node);
//       } else {
//         uniqueNodes[node.id] = {
//           original: undefined,
//           duplicates: [node]
//         };
//       }
//     }
//   }
//
//   for (var id in uniqueNodes) {
//     var node = uniqueNodes[id],
//       duplicate;
//     if (!node.original) continue;
//     for (let i = 0; i < node.duplicates.length; i++) {
//       duplicate = node.duplicates[i];
//       duplicate.found = "1";
//       duplicate.investors = node.original.investors;
//       duplicate._investors = node.original._investors;
//       duplicate.deals = node.original.deals;
//       duplicate._deals = node.original._deals;
//     }
//   }
//
//   return data;
// };

// Update children/links in tree
const getLinkedTreeData = function (curRoot, curCrossLinks) {
  const nodesProcessed = {};

  function getLink(node, childNode, type, dir) {
    let found = false,
      link;
    // Find link
    for (let i = 0; i < curCrossLinks.length; i++) {
      link = curCrossLinks[i];
      if (link.source.id === node.id && link.target.id === childNode.id) {
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
        type: type,
        dir: dir,
      };
    }
    return link;
  }

  function getChildrenAndLinks(currentNode, parentNode) {
    let node = {};
    const links = [];

    // Node already processed?

    if (currentNode.id in nodesProcessed) {
      let type = currentNode.type,
        dir = "parent";
      if (type === "investor") {
        type = currentNode.involvement.type;
        dir = currentNode.involvement.dir;
      }
      links.push(getLink(parentNode, nodesProcessed[currentNode.id], type, dir));
      // New node
    } else {
      node = currentNode;
      nodesProcessed[currentNode.id] = node;
      // Node has children
      if (!node.investors) {
        node.investors = [];
      }
      if (!node.deals) {
        node.deals = [];
      }
      const investorsAndDeals = node.investors.concat(node.deals);
      if (investorsAndDeals && Object.keys(investorsAndDeals).length > 0) {
        const children = [];
        let childNode;

        // First only check all direct children
        for (let id in investorsAndDeals) {
          if (!investorsAndDeals.hasOwnProperty(id)) continue;
          childNode = investorsAndDeals[id];

          let [childRoot, childCrossLinks] = getChildrenAndLinks(childNode, node);

          if (Object.keys(childRoot).length > 0) {
            children.push(childRoot);
          }
          if (childCrossLinks.length > 0) {
            links.push.apply(links, childCrossLinks);
          }
        }
        node.children = children;
      } else {
        node.children = [];
      }
      // Also save disabled children, since relations are only saved within the first occurance
      /*if (node._childrenAndLinks && Object.keys(node._childrenAndLinks).length > 0) {
          for (var name in node._childrenAndLinks) {
              if (!(name in nodesProcessed)) {
                nodesProcessed[name] = node._childrenAndLinks[name];
              }
          }
      }*/
    }

    return [node, links];
  }

  return getChildrenAndLinks(curRoot);
};

/*
This code is based on:
https://bl.ocks.org/anonymous/ca046ccc115520d501060e4256aa6ada

and the following convention:
https://github.com/bumbeishvili/d3-coding-conventions
*/

function renderChartCollapsibleNetwork(params) {
  // Exposed variables
  let attrs = {
    id: "id" + Math.floor(Math.random() * 1000000),
    svgWidth: 960,
    svgHeight: 600,
    marginTop: 0,
    marginBottom: 5,
    marginRight: 0,
    marginLeft: 30,
    nodeRadius: 28,
    container: "body",
    distance: 100,
    hiddenChildLevel: 1,
    lineStrokeWidth: 1.5,
    data: null,
    ...params,
  };

  // InnerFunctions which will update visuals
  let updateData;
  let filter;

  // Main chart object
  const main = function (selection) {
    selection.each(function scope() {
      // Calculated properties
      const calc = {};
      calc.chartLeftMargin = attrs.marginLeft;
      calc.chartTopMargin = attrs.marginTop;
      calc.chartWidth = attrs.svgWidth - attrs.marginRight - calc.chartLeftMargin;
      calc.chartHeight = attrs.svgHeight - attrs.marginBottom - calc.chartTopMargin;

      // ########################## HIERARCHY STUFF  #########################
      const myhierarchy = {};

      // // ###########################   BEHAVIORS #########################
      // const behaviors = {};
      // // behaviors.zoom = d3.zoom().scaleExtent([0.75, 1.5, 8]).on("zoom", zoomed);
      // // behaviors.drag = d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended);

      // ###########################   LAYOUTS #########################
      const layouts = {};

      // Custom radial kayout
      layouts.radial = d3.radial();

      // ###########################   FORCE STUFF #########################
      const force = {};
      force.link = forceLink().id((d) => d.id);
      force.charge = forceManyBody();
      force.center = forceCenter(calc.chartWidth / 2, calc.chartHeight / 2);

      // Prevent collide
      force.collide = forceCollide().radius((d) => {
        // If parent has many children, reduce collide strength
        if (d.parent) {
          if (d.parent.children.length > 10) {
            // Also slow down node movement
            slowDownNodes();
            return 7;
          }
        }

        // Increase collide strength
        if (d.children && d.depth > 2) {
          return attrs.nodeRadius;
        }
        return attrs.nodeRadius * 2;
      });

      // Manually set x positions (which is calculated using custom radial layout)
      force.x = forceX()
        .strength(0.5)
        .x(function (d, i) {
          // If node does not have children and is channel (depth=2) , then position it on parent's coordinate
          if (!d.children && d.depth > 2) {
            if (d.parent) {
              d = d.parent;
            }
          }

          // Custom circle projection -  radius will be -  (d.depth - 1) * 150
          return projectCircle(d.proportion, (d.depth - 1) * 150)[0];
        });

      // Manually set y positions (which is calculated using d3.cluster)
      force.y = forceY()
        .strength(0.5)
        .y(function (d, i) {
          // If node does not have children and is channel (depth=2) , then position it on parent's coordinate
          if (!d.children && d.depth > 2) {
            if (d.parent) {
              d = d.parent;
            }
          }

          // Custom circle projection -  radius will be -  (d.depth - 1) * 150
          return projectCircle(d.proportion, (d.depth - 1) * 150)[1];
        });

      //---------------------------------  INITIALISE FORCE SIMULATION ----------------------------

      // Get based on top parameter simulation
      force.simulation = forceSimulation()
        .force("link", force.link)
        .force("charge", force.charge)
        .force("center", force.center)
        .force("collide", force.collide)
        .force("x", force.x)
        .force("y", force.y);

      // ###########################   HIERARCHY STUFF #########################

      // Flatten root
      let [startRoot, startCrossLinksData] = getLinkedTreeData(
        invData,
        invCrossLinksData
      );
      myhierarchy.root = hierarchy(startRoot, function (d) {
        return d.children;
      });
      hideLevels();

      // ####################################  DRAWINGS #######################

      // Drawing containers
      const container = d3.select(this);

      // Add svg
      invSvg = container
        .patternify({ tag: "svg", selector: "svg-chart-container" })
        .attr("viewBox", "0 0 " + attrs.svgWidth + " " + attrs.svgHeight)
        .attr("width", attrs.svgWidth)
        .attr("height", attrs.svgHeight);
      // .call(behaviors.zoom);

      // Add container g element
      const chart = invSvg
        .patternify({ tag: "g", selector: "chart" })
        .attr(
          "transform",
          "translate(" + calc.chartLeftMargin + "," + calc.chartTopMargin + ")"
        );

      // ################################   Chart Content Drawing ##################################

      // Defs for arrows
      let invDefs = invSvg.append("defs");
      invDefs
        .append("marker")
        .attr("id", "arrowhead-parent")
        .attr("viewBox", "-0 -5 10 10")
        .attr("refX", 32)
        .attr("refY", 0)
        .attr("orient", "auto")
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("xoverflow", "visible")
        .append("svg:path")
        .attr("d", "M 0,-5 L 10 ,0 L 0,5")
        .attr("fill", "#72B0FD")
        .style("stroke", "none");
      invDefs
        .append("marker")
        .attr("id", "arrowhead-tertiary")
        .attr("viewBox", "-0 -5 10 10")
        .attr("refX", 32)
        .attr("refY", 0)
        .attr("orient", "auto")
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("xoverflow", "visible")
        .append("svg:path")
        .attr("d", "M 0,-5 L 10 ,0 L 0,5")
        .attr("fill", "#F78E8F")
        .style("stroke", "none");

      // Link wrapper
      const linksWrapper = chart.patternify({ tag: "g", selector: "links-wrapper" });
      const crossLinksWrapper = chart.patternify({
        tag: "g",
        selector: "crosslinks-wrapper",
      });

      // Node wrapper
      const nodesWrapper = chart.patternify({ tag: "g", selector: "nodes-wrapper" });
      let nodes, links, crossLinks, enteredNodes, invNodes, dealNodes;

      // Reusable function which updates visual based on data change
      update();

      // Update visual based on data change
      function update(clickedNode) {
        // Set xy and proportion properties with custom radial layout
        let [curRoot, curCrossLinksData] = getLinkedTreeData(
          invData,
          invCrossLinksData
        );
        curRoot = hierarchy(curRoot, function (d) {
          return d.children;
        });
        layouts.radial(curRoot);

        // Nodes and links array
        const nodesArr = flatten(curRoot, true)
          .orderBy((d) => d.depth)
          .filter((d) => !d.hidden);

        const linksArr = curRoot
          .links()
          .filter((d) => !d.source.hidden)
          .filter((d) => !d.target.hidden);

        // Make new nodes to appear near the parents
        nodesArr.forEach(function (d, i) {
          if (clickedNode && clickedNode.data.id === d.data.id) {
            d.fx = clickedNode.x;
            d.fy = clickedNode.y;
          }
          if (clickedNode && clickedNode.parent.id === (d.parent && d.parent.data.id)) {
            d.x = d.parent.x;
            d.y = d.parent.y;
          }
        });

        // Node groups
        nodes = nodesWrapper.selectAll(".node").data(nodesArr, (d) => d.data.id);
        nodes.exit().remove();
        enteredNodes = nodes.enter().append("g");

        // Bind event handlers
        enteredNodes
          .on("click", nodeClick)
          .on("mouseenter", nodeMouseEnter)
          .on("mouseleave", nodeMouseLeave);
        // .call(behaviors.drag);

        enteredNodes.append("circle").attr("r", attrs.nodeRadius);

        // Modal
        enteredNodes.on("contextmenu", function (d, i) {
          d3.event.preventDefault();
          // if (d.data.type === "investor") {
          //   showInvestorModal(d.data, i);
          // } else {
          //   showDealModal(d.data, i);
          // }
        });

        // Tooltip
        // $("svg .node").tooltip({
        //   container: "body",
        //   placement: "bottom",
        //   html: true,
        //   title: function () {
        //     const data = d3.select(this).datum().data;
        //     if (data.type == "investor") {
        //       var name =
        //           "<strong>" + data.name + " (#" + data.identifier + ")</strong>",
        //         meta = [data.country, data.classification]
        //           .filter(function (val) {
        //             return val;
        //           })
        //           .join(", ");
        //       return name + (meta ? "<br>" + meta : "");
        //     } else {
        //       var name = "<strong>Deal #" + data.name + "</strong>";
        //       return name + "<br>" + data.country;
        //     }
        //   },
        // });

        // Subtitle top
        // invNodes.append("text")
        //   .attr("dy", "-1.1em")
        //   .attr("class", "subtitle")
        //   .text(function (d) {return '#' + d.identifier;});

        // Title (first or center row)
        enteredNodes
          .append("text")
          .attr("dy", function (d) {
            return d.data.type === "investor" ? "-.1em" : ".35em";
          })
          .text(function (d) {
            if (d.data.type === "investor") {
              const name = d.data.name;
              if (name.length > 20) {
                return wordwrap(name)[0];
              } else {
                return "";
              }
            } else {
              return "#" + d.data.identifier;
            }
          });

        // Title (second row)
        enteredNodes
          .append("text")
          .attr("dy", function (d) {
            return d.data.name.length > 20 ? ".9em" : ".35em";
          })
          .text(function (d) {
            if (d.data.type === "investor") {
              const name = d.data.name;
              if (name.length <= 40) {
                return name.length > 20 ? wordwrap(name)[1] : name;
              } else {
                return wordwrap(name)[1] + "...";
              }
            }
          });

        // Subtitle (bottom)
        enteredNodes
          .append("text")
          .attr("dy", "1.9em")
          .attr("class", "subtitle")
          .text(function (d) {
            return d.data.country_code;
          });

        // Merge node groups and style it
        nodes = enteredNodes.attr("class", function (d) {
          const data = d.data;
          let cls = "node " + data.type;
          cls += data.is_root ? " is-root" : "";
          if (
            (data._investors && Object.keys(data._investors).length > 0) ||
            (data._deals && Object.keys(data._deals).length > 0)
          ) {
            cls += " has-children";
          }
          return cls;
        });

        // Links
        function getLinkClass(d) {
          const data = d.target.data;
          return (data.involvement && data.involvement.type) || data.type;
        }

        function getCrossLinkClass(d) {
          const data = d.target;
          return (
            d.type || (data.type === "investor" && data.involvement.type) || data.type
          );
        }

        links = linksWrapper
          .selectAll(".link")
          .data(linksArr, (d) => d.source.id + "-" + d.target.id);
        // links.exit().remove();
        links = links
          .enter()
          .append("line")
          .merge(links)
          .attr("class", function (d) {
            return "link " + getLinkClass(d);
          })
          .attr("marker-end", function (d) {
            return "url(#arrowhead-" + getLinkClass(d) + ")";
          });

        // Cross links
        crossLinks = crossLinksWrapper
          .selectAll(".crosslink")
          .data(curCrossLinksData, (d) => d.source.id + "-" + d.target.id);
        crossLinks.exit().remove();

        crossLinks = crossLinks
          .enter()
          .insert("line")
          // .merge(crossLinks)
          .attr("class", function (d) {
            return "crosslink " + getCrossLinkClass(d);
          })
          .attr("marker-end", function (d) {
            return "url(#arrowhead-" + getCrossLinkClass(d) + ")";
          });

        // Force simulation
        force.simulation.nodes(nodesArr).on("tick", ticked);

        // Links simulation
        force.simulation
          .force("link")
          .links(links)
          .id((d) => d.id)
          .distance(100)
          .strength((d) => 1);

        // Cross links simulation
        force.simulation
          .force("link")
          .links(crossLinks)
          .id((d) => d.id)
          .distance(100)
          .strength((d) => 1);
      }

      // ####################################### EVENT HANDLERS  ########################

      // Zoom handler
      function zoomed() {
        // Get transform event
        const transform = d3.event.transform;
        attrs.lastTransform = transform;

        // Apply transform event props to the wrapper
        chart.attr("transform", transform);

        invSvg.selectAll("marker").attr("refX", function (d) {
          return 32 / (attrs.lastTransform ? attrs.lastTransform.k : 1);
        });

        invSvg.selectAll(".node").attr("transform", function (d) {
          return `translate(${
            d.x
          },${d.y}) scale(${1 / (attrs.lastTransform ? attrs.lastTransform.k : 1)})`;
        });
        invSvg
          .selectAll(".link")
          .attr(
            "stroke-width",
            attrs.lineStrokeWidth / (attrs.lastTransform ? attrs.lastTransform.k : 1)
          );
      }

      // Tick handler
      function ticked() {
        function getDirNode(r, s, t) {
          if (r.data.involvement && r.data.involvement.dir === "parent") {
            return t;
          } else {
            return s;
          }
        }

        // Set links position
        links
          .attr("x1", function (d) {
            return getDirNode(d.target, d.target, d.source).x;
          })
          .attr("y1", function (d) {
            return getDirNode(d.target, d.target, d.source).y;
          })
          .attr("x2", function (d) {
            return getDirNode(d.target, d.source, d.target).x;
          })
          .attr("y2", function (d) {
            return getDirNode(d.target, d.source, d.target).y;
          });

        // Set crosslinks position
        crossLinks
          .attr("x1", function (d) {
            return findNode(d.dir === "parent" ? d.target.id : d.source.id).x;
          })
          .attr("y1", function (d) {
            return findNode(d.dir === "parent" ? d.target.id : d.source.id).y;
          })
          .attr("x2", function (d) {
            return findNode(d.dir === "parent" ? d.source.id : d.target.id).x;
          })
          .attr("y2", function (d) {
            return findNode(d.dir === "parent" ? d.source.id : d.target.id).y;
          });

        // Set nodes position
        invSvg.selectAll(".node").attr("transform", function (d) {
          if (d.fx && d.fy) {
            return `translate(${d.fx},${d.fy})`;
          } else {
            return `translate(${d.x},${d.y}) scale(${
              1 / (attrs.lastTransform ? attrs.lastTransform.k : 1)
            })`;
          }
        });
      }

      // Handler drag start event
      function dragstarted(d) {
        // Disable node fixing
        // nodes.each(d => { d.fx = null; d.fy = null })
      }

      // Handle dragging event
      function dragged(d) {
        // Make dragged node fixed
        d.fx = d3.event.x;
        d.fy = d3.event.y;

        const diffX = d.fx - d.x;
        const diffY = d.fy - d.y;
        const moved = [d.id];

        function moveChildren(node) {
          if (!node.children) {
            return;
          }
          for (let c of node.children) {
            if (moved.indexOf(c.id) > -1) {
              continue;
            }
            moved.push(c.id);
            c.fx = c.x + diffX;
            c.fy = c.y + diffY;
            moveChildren(c);
          }
        }

        moveChildren(d);
      }

      // -------------------- handle drag end event ---------------
      function dragended(d) {
        // We are doing nothing, here , aren't we?
      }

      // -------------------------- node mouse hover handler ---------------
      function nodeMouseEnter(d) {
        // Get hovered node
        const node = d3.select(this).classed("hover", true);

        // Get links
        const links = myhierarchy.root.links();

        // Get hovered node connected links
        const connectedLinks = links.filter(
          (l) => l.source.id === d.id || l.target.id === d.id
        );

        // Get hovered node linked nodes
        const linkedNodes = connectedLinks
          .map((s) => s.source.id)
          .concat(connectedLinks.map((d) => d.target.id));

        // Reduce all other nodes opacity
        nodesWrapper
          .selectAll(".node")
          .filter((n) => linkedNodes.indexOf(n.id) === -1)
          .classed("hover-other", true);

        // Reduce all other links opacity
        linksWrapper.selectAll(".link").classed("hover-other", true);

        // Highlight hovered nodes connections
        linksWrapper
          .selectAll(".link")
          .filter((l) => l.source.id === d.id || l.target.id === d.id)
          .classed("hover", true);

        // Reduce all other crosslinks opacity
        crossLinksWrapper.selectAll(".crosslink").classed("hover-other", true);

        // Highlight hovered nodes connections
        crossLinksWrapper
          .selectAll(".crosslink")
          .filter((l) => l.source.id === d.id || l.target.id === d.id)
          .classed("hover", true);
      }

      // --------------- handle mouseleave event ---------------
      function nodeMouseLeave(d) {
        // Return things back to normal
        nodesWrapper.selectAll(".node").classed("hover hover-other", false);
        linksWrapper.selectAll(".link").classed("hover hover-other", false);
        crossLinksWrapper.selectAll(".crosslink").classed("hover hover-other", false);
      }

      // --------------- handle node click event ---------------
      function nodeClick(d) {
        function restartSimulation(simulation) {
          simulation.restart();
          simulation.alphaTarget(0.15);
          simulation.alphaDecay(0.005);
          simulation.velocityDecay(0.6);
          simulation.restartAlpha(0.1);
        }

        // Free fixed nodes
        nodes.each((d) => {
          d.fx = null;
          d.fy = null;
        });
        d.children = null;

        // Collapse or expand node
        const data = d.data;
        if (
          (data.investors && Object.keys(data.investors).length > 0) ||
          (data.deals && Object.keys(data.deals).length > 0)
        ) {
          data._investors = data.investors;
          data.investors = null;
          data._deals = data.deals;
          data.deals = null;
          update();
          restartSimulation(force.simulation);
        } else if (
          (data._investors && Object.keys(data._investors).length > 0) ||
          (data._deals && Object.keys(data._deals).length > 0)
        ) {
          data.investors = data._investors;
          data._investors = null;
          data.deals = data._deals;
          data._deals = null;
          update(d);
          restartSimulation(force.simulation);
        } else {
          // Nothing is to collapse or expand
        }
        // freeNodes();
      }

      // #########################################  UTIL FUNCS ##################################
      updateData = function () {
        main.run();
      };

      function slowDownNodes() {
        force.simulation.alphaTarget(0.05);
      }

      function speedUpNodes() {
        force.simulation.alphaTarget(0.45);
      }

      function freeNodes() {
        d3.selectAll(".node").each((n) => {
          n.fx = null;
          n.fy = null;
        });
      }

      function projectCircle(value, radius) {
        const r = radius || 0;
        const corner = value * 2 * Math.PI;
        return [Math.sin(corner) * r, -Math.cos(corner) * r];
      }

      // Recursively loop on children and extract nodes as an array
      function flatten(root, clustered) {
        const nodesArray = [];
        let i = 0;

        function recurse(node, depth) {
          if (node.children)
            node.children.forEach(function (child) {
              recurse(child, depth + 1);
            });
          if (!node.id) node.id = ++i;
          else ++i;
          node.depth = depth;
          if (clustered) {
            if (!node.cluster) {
              // If cluster coordinates are not set, set it
              node.cluster = { x: node.x, y: node.y };
            }
          }
          nodesArray.push(node);
        }

        recurse(root, 1);
        return nodesArray;
      }

      function debug() {
        if (attrs.isDebug) {
          // Stringify func
          const stringified = scope + "";

          // Parse variable names
          const groupVariables = stringified
            // Match var x-xx= {};
            .match(/var\s+([\w])+\s*=\s*{\s*}/gi)
            // Match xxx
            .map((d) => d.match(/\s+\w*/gi).filter((s) => s.trim()))
            // Get xxx
            .map((v) => v[0].trim());

          // Assign local variables to the scope
          groupVariables.forEach((v) => {
            main["P_" + v] = eval(v);
          });
        }
      }

      debug();

      function hideLevels() {
        // Hide members based on their depth
        const arr = flatten(myhierarchy.root);
        arr.forEach((d) => {
          const data = d.data;
          if (d.depth > attrs.hiddenChildLevel) {
            if (data.investors && Object.keys(data.investors).length > 0) {
              data._investors = data.investors;
              data.investors = null;
            }
            if (data.deals && Object.keys(data.deals).length > 0) {
              data._deals = data.deals;
              data.deals = null;
            }
          } else {
            if (data._investors && Object.keys(data._investors).length > 0) {
              data.investors = data._investors;
              data._investors = null;
            }
            if (data._deals && Object.keys(data._deals).length > 0) {
              data.deals = data._deals;
              data._deals = null;
            }
          }
        });
      }

      // $("#depth").change(function () {
      //   attrs.hiddenChildLevel = parseInt($("#depth").val());
      //   hideLevels();
      //   update();
      // });
    });
  };

  //----------- PROTOTYPE FUNCTIONS  ----------------------
  d3.selection.prototype.patternify = function (params) {
    const container = this;
    const selector = params.selector;
    const elementTag = params.tag;
    const data = params.data || [selector];

    // Pattern in action
    let selection = container.selectAll("." + selector).data(data);
    selection.exit().remove();
    // selection = selection.enter().append(elementTag).merge(selection);
    selection.attr("class", selector);
    return selection;
  };

  // Custom radial layout
  d3.radial = function () {
    return function setProportions(root) {
      recurse(root, 0, 1);

      function recurse(node, min, max) {
        node.proportion = (max + min) / 2;
        if (!node.x) {
          // If node has parent, match entered node positions to it's parent
          if (node.parent) {
            node.x = node.parent.x;
          } else {
            node.x = 0;
          }
        }

        // If node had parent, match entered node positions to it's parent
        if (!node.y) {
          if (node.parent) {
            node.y = node.parent.y;
          } else {
            node.y = 0;
          }
        }

        // Recursively do the same for children
        if (node.children) {
          const offset = (max - min) / node.children.length;
          node.children.forEach(function (child, i, arr) {
            const newMin = min + offset * i;
            const newMax = newMin + offset;
            recurse(child, newMin, newMax);
          });
        }
      }
    };
  };

  // https://github.com/bumbeishvili/d3js-boilerplates#orderby
  Array.prototype.orderBy = function (func) {
    this.sort((a, b) => {
      a = func(a);
      b = func(b);
      if (typeof a === "string" || a instanceof String) {
        return a.localeCompare(b);
      }
      return a - b;
    });
    return this;
  };

  // ##########################  BOILEPLATE STUFF ################

  // Dynamic keys functions
  Object.keys(attrs).forEach((key) => {
    // Attach variables to main function
    return (main[key] = function (_) {
      const string = `attrs['${key}'] = _`;
      if (!arguments.length) {
        return eval(` attrs['${key}'];`);
      }
      eval(string);
      return main;
    });
  });

  // Set attrs as property
  main.attrs = attrs;

  // Debugging visuals
  main.debug = function (isDebug) {
    attrs.isDebug = isDebug;
    if (isDebug) {
      if (!window.charts) window.charts = [];
      window.charts.push(main);
    }
    return main;
  };

  // Exposed update functions
  main.data = function (value) {
    if (!arguments.length) return attrs.data;
    attrs.data = value;
    if (typeof updateData === "function") {
      updateData();
    }
    return main;
  };

  // Run visual
  main.run = function () {
    d3.selectAll(attrs.container).call(main);
    return main;
  };

  main.filter = function (filterParams) {
    if (!arguments.length) return attrs.filterParams;
    attrs.filterParams = filterParams;
    if (typeof filter === "function") {
      filter();
    }
    return main;
  };

  return main;
}

export function loadInvestorNetwork(investors, containerEl) {
  invData = investors;
  let x = renderChartCollapsibleNetwork()
    .svgHeight(invHeight)
    .svgWidth(invWidth)
    .container(containerEl)
    .data({ root: invData })
    .debug(true)
    .run();
  console.log(x);
  // d3.json(url, data => {
  //   console.log("Called3!");
  //   invData = updateReferences(data.data);
  //   console.log(invData);
  // let networkChart = renderChartCollapsibleNetwork()
  //   .svgHeight(invHeight)
  //   .svgWidth(invWidth)
  //   .container(containerEl)
  //   .data({ root: invData })
  //   .debug(true)
  //   .run();
  // });
}
