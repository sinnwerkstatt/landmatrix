<script lang="ts" module>
  export type DataType = {
    name: string
    value: string
    label: string
    fillColor: string
  }
</script>

<script lang="ts">
  import * as d3 from "d3"
  import { onMount } from "svelte"

  interface Props {
    data: DataType[]
    width?: number
    onrendered?: (element: SVGElement) => void
  }
  let { data, width = 600, onrendered }: Props = $props()

  let chart: SVGElement | undefined = $state()

  onMount(() => {
    if (!data.length) return

    const height = data.length * 60

    const tooltip = d3
      .select("body")
      .append("div")
      .attr(
        "class",
        "absolute top-0 rounded border bg-white p-3 text-black opacity-0 dark:bg-gray-800 dark:text-white",
      )
      .style("pointer-events", "none")

    const svg = d3
      .select(chart!)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("width", width)
      .attr("height", height)
      .append("g")

    const yScale = d3
      .scaleBand()
      .domain(data.map(d => d.name))
      .range([0, height])
      .padding(0.2)

    const labelGroup = svg
      .append("g")
      .style("font-size", "18px")
      .style("font-weight", "400")
      .style("fill", "black")
      .attr("class", "dark:fill-white transition-colors")
    labelGroup
      .selectAll(".status")
      .data(data)
      .join("text")
      .attr("x", 0)
      .attr("y", d => yScale(d.name)! + 4)
      // .attr("dy", "0.35em")
      .attr("class", "dark:fill-white transition-colors")
      .text(d => d.name)

    // const labelGroupWidth = labelGroup.node()!.getBoundingClientRect().width
    // labelGroup.attr("transform", `translate(${width - labelGroupWidth},0)`)

    const percentageGroup = svg
      .append("g")
      .attr("font-weight", "700")
      .attr("fill", "black")
      .attr("class", "dark:fill-white transition-colors")
    percentageGroup
      .selectAll(".value-label")
      .data(data)
      .join("text")
      .attr("x", 0)
      .attr("y", d => yScale(d.name)! + 24)

      .text(d => d.value + "%")
    const percentageGroupWidth = percentageGroup.node()!.getBoundingClientRect().width
    percentageGroup.attr("transform", `translate(${width - percentageGroupWidth},0)`)

    const xScale = d3
      .scaleLinear()
      .domain([0, Math.max(...data.map(_x => +_x.value))])
      .range([0, width - percentageGroupWidth - 20])

    svg
      .selectAll("rect")
      .data(data)
      .join("rect")
      .attr("x", 0)
      .attr("y", d => yScale(d.name)! + 10)
      .attr("width", d => Math.max(2, xScale(+d.value)))
      .attr("height", 20)
      .attr("fill", d => d.fillColor)
      .attr("rx", 4)
      .attr("ry", 4)
      .on("mouseover", (event, d) => {
        tooltip
          .html(d.label)
          .style("left", event.pageX + 10 + "px")
          .style("top", event.pageY - 28 + "px")
          .transition()
          .duration(200)
          .style("opacity", 0.96)
      })
      .on("mouseout", () => tooltip.transition().duration(500).style("opacity", 0))

    onrendered?.(chart!)
  })
</script>

<svg class="status-bar-chart size-full" bind:this={chart}></svg>
