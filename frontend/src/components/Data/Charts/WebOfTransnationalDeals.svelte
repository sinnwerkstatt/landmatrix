<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { onMount } from "svelte"

  import type { EdgeBundlingData } from "$lib/data/charts/webOfTransnationalDeals"
  import { LandMatrixRadialSpider } from "$lib/data/charts/webOfTransnationalDeals"
  import { filters } from "$lib/filters"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import type { FileType } from "$components/Data/Charts/utils"
  import { downloadJSON, downloadSVG } from "$components/Data/Charts/utils"

  interface Props {
    title?: string
    deals: EdgeBundlingData
  }

  let { title = "", deals }: Props = $props()

  let svgComp: SVGElement | undefined = $state()

  const redrawSpider = (
    deals: EdgeBundlingData,
    countryId: number | undefined,
  ): void => {
    if (!svgComp) return

    LandMatrixRadialSpider(svgComp, deals, countryId, countryId => {
      $filters.country_id = countryId
      $filters.region_id = undefined
    })
  }

  const handleDownload = (fileType: FileType) => {
    if ($tracker) $tracker.trackEvent("Chart", "Web of transnational deals", fileType)
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(deals, null, 2), title)
      case "csv":
        return // NOT SUPPORTED
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }

  $effect(() => {
    redrawSpider(deals, $filters.country_id)
  })

  onMount(() => redrawSpider(deals, $filters.country_id))
</script>

<ChartWrapper
  disableCSV
  ondownload={handleDownload}
  {title}
  wrapperClasses="mx-auto xl:w-4/5"
>
  <svg bind:this={svgComp} id="web-of-transnational-deals">
    <style lang="postcss">
      #incoming-marker {
        @apply fill-purple;
      }

      #outgoing-marker {
        @apply fill-red;
      }

      path.incoming-highlighted {
        @apply stroke-purple stroke-2;
        marker-start: url(#incoming-marker);
      }

      path.outgoing-highlighted {
        @apply stroke-red stroke-2;
        marker-start: url(#outgoing-marker);
      }

      path.incoming-permahighlight {
        @apply stroke-purple stroke-[3];
        marker-start: url(#incoming-marker);
      }

      path.outgoing-permahighlight {
        @apply stroke-red stroke-2;
        marker-start: url(#outgoing-marker);
      }

      text.incoming-highlighted {
        @apply cursor-pointer fill-purple font-bold;
      }

      text.outgoing-highlighted {
        @apply cursor-pointer fill-red font-bold;
      }

      text.incoming-permahighlight {
        @apply cursor-pointer fill-purple font-bold;
      }

      text.outgoing-permahighlight {
        @apply cursor-pointer fill-red font-bold;
      }

      text.incoming-permahighlight.outgoing-permahighlight {
        @apply cursor-pointer fill-gray-700 font-bold;
      }
    </style>
  </svg>
</ChartWrapper>
