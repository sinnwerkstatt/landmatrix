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
  GeoGeometryObjects,
  geoGraticule,
  GeoGraticuleGenerator,
  geoOrthographic,
  GeoPath,
  geoPath,
  pointer,
  select,
  zoom,
} from "d3";
import { feature } from "topojson-client";
import versor from "versor";
import world from "world-atlas/countries-110m.json";
import type { DragBehavior } from "d3-drag";
import type { GeoJSONObject } from "@turf/turf";

export class GlobalInvolvementMap {
  private width: number;
  private readonly height: number;
  private scale: number;
  private projection: any;
  private readonly path: GeoPath;
  private graticule: GeoGraticuleGenerator;
  private svg: any;
  private countries: any;
  private backGraticules: any;
  private frontGraticules: any;
  private backCountries: any;
  private frontCountries: any;
  private moneylines: any;
  private sourceCountry?: GeoJSONObject;
  private global_map_of_investments: any;

  constructor(svg_selector: string) {
    this.width = 500;
    this.height = 500;
    this.scale = this.height / 2.0;
    // geoMercator
    this.projection = geoOrthographic()
      .scale(this.scale)
      .translate([this.width / 2, this.height / 2])
      .clipAngle(90);

    // let centroid = geoPath().projection((d) => d).centroid;

    this.countries = feature(world, world.objects.countries).features;

    this.path = geoPath().projection(this.projection);
    this.graticule = geoGraticule().extent([
      [-180, -90],
      [180 - 0.1, 90 - 0.1],
    ]);

    this.svg = select(svg_selector)
      .attr("width", this.width)
      .attr("height", this.height);
    this.svg
      .append("circle")
      .attr("class", "world-outline")
      .attr("cx", this.width / 2)
      .attr("cy", this.height / 2)
      .attr("r", this.projection.scale());

    addMarkers(this.svg);
  }

  public doTheThing(global_map_of_investments): void {
    this.global_map_of_investments = global_map_of_investments;
    // draw the backside of the earth.
    this.projection.clipAngle(180);
    this.backGraticules = this.svg
      .append("path")
      .datum(this.graticule)
      .attr("class", "back-line")
      .attr("d", this.path);
    this.backCountries = this.svg
      .selectAll(".back-country")
      .data(this.countries)
      .enter()
      .insert("path", ".back-line")
      .attr("class", "back-country")
      .attr("d", this.path);

    // draw the frontside
    this.projection.clipAngle(90);
    this.frontGraticules = this.svg
      .append("path")
      .datum(this.graticule)
      .attr("class", "line")
      .attr("d", this.path);
    // console.log({ countries });
    this.frontCountries = this.svg
      .selectAll(".country")
      .data(this.countries)
      .enter()
      .insert("path", ".line")
      .attr("class", "country")
      .attr("data-id", (d) => d.id)
      .attr("d", this.path)
      .on("click", (e) => this.countrySelect(e));

    this.svg.call(this.globe_drag());
    this.svg.call(
      zoom().on("zoom", (e) => {
        this.zoomed(e);
      })
    );
  }

  countrySelect(e: Event): void {
    // reset playing field
    if (this.moneylines) this.moneylines.remove();
    this.svg.selectAll(".country").attr("class", "country");

    const sourceCountryId = +e.target.dataset.id;
    console.log({ sourceCountryId });
    this.sourceCountry = this.countries.find((c) => +c.id === sourceCountryId);
    const targetCountries = Object.keys(
      this.global_map_of_investments[sourceCountryId]
    ).map((k) => this.countries.find((c) => +c.id !== sourceCountryId && +c.id === +k));
    console.log({ sourceCountry: this.sourceCountry, targetCountries });

    if (targetCountries) {
      this.moneylines = this.svg
        .append("g")
        .attr("class", "moneylines")
        .selectAll(".lines")
        .data(targetCountries)
        .enter()
        .append("path")
        .attr("class", "moneyline")
        .attr("d", (target) => this.moneyLine(this.sourceCountry, target));
    }

    this.svg
      .selectAll(".country")
      .classed("investor-country", (d) => targetCountries.includes(d));
    this.svg
      .selectAll(".country")
      .classed("target-country", (d) => sourceCountryId === +d.id);
    // select(this).classed("target-country", true);
  }

  globe_drag(): DragBehavior<Element, unknown, unknown> {
    let v0: number, r0: number, q0: number;
    const proj = this.projection;
    const callback = () => {
      this.refresh();
    };
    return drag()
      .on("start", function (event) {
        v0 = versor.cartesian(proj.invert(pointer(event, this)));
        r0 = proj.rotate();
        q0 = versor(r0);
      })
      .on("drag", function (event) {
        const v1 = versor.cartesian(proj.rotate(r0).invert(pointer(event, this)));
        const q1 = versor.multiply(q0, versor.delta(v0, v1));
        const r1 = versor.rotation(q1);
        proj.rotate(r1);
        callback();
      });
  }

  moneyLine(
    sourceCountry: GeoGeometryObjects,
    target: GeoGeometryObjects
  ): string | null {
    return this.path({
      type: "LineString",
      coordinates: [geoCentroid(sourceCountry), geoCentroid(target)],
    });
  }

  refresh(): void {
    this.projection.clipAngle(180);
    this.backCountries.attr("d", this.path);
    this.backGraticules.attr("d", this.path);

    this.projection.clipAngle(90);
    this.frontCountries.attr("d", this.path);
    this.frontGraticules.attr("d", this.path);
    if (this.moneylines)
      this.moneylines.attr("d", (target) => this.moneyLine(this.sourceCountry, target));
  }

  zoomed(event): void {
    this.scale = event.sourceEvent.deltaY > 0 ? this.scale * 0.9 : this.scale * 1.1;
    this.projection.scale(this.scale);
    this.svg.select(".world-outline").attr("r", this.scale);
    this.refresh();
  }
}
