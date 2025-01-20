<script lang="ts">
  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    downloadCSV,
    downloadJSON,
    downloadSVG,
    type FileType,
  } from "$components/Data/Charts/utils"
  import StatusBarChart, { type DataType } from "$components/StatusBarChart.svelte"

  interface Props {
    title: string
    data: DataType[]
  }

  let { title, data }: Props = $props()

  const toCSV = (_data: DataType[]) => {
    console.log(_data)
    return [_data.map(x => x.name).join(","), _data.map(x => x.value).join(",")].join(
      "\n",
    )
  }

  let chartSVG: SVGElement | null = null
  const elementRendered = (e: SVGElement) => {
    chartSVG = e
  }
  const handleDownload = (fileType: FileType) => {
    // TODO Kurt
    // if ($tracker) $tracker.trackEvent("Chart", title, fileType)

    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(data, null, 2), title)
      case "csv":
        return downloadCSV(toCSV(data), title)
      default:
        return downloadSVG(chartSVG, fileType, title)
    }
  }
</script>

<ChartWrapper {title} ondownload={handleDownload}>
  <div class="w-full">
    <StatusBarChart {data} onrendered={elementRendered} />
  </div>
</ChartWrapper>
