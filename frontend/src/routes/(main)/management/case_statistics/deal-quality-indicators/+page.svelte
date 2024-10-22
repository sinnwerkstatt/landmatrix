<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { page } from "$app/stores"

  import { filters } from "$lib/filters"
  import type { components } from "$lib/openAPI"
  import type { DealQIKey, Model } from "$lib/types/data"
  import { aDownload } from "$lib/utils/download"

  import AdjustmentsIcon from "$components/icons/AdjustmentsIcon.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import DownloadModal, {
    type DownloadEvent,
  } from "$components/New/DownloadModal.svelte"

  import ActionButton from "../ActionButton.svelte"
  import { createBlob, createFilename, type DownloadContext } from "../downloadObjects"
  import FilterModal from "../FilterModal.svelte"
  import QIInverseSwitcher from "../QIInverseSwitcher.svelte"
  import QINavigator from "../QINavigator.svelte"
  import QITable from "../QITable.svelte"
  import QITableDownload from "../QITableDownload.svelte"

  const model: Model = "deal"

  let activeKey: DealQIKey | null = null
  let inverse = false

  let counts: components["schemas"]["DealQICounts"] | null = null

  const fetchCounts = () => {
    counts = null

    $page.data.apiClient
      .GET(
        `/api/quality-indicators/counts/deal/?${$filters.toRESTFilterArray()}` as "/api/quality-indicators/counts/deal/",
      )
      .then(res => ("error" in res ? Promise.reject(res.error) : res.data!))
      .then(res => (counts = res))
  }

  onMount(fetchCounts)

  let filterOpen: boolean = false
  let downloadOpen: boolean = false

  const download = (e: DownloadEvent) => {
    const blob = createBlob(e.detail, counts)
    const context: DownloadContext = {
      filters: $filters,
      regions: $page.data.regions,
      countries: $page.data.countries,
    }
    const filename = createFilename("deal-quality-indicators", e.detail, context)

    aDownload(blob, filename)

    downloadOpen = false
  }
</script>

<ul class="mb-4 ml-4 mr-8 flex flex-wrap items-baseline justify-end gap-x-8">
  <li>
    <ActionButton
      on:click={() => (filterOpen = true)}
      icon={AdjustmentsIcon}
      label={$_("Filter")}
    />
  </li>
  <li>
    <ActionButton
      on:click={() => (downloadOpen = true)}
      icon={DownloadIcon}
      label={$_("Download")}
    />
  </li>
</ul>

<QINavigator {model} {counts} bind:activeKey>
  <svelte:fragment slot="list">
    <div class="p-2" transition:slide={{ duration: 300 }}>
      <div class="flex justify-between">
        <QIInverseSwitcher bind:inverse {model} />
        <QITableDownload />
      </div>
      <div class="h-[300px] overflow-y-auto">
        {#if activeKey}
          <QITable key={activeKey} {model} {inverse} />
        {/if}
      </div>
    </div>
  </svelte:fragment>
</QINavigator>

<DownloadModal
  bind:open={downloadOpen}
  on:download={download}
  disableSubmit={!counts}
/>

<FilterModal
  bind:open={filterOpen}
  on:submit={async () => {
    fetchCounts()
    filterOpen = false
  }}
/>
