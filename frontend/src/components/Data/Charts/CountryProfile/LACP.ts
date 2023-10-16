import * as d3 from "d3"

import { IoIGroup } from "$lib/types/deal"

export type Data = {
  key: string
  label: string
  value: number
  groupKey: string
  groupLabel: string
  color: string // rgb
}[]

export type Group = {
  key: string
  label: string
  color: string
}

export const IOI_GROUP_COLORS: {
  [key in IoIGroup]: string
} = {
  // copied from tailwind.config
  [IoIGroup.FORESTRY]: "#477722",
  [IoIGroup.AGRICULTURE]: "#E7CC41",
  [IoIGroup.RENEWABLE_ENERGY]: "#AA70DD",
  [IoIGroup.OTHER]: "#E8726A",
}

export const drawGraph = async (
  node: SVGElement,
  data: Data,
  groups: Group[],
  title: string,
  xLabel: string,
  yLabel: string,
) => {
  const margin = { top: 50, right: 10, bottom: 150, left: 90 }
  const width = 1000
  const height = 500

  const svg = d3
    .select(node)
    .attr("viewBox", `0 0 ${width} ${height}`)
    .attr("height", "100%")
    .attr("width", "100%")

  const x = d3
    .scaleBand()
    .range([margin.left, width - margin.right])
    .domain(data.map(d => d.label))
    .padding(0.1)

  const xAxis = d3.axisBottom(x)

  svg
    .append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(xAxis)
    .attr("stroke-width", 0.1)
    .attr("font-family", "inherit")
    .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end")

  const yMax = d3.max(data.map(d => d.value)) ?? 0
  const y = d3
    .scaleLinear()
    .domain([0, (yMax > 5 ? yMax : 5) * 1.1])
    .range([height - margin.bottom, margin.top])

  const yTicks = y.ticks(4).filter(Number.isInteger)
  const yAxis = d3
    .axisLeft(y)
    .tickSizeOuter(0)
    .tickValues(yTicks)
    .tickFormat(d3.format(yMax > 10_000 ? ".1e" : "d"))

  svg
    .append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(yAxis)
    .attr("font-family", "inherit")
    .attr("stroke-width", 0.1)

  const yAxisGrid = yAxis
    .tickSizeInner(margin.left + margin.right - width)
    .tickFormat(() => "")

  svg
    .append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .attr("stroke-width", 0.1)
    .call(yAxisGrid)

  svg
    .selectAll("myBars")
    .data(data)
    .enter()
    .append("rect")
    .attr("x", d => x(d.label) as number)
    .attr("y", d => y(d.value))
    .attr("width", x.bandwidth())
    .attr("height", d => height - margin.bottom - y(d.value))
    .attr("data-group", d => d.groupKey)
    .attr("stroke-width", 0.1)
    .attr("fill", d => d.color)

  // title & axis labels
  const titlePos = [width / 2, margin.top / 2]
  svg
    .append("g")
    .attr("transform", `translate(${titlePos.join(",")})`)
    .append("text")
    .text(title)
    .attr("font-size", "1.25rem")
    .attr("fill", "currentColor")
    .attr("text-anchor", "middle")
    .style("alignment-baseline", "middle")

  const xLabelPos = [width / 2, height - 10]
  svg
    .append("text")
    .attr("transform", `translate(${xLabelPos.join(",")})`)
    .attr("fill", "currentColor")
    .style("text-anchor", "middle")
    .style("alignment-baseline", "bottom")
    .text(xLabel)

  const yLabelPos = [25, margin.top + (height - margin.top - margin.bottom) / 2]
  svg
    .append("text")
    .attr("transform", `translate(${yLabelPos.join(",")})rotate(-90)`)
    .attr("fill", "currentColor")
    .style("text-anchor", "middle")
    .text(yLabel)

  // legend
  const dotSize = 20
  const legendPos = [(3 / 4) * width - margin.right, margin.top + 15]
  const legend = svg.append("g").attr("transform", `translate(${legendPos.join(",")})`)

  legend
    .append("rect")
    .attr("width", width / 4 - 10)
    .attr("height", groups.length * (dotSize + 5) + 5)
    .attr("fill", "white")
    .attr("stroke-width", 0.1)

  legend
    .selectAll("myDots")
    .data(groups)
    .enter()
    .append("rect")
    .attr("x", 5)
    .attr("y", (d, i) => 5 + i * (dotSize + 5))
    .attr("width", dotSize)
    .attr("height", dotSize)
    .attr("data-group", d => d.key)
    .attr("stroke-width", 0.1)
    .attr("fill", d => d.color)

  legend
    .selectAll("myLabels")
    .data(groups)
    .enter()
    .append("text")
    .attr("x", dotSize + 10)
    .attr("y", (d, i) => 5 + i * (dotSize + 5) + dotSize / 2 + 2)
    .text(d => d.label)
    .attr("fill", "currentColor")
    .attr("text-anchor", "left")
    .style("alignment-baseline", "middle")
}
