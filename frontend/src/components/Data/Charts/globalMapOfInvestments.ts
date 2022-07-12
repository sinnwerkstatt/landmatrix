/**
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
  geoCentroid,
  geoNaturalEarth1, // geoOrthographic,
  geoPath,
  select,
  zoom,
} from "d3";
import type { D3ZoomEvent, GeoPath } from "d3";
import type * as GeoJSON from "geojson";
import { feature } from "topojson-client";
import world from "world-atlas/countries-110m.json";
import { addMarkers } from "./utils";

export class GlobalInvestmentMap {
  private readonly width = 950;
  private readonly height = 500;
  private readonly projection;
  private readonly path: GeoPath;
  private readonly svg;
  private readonly countries;
  private readonly moneylines;
  private frontCountries: unknown;
  private selectedCountry?: unknown;
  private global_map_of_investments: unknown;

  constructor(svg_selector: string) {
    this.projection = geoNaturalEarth1();
    // this.projection = geoEqualEarth();

    this.countries = feature(world, world.objects.countries).features;
    console.log("countries", { countries: this.countries });
    this.path = geoPath().projection(this.projection);

    this.svg = select(svg_selector).attr("viewBox", `0 0 ${this.width} ${this.height}`);
    this.moneylines = this.svg.append("g").attr("class", "moneylines");
    console.warn("MONEYLS", this.moneylines);

    addMarkers(this.svg);
  }

  public doTheThing(global_map_of_investments): void {
    this.global_map_of_investments = global_map_of_investments;

    console.log("doTheThing");
    this.frontCountries = this.svg
      .selectAll(".country")
      .data(this.countries)
      .enter()
      .insert("path", ".line")
      .attr("class", "country")
      .attr("data-id", (d) => d.id)
      .attr("d", this.path)
      .on("mouseover", (e: Event) => select(e.target).classed("hover", true))
      .on("mouseout", (e: Event) => select(e.target).classed("hover", false))
      .on("click", (e: Event) => this.countrySelect(e));

    this.svg.call(
      zoom().on("zoom", (e) => {
        this.zoomed(e);
      })
    );
  }

  countrySelect(e: PointerEvent): void {
    // reset playing field
    this.moneylines.selectAll("*").remove();
    this.svg.selectAll(".country").attr("class", "country");

    const selectedCountryId = +e.target?.dataset.id;
    this.selectedCountry = this.countries.find((c) => +c.id === selectedCountryId);

    const investorCountries: GeoJSON.Feature[] = [];
    const targetCountries: GeoJSON.Feature[] = [];

    Object.entries(this.global_map_of_investments).forEach(([k, v]) => {
      Object.keys(v).forEach((x) => {
        if (+k === +selectedCountryId && +x !== +selectedCountryId)
          investorCountries.push(this.countries.find((c) => +c.id === +x));
        if (+x === +selectedCountryId && +k !== +selectedCountryId)
          targetCountries.push(this.countries.find((c) => +c.id === +k));
        // if (+x === +selectedCountryId) targetCountries.push(v);
      });
    });

    if (investorCountries.length > 0) {
      console.log("investorCountries", { investorCountries });
      this.moneylines
        .selectAll(".lines")
        .data(investorCountries)
        .enter()
        .append("path")
        .attr("class", "investor-country-line")
        .attr("d", (target) => this.moneyLine(this.selectedCountry, target));
    }

    if (targetCountries.length > 0) {
      console.log("targetCountries", { targetCountries });
      this.moneylines
        .selectAll(".lines")
        .data(targetCountries)
        .enter()
        .append("path")
        .attr("class", "target-country-line")
        .attr("d", (target) => this.moneyLine(this.selectedCountry, target));
    }

    this.svg
      .selectAll(".country")
      .classed("investor-country", (d) => investorCountries.includes(d));
    this.svg
      .selectAll(".country")
      .classed("target-country", (d) => targetCountries.includes(d));
    this.svg
      .selectAll(".country")
      .classed("selected-country", (d) => selectedCountryId === +d.id);
    // select(this).classed("target-country", true);
  }

  moneyLine(source: GeoJSON.Feature, target: GeoJSON.Feature): string | null {
    return this.path({
      type: "LineString",
      coordinates: [geoCentroid(source), geoCentroid(target)],
    });
  }

  zoomed(event: D3ZoomEvent<Element, unknown>): void {
    this.svg.attr("transform", event.transform);
  }
}
