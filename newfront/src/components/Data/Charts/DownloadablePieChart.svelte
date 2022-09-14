<script lang="ts">
  import { Chart } from "chart.js"
  import type { ChartData } from "chart.js"

  import ChartWrapper from "$components/Data/Charts/ChartWrapper.svelte"
  import { downloadJSON, downloadPNG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import StatusPieChart from "$components/StatusPieChart.svelte"

  export let title: string
  export let data: ChartData<"pie">
  export let unit = ""

  let chart: Chart<"pie">

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(data, null, 2), title)
      case "csv":
        return // TODO
      case "png":
        return downloadPNG(chart.toBase64Image(), title)
      default:
        return // TODO
    }
  }
</script>

<ChartWrapper {title} on:download={handleDownload}>
  <StatusPieChart bind:chart {data} {unit} />
</ChartWrapper>
