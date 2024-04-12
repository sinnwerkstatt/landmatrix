/**
 *
 */
import { axisLeft, descending, max, range, scaleBand, scaleLinear, select } from "d3"

export type DynamicsDataPoint = {
  name: string
  value: number
}

export class DynamicsOfDeal {
  private readonly width = 816
  private readonly height = 680
  private readonly margin = { top: 30, right: 0, bottom: 10, left: 300 }

  do_the_graph(svgElement: SVGElement, data: DynamicsDataPoint[]): void {
    if (!svgElement) return
    select(svgElement).selectAll("*").remove() // clear

    data = data.sort((a, b) => descending(a.value, b.value))
    const svg = select(svgElement)
      // there is a little extra padding at the bottom (+ 10)
      .attr("viewBox", `0 0 ${this.width + 20} ${this.height + 20 + 10}`)
      .attr("height", "100%")
      .attr("width", "100%")
      .style("background-color", "white")
      .append("g")

    const y = scaleBand()
      .domain(range(data.length).map(x => x.toString()))
      .rangeRound([this.margin.top, this.height - this.margin.bottom])
      .padding(0.1)

    const x = scaleLinear()
      .domain([0, max(data, d => d.value) ?? 0])
      .range([this.margin.left, this.width - this.margin.right])

    const format = (val: number) =>
      `${Math.round(val).toLocaleString("fr").replace(",", ".")} ha`

    const bar = svg.selectAll("g").data(data).enter().append("g")

    bar
      .attr("fill", "#fc941f")
      .append("rect")
      .attr("x", x(0))
      .attr("y", (d, i) => y(i.toString()) ?? 0)
      .attr("width", d => x(d.value) - x(0) || 0)
      .attr("height", y.bandwidth())

    bar
      .append("text")
      .attr("x", d => x(d.value))
      .attr("y", (d, i) => (y(i.toString()) ?? 0) + y.bandwidth() / 2)
      .text(d => format(d.value))
      .attr("dy", "0.35em")
      .attr("dx", function (d) {
        const barWidth = x(d.value) - x(0)
        const textWidth = Math.ceil(Math.max(0, this.getBBox().width))
        if (textWidth > barWidth + 5) return 5
        return -textWidth - 5
      })
      .attr("fill", (d, idx, z) =>
        +(z[idx].getAttribute("dx") || 1) > 0 ? "black" : "white",
      )

    svg
      .append("g")
      .attr("transform", `translate(${this.margin.left},0)`)
      .call(
        axisLeft(y)
          .tickFormat(i => data[+i].name)
          .tickSizeOuter(0),
      )
      .attr("font-size", "1rem")
      .attr("font-family", "inherit")
  }
}

export const toCSV = (data: DynamicsDataPoint[]): string =>
  data.map(entry => [entry.name, entry.value].join(",") + "\n").join("")

export const toJSON = (data: DynamicsDataPoint[]): string =>
  JSON.stringify(data, null, 2)
