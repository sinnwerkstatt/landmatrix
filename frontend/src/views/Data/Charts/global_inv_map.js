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

import {
  drag,
  geoCentroid,
  geoGraticule,
  geoInterpolate,
  geoOrthographic,
  geoPath,
  mean,
  pointer,
  pointers,
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
let projection = geoOrthographic()
  .scale(height / 2.0)
  .translate([width / 2, height / 2])
  .clipAngle(90);

let centroid = geoPath().projection((d) => d).centroid;

let countries = feature(world, world.objects.countries).features;

let path = geoPath().projection(projection);
let graticule = geoGraticule().extent([
  [-180, -90],
  [180 - 0.1, 90 - 0.1],
]);

export function doTheThing(svg_selector) {
  let svg = select(svg_selector).attr("width", width).attr("height", height);

  svg
    .append("circle")
    .attr("class", "world-outline")
    .attr("cx", width / 2)
    .attr("cy", height / 2)
    .attr("r", projection.scale());

  // let rotate = d3_geo_greatArcInterpolator();

  let i = -1;
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

  projection.clipAngle(90);
  let line = svg.append("path").datum(graticule).attr("class", "line").attr("d", path);
  let country = svg
    .selectAll(".country")
    .data(countries)
    .enter()
    .insert("path", ".line")
    .attr("class", "country")
    .attr("d", path);

  let ug = countries.find((c) => c.properties.name === "Uganda");
  let chile = countries.find((c) => c.properties.name === "Chile");
  let argentina = countries.find((c) => c.properties.name === "Argentina");
  function lineToLondon(source, target) {
    return path({
      type: "LineString",
      coordinates: [geoCentroid(source), geoCentroid(target)],
    });
  }
  let source = ug;
  let targets = [chile, argentina];
  let moneylines = svg
    .append("g")
    .attr("class", "moneylines")
    .selectAll(".lines")
    .data(targets)
    .enter()
    .append("path")
    .attr("class", "moneyline")
    .attr("d", (target) => lineToLondon(source, target));

  function refresh() {
    projection.clipAngle(180);
    backCountry.attr("d", path);
    backLine.attr("d", path);

    projection.clipAngle(90);
    country.attr("d", path);
    line.attr("d", path);
    moneylines.attr("d", (target) => lineToLondon(source, target));
    // svg.selectAll(".land").attr("d", path);
    // svg.selectAll(".countries path").attr("d", path);
    // svg.selectAll(".graticule").attr("d", path);
    // svg.selectAll(".point").attr("d", path);
    // svg.selectAll(".lines").attr("d", (d) => { if (d) { return lineToLondon(d); }});
    // position_labels();
  }

  const zoomed = (event) => {
    console.log({ event });
    console.log("zoomed");
    // projection.translate(event.translate).scale(event.scale);
    // refresh();
  };
  svg.call(globe_drag(refresh));
  svg.call(zoom().on("zoom", zoomed));
}

// svg
//   .call(
//     mydrag(projection)
//       .on("drag.render", () => {})
//       .on("end.render", () => {})
//   )
//   .call(() => {})
//   .node();

// // step();
//
// // function step() {
// //   if (++i >= countries.length) i = 0;
// //
// //   // title.text(countries[i].id);
// //
// //   country.transition().style("fill", function (d, j) {
// //     return j === i ? "red" : "#737368";
// //   });
// //
// //   transition()
// //     .delay(250)
// //     .duration(1250)
// //     .tween("rotate", function () {
// //       let point = centroid(countries[i]);
// //       rotate
// //         .source(projection.rotate())
// //         .target([-point[0], -point[1]])
// //         .distance();
// //       return function (t) {
// //         projection.rotate(rotate(t)).clipAngle(180);
// //         backCountry.attr("d", path);
// //         backLine.attr("d", path);
// //
// //         projection.rotate(rotate(t)).clipAngle(90);
// //         country.attr("d", path);
// //         line.attr("d", path);
// //       };
// //     })
// //     .transition()
// //     .each("end", step);
// // }
//
// let d3_radians = Math.PI / 180;
//
// function d3_geo_greatArcInterpolator() {
//   let x0, y0, cy0, sy0, kx0, ky0, x1, y1, cy1, sy1, kx1, ky1, d, k;
//
//   function interpolate(t) {
//     var B = Math.sin((t *= d)) * k,
//       A = Math.sin(d - t) * k,
//       x = A * kx0 + B * kx1,
//       y = A * ky0 + B * ky1,
//       z = A * sy0 + B * sy1;
//     return [
//       Math.atan2(y, x) / d3_radians,
//       Math.atan2(z, Math.sqrt(x * x + y * y)) / d3_radians,
//     ];
//   }
//
//   interpolate.distance = function () {
//     if (d == null)
//       k =
//         1 /
//         Math.sin(
//           (d = Math.acos(
//             Math.max(-1, Math.min(1, sy0 * sy1 + cy0 * cy1 * Math.cos(x1 - x0)))
//           ))
//         );
//     return d;
//   };
//
//   interpolate.source = function (_) {
//     var cx0 = Math.cos((x0 = _[0] * d3_radians)),
//       sx0 = Math.sin(x0);
//     cy0 = Math.cos((y0 = _[1] * d3_radians));
//     sy0 = Math.sin(y0);
//     kx0 = cy0 * cx0;
//     ky0 = cy0 * sx0;
//     d = null;
//     return interpolate;
//   };
//
//   interpolate.target = function (_) {
//     var cx1 = Math.cos((x1 = _[0] * d3_radians)),
//       sx1 = Math.sin(x1);
//     cy1 = Math.cos((y1 = _[1] * d3_radians));
//     sy1 = Math.sin(y1);
//     kx1 = cy1 * cx1;
//     ky1 = cy1 * sx1;
//     d = null;
//     return interpolate;
//   };
//
//   return interpolate;
// }
