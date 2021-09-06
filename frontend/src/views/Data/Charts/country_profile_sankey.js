/**
 * https://gist.github.com/d3noob/31665aced416f27abca4fa46f5f4b568
 * https://observablehq.com/@d3/sankey-diagram
 * https://observablehq.com/@d3/brexit-voting?collection=@d3/d3-sankey
 * https://observablehq.com/@d3/sankey-diagram
 */
import { format, select } from "d3";
import { sankey, sankeyLinkHorizontal } from "d3-sankey";

export function do_the_sank(data) {
  // set the dimensions and margins of the graph
  var margin = { top: 10, right: 10, bottom: 10, left: 10 },
    width = 900 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

  const myformat = (d) => format(",.0f")(d);

  select("#sankey").selectAll().remove();

  let svg = select("#sankey")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  let d3sankey = sankey()
    .nodeId((d) => d.id)
    .nodeWidth(10)
    .nodePadding(20)
    .size([width, height]);
  let graph = d3sankey(data);

  const stroke_colors = {
    IN_OPERATION: "#f79425",
    PROJECT_ABANDONED: "#44bc87",
    PROJECT_NOT_STARTED: "#b8d435",
    STARTUP_PHASE: "#179a62",
  };

  let link = svg
    .append("g")
    .selectAll(".link")
    .data(graph.links)
    .enter()
    .append("path")
    .attr("class", "link")
    .attr("d", sankeyLinkHorizontal())
    .attr("stroke", (d) => stroke_colors[d.source.id])
    .attr("stroke-width", (d) => d.width);

  // add the link titles
  link
    .append("title")
    .text((d) => d.source.name + " → " + d.target.name + "\n" + myformat(d.value));

  // add in the nodes
  var node = svg
    .append("g")
    .selectAll(".node")
    .data(graph.nodes)
    .enter()
    .append("g")
    .attr("class", "node");

  // add the rectangles for the nodes
  node
    .append("rect")
    .attr("x", (d) => d.x0 + 2)
    .attr("y", (d) => d.y0)
    .attr("height", (d) => d.y1 - d.y0)
    .attr("width", d3sankey.nodeWidth() - 4)
    .style("fill", "#111")
    .style("stroke", null)
    .style("stroke-width", 0)
    .append("title")
    .text((d) => d.name + "\n" + myformat(d.value));

  // add in the title for the nodes
  node
    .append("text")
    .attr("x", (d) => d.x0 - 6)
    .attr("y", (d) => (d.y1 + d.y0) / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text((d) => d.name)
    .filter((d) => d.x0 < width / 2)
    .attr("x", (d) => d.x1 + 6)
    .attr("text-anchor", "start");
}
