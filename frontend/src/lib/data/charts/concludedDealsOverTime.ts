import * as d3 from "d3"
import * as R from "ramda"

import {
  getConcludedRange,
  getCurrentSize,
  getInitialSize,
  hasBeenConcluded,
  hasConcludedDate,
} from "$lib/data/dealUtils"
import type { Dated } from "$lib/data/itemUtils"
import { isDated, parseDate } from "$lib/data/itemUtils"
import type { ContractSizeItem, Deal } from "$lib/types/deal"

const getCurrentYear: () => number = R.pipe(
  R.constructN(0, Date),
  R.invoker(0, "getFullYear"),
)

export const createYears: (startYear: number) => number[] = startYear =>
  R.range(startYear, getCurrentYear())

export const createYearSizeMap: (deal: Deal) => Record<string, number> = R.pipe<
  [Deal],
  ContractSizeItem[],
  Dated<ContractSizeItem>[],
  Dated<ContractSizeItem>[],
  Record<string, number>
>(
  R.propOr([], "contract_size"),
  R.filter<ContractSizeItem, Dated<ContractSizeItem>>(isDated),
  R.sortWith<Dated<ContractSizeItem>>([
    R.ascend(R.prop<string>("date")),
    R.ascend(R.has("current")),
  ]),
  R.reduce(
    (acc, { date, area }) => R.assoc(R.toString(parseDate(date)), area, acc),
    {},
  ),
)

export const createBuckets =
  (years: number[]) =>
  (deal: Deal): Bucket[] => {
    const [concludedYear, canceledYear] = getConcludedRange(deal)
    const initialSize = getInitialSize(deal)

    const yearSizeMap = createYearSizeMap(deal)
    return R.mapAccum(
      (lastSize, year) => {
        if (year < concludedYear) {
          return [lastSize, { size: 0, count: 0 }]
        }
        if (canceledYear && year > canceledYear) {
          return [lastSize, { size: 0, count: 0 }]
        }
        const size = yearSizeMap[year] ?? lastSize
        return [size, { size, count: 1 }]
      },
      initialSize,
      years,
    )[1]
  }

export interface Bucket {
  size: number
  count: number
}

export interface ConcludedDealsOverTimeAccumulator {
  buckets: Bucket[]
  excluded: Bucket
}

export const createConcludedDealsOverTimeReducer = (years: number[]) => {
  return (
    acc: ConcludedDealsOverTimeAccumulator,
    deal: Deal,
  ): ConcludedDealsOverTimeAccumulator => {
    // filtered
    if (!hasBeenConcluded(deal)) {
      return acc
    }
    // excluded
    if (!hasConcludedDate(deal)) {
      return R.evolve(
        {
          excluded: {
            size: R.add(getCurrentSize(deal)),
            count: R.add(1),
          },
        },
        acc,
      )
    }
    // valid
    return R.evolve(
      { buckets: R.zipWith(R.mergeWith(R.add), createBuckets(years)(deal)) },
      acc,
    )
  }
}

export interface ChartData {
  excluded: Bucket
  sizes: [Date, number][]
  counts: [Date, number][]
}

const asDate: (year: number) => Date = R.pipe(R.toString, R.constructN(1, Date))

export const createChartData = (startYear: number, deals: Deal[]): ChartData => {
  const years = createYears(startYear)

  const data = R.reduce(createConcludedDealsOverTimeReducer(years), {
    buckets: R.map(() => ({ size: 0, count: 0 }), years),
    excluded: { size: 0, count: 0 },
  })(deals)

  return {
    excluded: data.excluded,
    sizes: R.zipWith(
      (year: number, { size }: Bucket) => [asDate(year), size],
      years,
      data.buckets,
    ),
    counts: R.zipWith(
      (year: number, { count }: Bucket) => [asDate(year), count],
      years,
      data.buckets,
    ),
  }
}

export const clearGraph = (svgElement: SVGElement): void => {
  d3.select(svgElement).selectAll("*").remove()
}

export const drawGraph = (
  svgElement: SVGElement,
  chartData: [Date, number][],
): void => {
  const margin = { top: 10, right: 30, bottom: 30, left: 50 }
  const width = 600
  const height = 300

  const svg = d3
    .select(svgElement)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("height", "100%")
    .attr("width", "100%")
    .style("background-color", "white")

  const xMin = chartData[0][0]
  const xMax = chartData[chartData.length - 1][0]
  const x = d3
    .scaleUtc()
    .domain([xMin, xMax])
    .range([margin.left, width - margin.right])

  const xAxis = d3.axisBottom(x)

  const yMax = Math.max(...chartData.map(d => d[1]))
  const y = d3
    .scaleLinear()
    .domain([0, (yMax > 5 ? yMax : 5) * 1.1])
    .range([height - margin.bottom, margin.top])

  const yTicks = y.ticks().filter(Number.isInteger)
  const yAxis = d3
    .axisLeft(y)
    .tickSizeOuter(0)
    .tickValues(yTicks)
    .tickFormat(d3.format(yMax > 10_000 ? ".1e" : "d"))

  svg
    .append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(xAxis)
    .attr("font-family", "inherit")
    .attr("stroke", "black")
    .attr("stroke-width", 0.1)

  svg
    .append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(yAxis)
    .attr("font-family", "inherit")
    .attr("stroke", "black")
    .attr("stroke-width", 0.1)

  const area = d3
    .area<[Date, number]>()
    .x(d => x(d[0]))
    .y0(y(0))
    .y1(d => y(d[1]))

  svg
    .append("path")
    .datum(chartData)
    .attr("stroke", "current-color")
    .attr("stroke-width", 1.5)
    .attr("d", area)

  const xAxisGrid = xAxis
    .tickSizeInner(margin.top + margin.bottom - height)
    .tickFormat(() => "")

  const yAxisGrid = yAxis
    .tickSizeInner(margin.left + margin.right - width)
    .tickFormat(() => "")

  svg
    .append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .attr("stroke-width", 0.3)
    .call(xAxisGrid)

  svg
    .append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .attr("stroke-width", 0.3)
    .call(yAxisGrid)
}
