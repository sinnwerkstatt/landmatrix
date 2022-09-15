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

<ChartWrapper {title} wrapperClasses="w-3/4" on:download={handleDownload}>
  <svg id="web-of-transnational-deals" bind:this={svgComp} />
</ChartWrapper>

<!--suppress CssUnusedSymbol, CssUnknownTarget -->
<style>
  :global(#incoming-marker) {
    fill: var(--color-lm-orange);
  }
  :global(#outgoing-marker) {
    fill: var(--color-lm-investor);
  }

  :global(path.incoming-highlighted) {
    stroke: var(--color-lm-orange);
    stroke-width: 2;
    marker-start: url(#incoming-marker);
  }
  :global(path.outgoing-highlighted) {
    stroke: var(--color-lm-investor);
    stroke-width: 2;
    marker-start: url(#outgoing-marker);
  }

  :global(path.incoming-permahighlight) {
    stroke: var(--color-lm-orange);
    stroke-width: 2.5;
    marker-start: url(#incoming-marker);
  }
  :global(path.outgoing-permahighlight) {
    stroke: var(--color-lm-investor);
    stroke-width: 2.5;
    marker-start: url(#outgoing-marker);
  }

  :global(text.incoming-highlighted) {
    font-size: 14px;
    cursor: pointer;
    font-weight: bold;
    fill: var(--color-lm-orange);
  }
  :global(text.outgoing-highlighted) {
    font-size: 14px;
    cursor: pointer;
    font-weight: bold;
    fill: var(--color-lm-investor);
  }
</style>
