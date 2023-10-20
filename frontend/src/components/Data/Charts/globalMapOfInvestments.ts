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
import type { Feature, Point } from "geojson"
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

export interface TooltipData {
  name: string
  nInvestors: number
  nTargets: number
  x: number
  y: number
}

const createInverseInvestments = (investments: Investments): Investments => {
  const inverseInvestments: Investments = {}

  Object.entries(investments).forEach(([targetCountryId, targetInvestment]) =>
    Object.entries(targetInvestment).forEach(([countryId, bucket]) => {
      inverseInvestments[countryId] = {
        ...inverseInvestments[countryId],
        [targetCountryId]: bucket,
      }
    }),
  )

  return inverseInvestments
}

type Country = Feature<Point, { name: string }>
const unique = <T>(arr: Array<T>) => [...new Set(arr)]

const isAntarctica = (countryId: number) => countryId === 10

export const createGlobalMapOfInvestments = (
  svgSelector: string,
  setCountryFilter: (id: string) => void,
  setTooltip: (data: TooltipData | undefined) => void,
) => {
  const width = 950
  const height = 500

  const svg = select(svgSelector)
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
  ).features

  const resetZoom = () =>
    gZoom
      .transition()
      .duration(500)
      .call(zoomFn.transform as any, zoomIdentity)

  const path: GeoPath = geoPath().projection(geoNaturalEarth1())

  let incomingInvestments: Investments
  let outgoingInvestments: Investments

  const drawCountries = () => {
    gCountries
      .selectAll<BaseType, Country>("*")
      .data(countries)
      .enter()
      .append("path")
      .attr("class", "country")
      .attr("d", path)
  }

  const injectData = (
    investments: Investments,
    selectedCountryId: number | undefined,
  ): void => {
    incomingInvestments = investments
    outgoingInvestments = createInverseInvestments(incomingInvestments)

    gCountries
      .selectAll<BaseType, Country>("*")
      .on("mouseover", async (event: MouseEvent, country) => {
        const eventTarget = event.target as HTMLElement
        const countryId = country.id ? +country.id : -1

        select(eventTarget).classed("hover", true)
        setTooltip({
          name: country.properties.name,
          nInvestors: Object.values(incomingInvestments[countryId] ?? {}).length,
          nTargets: Object.values(outgoingInvestments[countryId] ?? {}).length,
          x: event.pageX + 10,
          y: event.pageY - (isAntarctica(+countryId) ? 150 : 50),
        })
      })
      .on("mouseout", (event: MouseEvent) => {
        const eventTarget = event.target as HTMLElement
        select(eventTarget).classed("hover", false)
        setTooltip(undefined)
      })
      .on("click", (_, { id }) => {
        selectCountry(id)
        setCountryFilter(id)
      })

    if (selectedCountryId) {
      selectCountry(selectedCountryId.toString())
    }
  }

  const clearSelection = (): void => {
    gCountries
      .selectAll<BaseType, Country>(".country")
      .classed("selected-country", false)
      .classed("investor-country", false)
      .classed("target-country", false)
  }

  const selectCountry = (countryId: string): void => {
    clearSelection()
    resetZoom()

    const selectedCountry = countries.find(c => +c.id === +countryId)
    if (!selectedCountry) {
      console.error("Country not found in map", countryId)
      return
    }

    const investorCountries = unique(
      Object.keys(incomingInvestments[countryId] ?? {}),
    ).filter(key => key !== countryId)
    const targetCountries = unique(
      Object.keys(outgoingInvestments[countryId] ?? {}),
    ).filter(key => key !== countryId)

    const isSelected = ({ id }: Country) => +id === +countryId
    const isInvestor = ({ id }: Country) => investorCountries.includes((+id).toString())
    const isTarget = ({ id }: Country) => targetCountries.includes((+id).toString())

    gCountries
      .selectAll<BaseType, Country>(".country")
      .classed("selected-country", isSelected)
      .classed("investor-country", isInvestor)
      .classed("target-country", isTarget)
  }

  return { drawCountries, injectData, selectCountry }
}
