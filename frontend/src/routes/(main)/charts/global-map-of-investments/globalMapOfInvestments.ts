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
import type { Feature, Geometry } from "geojson"
import { feature } from "topojson-client"
import type { Topology, GeometryCollection } from "topojson-specification"
import worldTopology from "world-atlas/countries-110m.json"

export interface Investments {
  incoming: CountryInvestmentsMap
  outgoing: CountryInvestmentsMap
}

export interface CountryInvestmentsMap {
  [countryId: string]: {
    [countryId: string]: {
      size: number
      count: number
    }
  }
}

export interface GlobalMap {
  selectCountry: (id: number | undefined) => void
}

interface Country extends Feature<Geometry, { name: string }> {
  id: number
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
  const gZoom = svg.append("g").call(zoomFn as any)

  // add background
  gZoom
    .append("rect")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "background")

  const gCountries = gZoom.append("g").attr("class", "countries")

  const countries = feature(
    worldTopology as unknown as Topology,
    worldTopology.objects.countries as GeometryCollection<{ name: string }>,
  ).features.map(country => ({ ...country, id: +(country.id as string) })) as Country[]

  const resetZoom = () =>
    gZoom
      .transition()
      .duration(500)
      .call(zoomFn.transform as any, zoomIdentity)

  const path: GeoPath = geoPath().projection(geoNaturalEarth1())

  gCountries
    .selectAll<BaseType, Country>("*")
    .data(countries)
    .enter()
    .append("path")
    .attr("class", "country")
    .attr("d", path)

  gCountries
    .selectAll<BaseType, Country>("*")
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
      .selectAll<BaseType, Country>(".country")
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

    const isSelected = ({ id }: Country) => id === countryId
    const isInvestor = ({ id }: Country) => investorCountries.includes(id.toString())
    const isTarget = ({ id }: Country) => targetCountries.includes(id.toString())

    gCountries
      .selectAll<BaseType, Country>(".country")
      .classed("selected-country", isSelected)
      .classed("investor-country", isInvestor)
      .classed("target-country", isTarget)
  }

  return { selectCountry }
}
