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
  zoomIdentity,
} from "d3"
import type { BaseType, D3ZoomEvent, GeoPath, Selection } from "d3"
import type { Feature, GeoJsonProperties } from "geojson"
import { feature } from "topojson-client"
import type { Topology, GeometryCollection } from "topojson-specification"
import worldTopology from "world-atlas/countries-110m.json"

export interface Investments {
  [targetCountryId: string]: TargetInvestments
}

interface TargetInvestments {
  [investorCountryId: string]: {
    size: string
    count: number
  }
}

type Country = Feature

const getId = (country: Country) => +(country.id as string)
const hasId = (id: string) => (country: Country) => getId(country) === +id
const unique = <T>(arr: Array<T>) => [...new Set(arr)]

export const createGlobalMapOfInvestments = (
  svgSelector: string,
  setCountryFilter: (id: string) => void,
) => {
  const width = 950
  const height = 500

  // https://github.com/d3/d3-zoom
  // https://stackoverflow.com/questions/29320905
  // https://gist.github.com/KarolAltamirano/b54c263184be0516a59d6baf7f053f3e
  // https://d3-graph-gallery.com/graph/interactivity_zoom.html
  // https://www.freecodecamp.org/news/5d963b0a153e

  const zoomed = (event: D3ZoomEvent<Element, unknown>): void => {
    gZoom.attr("transform", event.transform.toString())
  }

  const zoomFn = zoom().scaleExtent([1, 3]).on("zoom", zoomed)

  const svg = select(svgSelector).attr("viewBox", `0 0 ${width} ${height}`)
  const gZoom = svg.append("g").call(zoomFn as any)

  // add background
  gZoom
    .append("rect")
    .attr("width", width)
    .attr("height", height)
    .attr("class", "background")

  const gCountries = gZoom.append("g").attr("class", "countries")
  const gMoneyLines = gZoom.append("g").attr("class", "money-lines")

  const countries: Country[] = feature(
    worldTopology as unknown as Topology,
    worldTopology.objects.countries as GeometryCollection<GeoJsonProperties>,
  ).features

  const resetZoom = () =>
    gZoom
      .transition()
      .duration(500)
      .call(zoomFn.transform as any, zoomIdentity)

  const path: GeoPath = geoPath().projection(geoNaturalEarth1())

  let investments: Investments

  const drawCountries = () => {
    gCountries
      .selectAll<BaseType, Country>("*")
      .data(countries)
      .enter()
      .append("path")
      .attr("class", "country")
      .attr("data-id", getId)
      .attr("d", path)

    addMarkers(svg, 5)
  }

  const injectData = (
    data: Investments,
    selectedCountryId: number | undefined,
  ): void => {
    investments = data

    gCountries
      .selectAll<BaseType, Country>("*")
      .on("mouseover", (event: MouseEvent) =>
        select(event.target as HTMLElement).classed("hover", true),
      )
      .on("mouseout", (event: MouseEvent) =>
        select(event.target as HTMLElement).classed("hover", false),
      )
      .on("click", (event: PointerEvent) => {
        const countryId = (event.target as HTMLElement).dataset.id as string
        selectCountry(countryId)
        setCountryFilter(countryId)
      })

    if (selectedCountryId) {
      selectCountry(selectedCountryId.toString())
    }
  }

  const getInvestorAndTargetCountries = (
    selectedCountry: Country,
  ): { investorCountries: Country[]; targetCountries: Country[] } => {
    const investorCountries: Country[] = []
    const targetCountries: Country[] = []

    Object.entries<TargetInvestments>(investments).forEach(
      ([targetCountryId, targetInvestments]) => {
        const targetCountry = countries.find(hasId(targetCountryId))
        if (!targetCountry) return

        Object.keys(targetInvestments).forEach(investorCountryId => {
          const investorCountry = countries.find(hasId(investorCountryId))

          if (!investorCountry || targetCountry === investorCountry) return
          if (targetCountry === selectedCountry) investorCountries.push(investorCountry)
          if (investorCountry === selectedCountry) targetCountries.push(targetCountry)
        })
      },
    )

    return {
      investorCountries: unique(investorCountries),
      targetCountries: unique(targetCountries),
    }
  }

  const clearSelection = (): void => {
    gMoneyLines.selectAll<BaseType, Country>("*").remove()
    gCountries
      .selectAll<BaseType, Country>(".country")
      .classed("selected-country", false)
      .classed("investor-country", false)
      .classed("target-country", false)
  }

  const selectCountry = (countryId: string): void => {
    clearSelection()
    resetZoom()

    const selectedCountry = countries.find(hasId(countryId))
    if (!selectedCountry) {
      console.error("Country not found in map", countryId)
      return
    }

    const { investorCountries, targetCountries } =
      getInvestorAndTargetCountries(selectedCountry)

    gMoneyLines
      .selectAll<BaseType, Country>(".investor-country-line")
      .data(investorCountries)
      .enter()
      .append("path")
      .attr("class", "investor-country-line")
      .attr("d", investorCountry => moneyLine(investorCountry, selectedCountry))

    gMoneyLines
      .selectAll<BaseType, Country>(".target-country-line")
      .data(targetCountries)
      .enter()
      .append("path")
      .attr("class", "target-country-line")
      .attr("d", targetCountry => moneyLine(selectedCountry, targetCountry))

    gCountries
      .selectAll<BaseType, Country>(".country")
      .classed("selected-country", country => country === selectedCountry)
      .classed("investor-country", country => investorCountries.includes(country))
      .classed("target-country", country => targetCountries.includes(country))
  }

  const moneyLine = (source: Country, target: Country): string | null =>
    path({
      type: "LineString",
      coordinates: [geoCentroid(source), geoCentroid(target)],
    })

  return { drawCountries, injectData, selectCountry }
}

export function addMarkers(
  svg: Selection<BaseType, unknown, HTMLElement, unknown>,
  size = 10,
): void {
  const defs = svg.append("defs")
  const marker_factory = (name: string) =>
    defs
      .append("marker")
      .attr("id", name)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 0)
      .attr("refY", 0)
      .attr("markerWidth", size)
      .attr("markerHeight", size)
      .attr("orient", "auto-start-reverse")
      .attr("markerUnits", "userSpaceOnUse")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
  marker_factory("incoming-marker")
  marker_factory("outgoing-marker")
}
