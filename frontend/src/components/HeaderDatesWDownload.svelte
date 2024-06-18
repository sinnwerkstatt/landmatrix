<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull, InvestorHull } from "$lib/types/data"

  import DetailsSummary from "$components/DetailsSummary.svelte"
  import HeaderDates from "$components/HeaderDates.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"

  export let obj: DealHull | InvestorHull

  $: isDeal = "fully_updated_at" in obj
  const downloadLink = (format: string): string =>
    `/api/legacy_export/?deal_id=${obj.id}&subset=UNFILTERED&format=${format}`
</script>

<!-- TODO Kurt: track individual deal downloads? -->
<div class="flex items-center gap-8">
  {#if isDeal}
    <DetailsSummary>
      <div class="btn btn-violet flex items-center gap-1" slot="summary">
        <DownloadIcon class="mx-1 my-0.5 h-6 w-6" />
      </div>
      <ul
        class="absolute z-50 mt-0.5 rounded border border-gray-400 bg-white shadow-2xl dark:bg-gray-700"
        slot="details"
      >
        <li class="my-5">
          <a
            class="px-4 py-2 text-black hover:text-violet-500 dark:text-white dark:hover:text-violet-200"
            data-sveltekit-reload
            href={downloadLink("xlsx")}
          >
            <DownloadIcon />
            {$_("Excel document")}
          </a>
        </li>
        <li class="my-5">
          <a
            class="px-4 py-2 text-black hover:text-violet-500 dark:text-white dark:hover:text-violet-200"
            data-sveltekit-reload
            href={downloadLink("csv")}
          >
            <DownloadIcon />
            {$_("CSV file")}
          </a>
        </li>
        <li class="my-5">
          <a
            class="px-4 py-2 text-black hover:text-violet-500 dark:text-white dark:hover:text-violet-200"
            data-sveltekit-reload
            href={`/api/gis_export/locations/?deal_id=${obj.id}&subset=UNFILTERED&format=json`}
          >
            <DownloadIcon />
            {$_("Locations (as geojson)")}
          </a>
        </li>
        <li class="my-5 block">
          <a
            class="px-4 py-2 text-black hover:text-violet-500 dark:text-white dark:hover:text-violet-200"
            data-sveltekit-reload
            href={`/api/gis_export/areas/?deal_id=${obj.id}&subset=UNFILTERED&format=json`}
          >
            <DownloadIcon />
            {$_("Areas (as geojson)")}
          </a>
        </li>
      </ul>
    </DetailsSummary>
  {/if}
  <HeaderDates {obj} />
</div>
