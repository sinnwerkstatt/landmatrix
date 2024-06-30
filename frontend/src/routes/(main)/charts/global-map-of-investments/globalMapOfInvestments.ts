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
  geoNaturalEarth1, // geoOrthographic,
  geoPath,
  select,
  zoom,
  zoomIdentity,
} from "d3"
import type { BaseType, D3ZoomEvent, GeoPath } from "d3"

import { createCountryFeatureList, type CountryFeature } from "$components/Map/world"

export interface Investments {
  incoming: Country2CountryInvestmentsMap
  outgoing: Country2CountryInvestmentsMap
}
export interface CountryInvestments {
  incoming: CountryInvestmentsMap
  outgoing: CountryInvestmentsMap
}
export interface Country2CountryInvestmentsMap {
  [countryId: string]: CountryInvestmentsMap
}

export interface CountryInvestmentsMap {
  [countryId: string]: {
    size: number
    count: number
  }
}

export interface GlobalMap {
  selectCountry: (id: number | undefined) => void
}

export const createGlobalMapOfInvestments = (
  svgElement: SVGElement,
  investments: Investments,
  setSelectedCountryId: (id: number | undefined) => void,
  setHoverCountryId: (id: number | undefined) => void,
) => {
  const width = 950
  const height = 500

  const svg = select(svgElement)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .style("width", "100%")

  // https://github.com/d3/d3-zoom
  // https://stackoverflow.com/questions/29320905
  // https://gist.github.com/KarolAltamirano/b54c263184be0516a59d6baf7f053f3e
  // https://d3-graph-gallery.com/graph/interactivity_zoom.html
  // https://www.freecodecamp.org/news/5d963b0a153e
  const zoomed = (event: D3ZoomEvent<Element, unknown>): void => {
    gZoom.attr("transform", event.transform.toString())
  }
  const zoomFn = zoom().scaleExtent([1, 3]).on("zoom", zoomed)
  const gZoom = svg.append("g").call(zoomFn as never)

  // add background
  gZoom
    .append("rect")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "background")

  const gCountries = gZoom.append("g").attr("class", "countries")

  const resetZoom = () =>
    gZoom
      .transition()
      .duration(500)
      .call(zoomFn.transform as never, zoomIdentity)

  const path: GeoPath = geoPath().projection(geoNaturalEarth1())

  gCountries
    .selectAll<BaseType, CountryFeature>("*")
    .data(createCountryFeatureList())
    .enter()
    .append("path")
    .attr("class", "country")
    .attr("d", path)

  gCountries
    .selectAll<BaseType, CountryFeature>("*")
    .on("mouseover", async (event: MouseEvent, { id }) => {
      const eventTarget = event.target as HTMLElement
      select(eventTarget).classed("hover", true)
      setHoverCountryId(id)

      select("#country-tooltip")
        .style("left", `${event.pageX + 10}px`)
        .style("top", `${event.pageY - 50}px`)
    })
    .on("mouseout", (event: MouseEvent) => {
      const eventTarget = event.target as HTMLElement
      select(eventTarget).classed("hover", false)
      setHoverCountryId(undefined)
    })
    .on("click", (_, { id }) => {
      selectCountry(id)
      setSelectedCountryId(id)
    })

  const clearSelection = (): void => {
    gCountries
      .selectAll<BaseType, CountryFeature>(".country")
      .classed("selected-country", false)
      .classed("investor-country", false)
      .classed("target-country", false)
  }

  const selectCountry = (countryId: number | undefined): void => {
    clearSelection()
    resetZoom()

    if (!countryId) {
      // console.error("Country not found in map", countryId)
      return
    }

    setSelectedCountryId(countryId)

    const investorCountries = Object.keys(investments["incoming"][countryId] ?? {})
    const targetCountries = Object.keys(investments["outgoing"][countryId] ?? {})

    const isSelected = ({ id }: CountryFeature) => id === countryId
    const isInvestor = ({ id }: CountryFeature) =>
      investorCountries.includes(id.toString())
    const isTarget = ({ id }: CountryFeature) => targetCountries.includes(id.toString())

    gCountries
      .selectAll<BaseType, CountryFeature>(".country")
      .classed("selected-country", isSelected)
      .classed("investor-country", isInvestor)
      .classed("target-country", isTarget)
  }

  // legend
  const legendPos = [10, height - 80]
  const legend = svg.append("g").attr("transform", `translate(${legendPos.join(",")})`)

  legend
    .append("rect")
    .attr("width", 180)
    .attr("height", 70)
    .attr("fill", "white")
    .attr("stroke-width", 0.3)
    .attr("stroke", "black")

  legend
    .append("rect")
    .attr("x", 10)
    .attr("y", 10)
    .attr("width", 20)
    .attr("height", 20)
    .attr("class", "target-country")

  legend
    .append("rect")
    .attr("x", 10)
    .attr("y", 40)
    .attr("width", 20)
    .attr("height", 20)
    .attr("class", "investor-country")

  legend
    .append("text")
    .attr("x", 40)
    .attr("y", 25)
    .text("Target country")
    .attr("fill", "currentColor")
    .style("alignment-baseline", "top")

  legend
    .append("text")
    .attr("x", 40)
    .attr("y", 55)
    .text("Investor country")
    .attr("fill", "currentColor")
    .style("alignment-baseline", "top")

  return { selectCountry }
}
