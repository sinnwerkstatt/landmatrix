<script lang="ts">
  import type { Chart, ChartData } from "chart.js"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    downloadCanvas,
    downloadCSV,
    downloadJSON,
  } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import StatusPieChart from "$components/StatusPieChart.svelte"

  export let title: string
  export let data: ChartData<"pie">
  export let unit = ""

  let chart: Chart<"pie">

  const toCSV = (data: ChartData<"pie">) =>
    [data.labels?.join(","), ...data.datasets.map(set => set.data.join(","))].join("\n")

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(data, null, 2), title)
      case "csv":
        return downloadCSV(toCSV(data), title)
      case "svg":
        return // Not supported
      default:
        if (chart) return downloadCanvas(chart.canvas, fileType, title)
    }
  }
</script>

<ChartWrapper disableSVG {title} on:download={handleDownload}>
  <StatusPieChart bind:chart {data} {unit} />
</ChartWrapper>
