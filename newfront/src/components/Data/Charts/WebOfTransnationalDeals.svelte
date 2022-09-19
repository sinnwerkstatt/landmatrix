<script lang="ts">
  import { onMount } from "svelte"

  import { LandMatrixRadialSpider } from "$lib/data/charts/webOfTransnationalDeals"
  import type { EdgeBundlingData } from "$lib/data/charts/webOfTransnationalDeals"
  import { filters } from "$lib/filters"

  import ChartWrapper from "$components/Data/Charts/ChartWrapper.svelte"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import { downloadImage, downloadJSON } from "$components/Data/Charts/utils"

  export let title = ""
  export let deals: EdgeBundlingData

  let svgComp: SVGElement

  const redrawSpider = (deals, country_id): void =>
    LandMatrixRadialSpider(
      svgComp,
      deals,
      country_id,
      country => ($filters.country_id = +country),
    )

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(deals, null, 2), title)
      case "csv":
        return // TODO
      default:
        return downloadImage(svgComp, fileType, title)
    }
  }

  $: $filters && redrawSpider(deals, $filters.country_id)

  onMount(() => redrawSpider(deals, $filters.country_id))
</script>

<ChartWrapper {title} disableCSV wrapperClasses="w-3/4" on:download={handleDownload}>
  <svg id="web-of-transnational-deals" bind:this={svgComp}>
    <!-- Include styles with fallback colors in svg for export-->
    <style>
      #incoming-marker {
        fill: var(--color-lm-orange, #fc941dff);
      }

      #outgoing-marker {
        fill: var(--color-lm-investor, #43b6b5ff);
      }

      path.incoming-highlighted {
        stroke: var(--color-lm-orange, #fc941dff);
        stroke-width: 2;
        marker-start: url(#incoming-marker);
      }

      path.outgoing-highlighted {
        stroke: var(--color-lm-investor, #43b6b5ff);
        stroke-width: 2;
        marker-start: url(#outgoing-marker);
      }

      path.incoming-permahighlight {
        stroke: var(--color-lm-orange, #fc941dff);
        stroke-width: 2.5;
        marker-start: url(#incoming-marker);
      }

      path.outgoing-permahighlight {
        stroke: var(--color-lm-investor, #43b6b5ff);
        stroke-width: 2.5;
        marker-start: url(#outgoing-marker);
      }

      text.incoming-highlighted {
        font-size: 14px;
        cursor: pointer;
        font-weight: bold;
        fill: var(--color-lm-orange, #fc941dff);
      }

      text.outgoing-highlighted {
        font-size: 14px;
        cursor: pointer;
        font-weight: bold;
        fill: var(--color-lm-investor, #43b6b5ff);
      }
    </style>
  </svg>
</ChartWrapper>
