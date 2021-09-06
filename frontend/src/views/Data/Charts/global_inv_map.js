/**
 *
 * inspirational resources
 * https://codepen.io/chrislaskey/pen/jqabBQ
 * https://observablehq.com/@d3/world-tour
 * https://dev.to/sriramvsharma/drawing-a-world-map-in-13-lines-of-code-368a
 * https://bl.ocks.org/d3noob/727ed3b5a2020a6d5b0aa5412a719bf5
 * http://using-d3js.com/05_01_paths.html
 * https://bl.ocks.org/mbostock/7ea1dde508cec6d2d95306f92642bc42
 * https://observablehq.com/@jk979/versor-dragging
 * https://www.jasondavies.com/maps/rotate/
 * http://bl.ocks.org/tlfrd/df1f1f705c7940a6a7c0dca47041fec8
 */

import { addMarkers } from "./utils";
import {
  drag,
  geoCentroid,
  geoGraticule,
  geoOrthographic,
  geoPath,
  pointer,
  select,
  zoom,
} from "d3";
import { feature } from "topojson-client";
import versor from "versor";
import world from "world-atlas/countries-110m.json";

function globe_drag(update) {
  let v0, r0, q0;

  function dragstarted(event) {
    v0 = versor.cartesian(projection.invert(pointer(event, this)));
    r0 = projection.rotate();
    q0 = versor(r0);
  }

  function dragged(event) {
    let v1 = versor.cartesian(projection.rotate(r0).invert(pointer(event, this)));
    let q1 = versor.multiply(q0, versor.delta(v0, v1));
    let r1 = versor.rotation(q1);
    projection.rotate(r1);
    update();
  }
  return drag().on("start", dragstarted).on("drag", dragged);
}

// export function mydrag(projection) {
//   let v0, q0, r0, a0, l;
//
//   function pointer(event, that) {
//     const t = pointers(event, that);
//
//     if (t.length !== l) {
//       l = t.length;
//       if (l > 1) a0 = Math.atan2(t[1][1] - t[0][1], t[1][0] - t[0][0]);
//       dragstarted.apply(that, [event, that]);
//     }
//
//     // For multitouch, average positions and compute rotation.
//     if (l > 1) {
//       const x = mean(t, (p) => p[0]);
//       const y = mean(t, (p) => p[1]);
//       const a = Math.atan2(t[1][1] - t[0][1], t[1][0] - t[0][0]);
//       return [x, y, a];
//     }
//
//     return t[0];
//   }
//
//   function dragstarted(event) {
//     v0 = versor.cartesian(projection.invert(pointer(event, this)));
//     q0 = versor((r0 = projection.rotate()));
//   }
//
//   function dragged(event) {
//     const p = pointer(event, this);
//     const v1 = versor.cartesian(projection.rotate(r0).invert(p));
//     const delta = versor.delta(v0, v1);
//     let q1 = versor.multiply(q0, delta);
//
//     // For multitouch, compose with a rotation around the axis.
//     if (p[2]) {
//       const d = (p[2] - a0) / 2;
//       const s = -Math.sin(d);
//       const c = Math.sign(Math.cos(d));
//       q1 = versor.multiply([Math.sqrt(1 - s * s), 0, 0, c * s], q1);
//     }
//
//     projection.rotate(versor.rotation(q1));
//
//     // In vicinity of the antipode (unstable) of q0, restart.
//     if (delta[0] < 0.7) dragstarted.apply(this, [event, this]);
//   }
//
//   return drag().on("start", dragstarted).on("drag", dragged);
// }

let width = 500;
let height = 500;
let scale = height / 2.0;
// geoMercator
let projection = geoOrthographic()
  .scale(scale)
  .translate([width / 2, height / 2])
  .clipAngle(90);

// let centroid = geoPath().projection((d) => d).centroid;

let countries = feature(world, world.objects.countries).features;

let path = geoPath().projection(projection);
let graticule = geoGraticule().extent([
  [-180, -90],
  [180 - 0.1, 90 - 0.1],
]);

function moneyLine(source, target) {
  return path({
    type: "LineString",
    coordinates: [geoCentroid(source), geoCentroid(target)],
  });
}

export function doTheThing(svg_selector, global_map_of_investments) {
  let svg = select(svg_selector).attr("width", width).attr("height", height);

  svg
    .append("circle")
    .attr("class", "world-outline")
    .attr("cx", width / 2)
    .attr("cy", height / 2)
    .attr("r", projection.scale());

  addMarkers(svg);

  // draw the backside of the earth.
  projection.clipAngle(180);
  let backLine = svg
    .append("path")
    .datum(graticule)
    .attr("class", "back-line")
    .attr("d", path);
  let backCountry = svg
    .selectAll(".back-country")
    .data(countries)
    .enter()
    .insert("path", ".back-line")
    .attr("class", "back-country")
    .attr("d", path);

  // draw the frontside
  projection.clipAngle(90);
  let line = svg.append("path").datum(graticule).attr("class", "line").attr("d", path);
  console.log({ countries });
  let country = svg
    .selectAll(".country")
    .data(countries)
    .enter()
    .insert("path", ".line")
    .attr("class", "country")
    .attr("data-id", (d) => d.id)
    .attr("d", path)
    .on("click", countrySelect);

  let source;
  let targets;
  let moneylines;
  function countrySelect(e) {
    // reset playing field
    if (moneylines) moneylines.remove();
    svg.selectAll(".country").attr("class", "country");

    let source_id = +e.target.dataset.id;
    console.log({ source_id });
    source = countries.find((c) => +c.id === source_id);
    targets = Object.keys(global_map_of_investments[source_id]).map((k) =>
      countries.find((c) => +c.id !== source_id && +c.id === +k)
    );
    console.log({ source, targets });

    if (targets) {
      moneylines = svg
        .append("g")
        .attr("class", "moneylines")
        .selectAll(".lines")
        .data(targets)
        .enter()
        .append("path")
        .attr("class", "moneyline")
        .attr("d", (target) => moneyLine(source, target));
    }

    svg.selectAll(".country").classed("investor-country", (d) => targets.includes(d));
    svg.selectAll(".country").classed("target-country", (d) => source_id === +d.id);
    select(this).classed("target-country", true);
  }

  function refresh() {
    projection.clipAngle(180);
    backCountry.attr("d", path);
    backLine.attr("d", path);

    projection.clipAngle(90);
    country.attr("d", path);
    line.attr("d", path);
    if (moneylines) moneylines.attr("d", (target) => moneyLine(source, target));
  }

  const zoomed = (event) => {
    console.log();
    console.log("zoomed");
    scale = event.sourceEvent.deltaY > 0 ? scale * 0.9 : scale * 1.1;
    projection.scale(scale);
    svg.select(".world-outline").attr("r", scale);
    refresh();
  };
  svg.call(globe_drag(refresh));
  svg.call(zoom().on("zoom", zoomed));
}
