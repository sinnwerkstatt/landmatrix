<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes"

  import DetailsSummary from "$components/DetailsSummary.svelte"
  import HeaderDates from "$components/HeaderDates.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"

  export let obj: DealHull | InvestorHull

  $: isDeal = "fully_updated_at" in obj
  const downloadLink = (format: string): string =>
    `/api/legacy_export/?deal_id=${obj.id}&subset=UNFILTERED&format=${format}`
</script>

<div class="flex items-center gap-8">
  {#if isDeal}
    <DetailsSummary>
      <div class="butn butn-violet flex items-center gap-1" slot="summary">
        <DownloadIcon class="mx-1 my-0.5 h-6 w-6" />
      </div>
      <ul
        class="absolute z-50 mt-1 rounded border border-gray-400 bg-white px-4 py-2 shadow-2xl dark:bg-gray-700"
        slot="details"
      >
        <li class="my-1">
          <div class="flex items-center gap-2">
            <a
              target="_blank"
              href={downloadLink("xlsx")}
              rel="noreferrer"
              class=" px-4 py-2"
              data-sveltekit-reload
            >
              <DownloadIcon />
              {$_("Excel document")}
            </a>
          </div>
        </li>
        <li class="my-1">
          <div class="flex items-center gap-2">
            <a
              target="_blank"
              href={downloadLink("csv")}
              rel="noreferrer"
              class=" px-4 py-2"
              data-sveltekit-reload
            >
              <DownloadIcon />
              {$_("CSV file")}
            </a>
          </div>
        </li>
      </ul>
    </DetailsSummary>
  {/if}
  <HeaderDates {obj} />
</div>
