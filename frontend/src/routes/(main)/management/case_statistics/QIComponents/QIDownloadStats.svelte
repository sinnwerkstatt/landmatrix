<script lang="ts">
  import { stringify as csvStringify } from "csv-stringify/browser/esm/sync"
  import { _ } from "svelte-i18n"
  import * as xlsx from "xlsx"

  import type { components } from "$lib/openAPI"
  import type { Model } from "$lib/types/data"
  import { aDownload } from "$lib/utils/download"

  import { a_download } from "$components/Data/Charts/utils"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import DownloadModal, {
    type DownloadEvent,
  } from "$components/New/DownloadModal.svelte"

  import { createCountyRegionSuffix } from "../downloadObjects"
  import { filters } from "../FilterBar.svelte"

  export let counts: components["schemas"]["QICountsResponse"] | null
  export let model: Model

  let showDownloadModal = false

  $: modelData = counts && counts[model]

  const download = (e: DownloadEvent) => {
    const filename =
      new Date().toISOString().slice(0, 10) +
      "_data-quality-indicators" +
      createCountyRegionSuffix($filters)

    if (e.detail === "json") {
      const jsonString = JSON.stringify(modelData)
      a_download(
        "data:application/json;charset=utf-8," + encodeURIComponent(jsonString),
        `${filename}.json`,
      )
    } else if (e.detail === "csv") {
      const csvString = csvStringify([modelData], { header: true })
      a_download(
        "data:text/csv;charset=utf-8," + encodeURIComponent(csvString),
        `${filename}.csv`,
      )
    } else {
      const csvString = csvStringify([modelData], { header: true })
      const wb = xlsx.read(csvString, { type: "string" })
      const data = xlsx.write(wb, { type: "array", bookType: "xlsx" })
      const blob = new Blob([data], { type: "application/ms-excel" })
      aDownload(blob, `${filename}.xlsx`)
    }

    showDownloadModal = false
  }
</script>

<button
  class="text-left"
  on:click={() => {
    showDownloadModal = true
  }}
  title={$_("Download statistics")}
>
  <DownloadIcon class="inline-block h-8 w-8" />
  <DownloadModal
    bind:open={showDownloadModal}
    on:download={download}
    disableSubmit={!modelData}
  />
</button>
