// source https://observablehq.com/@d3/hierarchical-edge-bundling

import { addMarkers } from "./utils";
import {
  ascending,
  cluster,
  hierarchy,
  select,
  selectAll,
  curveBundle,
  lineRadial,
} from "d3";

let width = 954;
let radius = width / 2;
let colornone = "#ccc";
let tree = cluster().size([2 * Math.PI, radius - 100]);
let line = lineRadial()
  .curve(curveBundle.beta(0.85))
  .radius((d) => d.y)
  .angle((d) => d.x);

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

export function LandMatrixRadialSpider(
  data_hierarchical,
  container,
  selectedCountry,
  updateCountryFn
) {
  selectAll("g > *").remove();
  const svg = select(container).attr("viewBox", [-width / 2, -width / 2, width, width]);

  const root = tree(
    bilink(
      hierarchy(data_hierarchical).sort(
        (a, b) => ascending(a.height, b.height) || ascending(a.data.name, b.data.name)
      )
    )
  );
  addMarkers(svg);

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

  function selectCountry(target, highlight_class = "highlighted") {
    let selection = select(target);
    if (selection.size() === 0) return;
    link.style("mix-blend-mode", null);
    selection.attr("font-weight", "bold");
    let d = selection.datum();

    let incoming_paths = selectAll(d.incoming.map((d) => d.path));
    incoming_paths.classed(`incoming-${highlight_class}`, true);
    incoming_paths.raise();
    let incoming_texts = selectAll(d.incoming.map(([d]) => d.text));
    incoming_texts.classed(`incoming-${highlight_class}`, true);

    let outgoing_paths = selectAll(d.outgoing.map((d) => d.path));
    outgoing_paths.classed(`outgoing-${highlight_class}`, true);

    outgoing_paths.raise();
    let outgoing_texts = selectAll(d.outgoing.map(([, d]) => d.text));
    outgoing_texts.classed(`outgoing-${highlight_class}`, true);
  }

  function mouseout_event(target) {
    let selection = select(target);
    if (selection.size() === 0) return;
    link.style("mix-blend-mode", "multiply");
    selection.attr("font-weight", null);
    let d = selection.datum();
    selectAll(d.incoming.map((d) => d.path)).classed("incoming-highlighted", false);
    selectAll(d.incoming.map(([d]) => d.text)).classed("incoming-highlighted", false);
    selectAll(d.outgoing.map((d) => d.path)).classed("outgoing-highlighted", false);
    selectAll(d.outgoing.map(([, d]) => d.text)).classed("outgoing-highlighted", false);

    selectCountry("#text_" + selectedCountry, "permahighlight");
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
    .attr("id", (d) => `text_${d.data.id}`)
    .attr("x", (d) => (d.x < Math.PI ? 6 : -6))
    .attr("text-anchor", (d) => (d.x < Math.PI ? "start" : "end"))
    .attr("transform", (d) => (d.x >= Math.PI ? "rotate(180)" : null))
    .text((d) => d.data.name)
    .each(function (d) {
      d.text = this;
    })
    .on("mouseover", (event) => selectCountry(event.currentTarget))
    .on("mouseout", (event) => mouseout_event(event.currentTarget))
    .on("mousedown", (d) => {
      selectedCountry =
        selectedCountry !== d.target.dataset.id ? d.target.dataset.id : null;
      updateCountryFn(selectedCountry);
    })
    .call((text) =>
      text.append("title").text(
        (d) => `${d.data.name}
      ${d.outgoing.length} investing countries
      investing in ${d.incoming.length} countries`
      )
    );

  selectCountry("#text_" + selectedCountry, "permahighlight");
}
