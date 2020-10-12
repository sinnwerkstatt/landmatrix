// source https://observablehq.com/@d3/hierarchical-edge-bundling

import * as d3 from "d3";
import { primary_color } from "/colors";

let width = 954;
let radius = width / 2;
let colorin = "#9c4ce8";
let colorout = primary_color;
let colornone = "#ccc";
let tree = d3.cluster().size([2 * Math.PI, radius - 100]);
let line = d3
  .lineRadial()
  .curve(d3.curveBundle.beta(0.85))
  .radius((d) => d.y)
  .angle((d) => d.x);

let selectedCountry = null;

function id(node) {
  return `${node.parent ? id(node.parent) + "." : ""}${node.data.name}`;
}

function bilink(root) {
  const map = new Map(root.leaves().map((d) => [id(d), d]));
  for (const d of root.leaves()) {
    d.incoming = [];
    d.outgoing = d.data.imports.map((i) => [d, map.get(i)]);
  }
  for (const d of root.leaves()) for (const o of d.outgoing) o[1].incoming.push(o);
  return root;
}

export function LandMatrixRadialSpider(data_hierarchical, container) {
  const svg = d3
    .select(container)
    .attr("viewBox", [-width / 2, -width / 2, width, width]);

  const root = tree(
    bilink(
      d3
        .hierarchy(data_hierarchical)
        .sort(
          (a, b) =>
            d3.ascending(a.height, b.height) || d3.ascending(a.data.name, b.data.name)
        )
    )
  );

  const link = svg
    .append("g")
    .attr("stroke", colornone)
    .attr("fill", "none")
    .selectAll("path")
    .data(root.leaves().flatMap((leaf) => leaf.outgoing))
    .join("path")
    .style("mix-blend-mode", "multiply")
    .attr("d", ([i, o]) => line(i.path(o)))
    .each(function (d) {
      d.path = this;
    });

  function mouseover_event(event, d) {
    link.style("mix-blend-mode", null);
    d3.select(this).attr("font-weight", "bold");
    d3.selectAll(d.incoming.map((d) => d.path))
      .attr("stroke", colorin)
      .attr("stroke-width", 3)
      .raise();
    d3.selectAll(d.incoming.map(([d]) => d.text))
      .attr("fill", colorin)
      .attr("font-weight", "bold");
    d3.selectAll(d.outgoing.map((d) => d.path))
      .attr("stroke", colorout)
      .attr("stroke-width", 3)
      .raise();
    d3.selectAll(d.outgoing.map(([, d]) => d.text))
      .attr("fill", colorout)
      .attr("font-weight", "bold");
  }

  function mouseout_event(event, d) {
    link.style("mix-blend-mode", "multiply");
    d3.select(this).attr("font-weight", null);
    d3.selectAll(d.incoming.map((d) => d.path))
      .attr("stroke", null)
      .attr("stroke-width", 1);
    d3.selectAll(d.incoming.map(([d]) => d.text))
      .attr("fill", null)
      .attr("font-weight", null);
    d3.selectAll(d.outgoing.map((d) => d.path))
      .attr("stroke", null)
      .attr("stroke-width", 1);
    d3.selectAll(d.outgoing.map(([, d]) => d.text))
      .attr("fill", null)
      .attr("font-weight", null);
  }

  svg
    .append("g")
    .selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr(
      "transform",
      (d) => `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0)`
    )
    .append("text")
    .attr("dy", "0.31em")
    .attr("data-id", (d) => d.data.id)
    .attr("x", (d) => (d.x < Math.PI ? 6 : -6))
    .attr("text-anchor", (d) => (d.x < Math.PI ? "start" : "end"))
    .attr("transform", (d) => (d.x >= Math.PI ? "rotate(180)" : null))
    .text((d) => d.data.name)
    .each(function (d) {
      d.text = this;
    })
    .on("mouseover", mouseover_event)
    .on("mouseout", mouseout_event)
    .on("mousedown", (d) => {
      selectedCountry = d.target.dataset.id;
      console.log("selected Country:", selectedCountry);
    })
    .call((text) =>
      text.append("title").text(
        (d) => `${d.data.name}
      ${d.outgoing.length} investing countries
      investing in ${d.incoming.length} countries`
      )
    );
}
