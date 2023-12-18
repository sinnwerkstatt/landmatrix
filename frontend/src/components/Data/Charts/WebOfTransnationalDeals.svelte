<script lang="ts">
  import { onMount } from "svelte"

  import { LandMatrixRadialSpider } from "$lib/data/charts/webOfTransnationalDeals"
  import type { EdgeBundlingData } from "$lib/data/charts/webOfTransnationalDeals"
  import { filters } from "$lib/filters"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import { downloadJSON, downloadSVG } from "$components/Data/Charts/utils"

  export let title = ""
  export let deals: EdgeBundlingData

  let svgComp: SVGElement

  const redrawSpider = (deals: EdgeBundlingData, countryId: number | undefined): void =>
    LandMatrixRadialSpider(
      svgComp,
      deals,
      countryId,
      countryId => ($filters.country_id = +countryId),
    )

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(deals, null, 2), title)
      case "csv":
        return // NOT SUPPORTED
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }

  $: $filters && redrawSpider(deals, $filters.country_id)

  onMount(() => redrawSpider(deals, $filters.country_id))
</script>

<ChartWrapper
  {title}
  disableCSV
  wrapperClasses="mx-auto xl:w-4/5"
  on:download={handleDownload}
>
  <svg id="web-of-transnational-deals" bind:this={svgComp} />
</ChartWrapper>

<style lang="css">
  :global(svg #incoming-marker) {
    @apply fill-purple;
  }

  :global(svg #outgoing-marker) {
    @apply fill-red;
  }

  :global(svg path.incoming-highlighted) {
    @apply stroke-purple stroke-2;
    marker-start: url(#incoming-marker);
  }

  :global(svg path.outgoing-highlighted) {
    @apply stroke-red stroke-2;
    marker-start: url(#outgoing-marker);
  }

  :global(svg path.incoming-permahighlight) {
    @apply stroke-purple stroke-[3];
    marker-start: url(#incoming-marker);
  }

  :global(svg path.outgoing-permahighlight) {
    @apply stroke-red stroke-2;
    marker-start: url(#outgoing-marker);
  }

  :global(svg text.incoming-highlighted) {
    @apply cursor-pointer fill-purple font-bold;
  }

  :global(svg text.outgoing-highlighted) {
    @apply cursor-pointer fill-red font-bold;
  }

  :global(svg text.incoming-permahighlight) {
    @apply cursor-pointer fill-purple font-bold;
  }

  :global(svg text.outgoing-permahighlight) {
    @apply cursor-pointer fill-red font-bold;
  }

  :global(svg text.incoming-permahighlight.outgoing-permahighlight) {
    @apply cursor-pointer fill-gray-700 font-bold;
  }
</style>
