<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { page } from "$app/state"

  import { filters } from "$lib/filters"
  import type { components } from "$lib/openAPI"
  import type { DealQIKey, Model } from "$lib/types/data"
  import { aDownload } from "$lib/utils/download"

  import AdjustmentsIcon from "$components/icons/AdjustmentsIcon.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import DownloadModal, {
    type DownloadEvent,
  } from "$components/New/DownloadModal.svelte"

  import ActionButton from "../../ActionButton.svelte"
  import { createBlob, createFilename, type DownloadContext } from "../../download"
  import FilterModal from "../../FilterModal.svelte"
  import QIInverseSwitcher from "../QIInverseSwitcher.svelte"
  import QINavigator from "../QINavigator.svelte"
  import QITable from "../QITable.svelte"
  import QITableDownload from "../QITableDownload.svelte"

  const model: Model = "deal"

  let activeKey: DealQIKey | null = $state(null)
  let inverse = $state(false)

  let counts: components["schemas"]["DealQICounts"] | null = $state(null)

  const fetchCounts = () => {
    counts = null

    page.data.apiClient
      .GET(
        `/api/quality-indicators/counts/deal/?${$filters.toRESTFilterArray()}` as "/api/quality-indicators/counts/deal/",
      )
      .then(res => ("error" in res ? Promise.reject(res.error) : res.data!))
      .then(res => (counts = res))
  }

  onMount(fetchCounts)

  let filterOpen: boolean = $state(false)
  let downloadOpen: boolean = $state(false)

  const download = (e: DownloadEvent) => {
    const blob = createBlob(e.detail, counts)
    const context: DownloadContext = {
      filters: $filters,
      regions: page.data.regions,
      countries: page.data.countries,
    }
    const filename = createFilename("deal-quality-indicators", e.detail, context)

    aDownload(blob, filename)

    downloadOpen = false
  }
</script>

<h2 class="heading3">
  {$_("Quality indicators for deal data")}
</h2>

<ul class="mb-4 ml-4 mr-8 flex flex-wrap items-baseline justify-end gap-x-8">
  <li>
    <ActionButton
      onclick={() => (filterOpen = true)}
      icon={AdjustmentsIcon}
      highlight={!$filters.isEmpty()}
      label={$_("Filter")}
    />
  </li>
  <li>
    <ActionButton
      onclick={() => (downloadOpen = true)}
      icon={DownloadIcon}
      label={$_("Download")}
    />
  </li>
</ul>

<QINavigator {model} {counts} bind:activeKey>
  {#snippet list()}
    {#if activeKey}
      <div class="p-2" transition:slide={{ duration: 300 }}>
        <div class="flex justify-between">
          <QIInverseSwitcher bind:inverse {model} />
          <QITableDownload qi={activeKey} {inverse} />
        </div>
        <div class="h-[300px] overflow-y-auto">
          <QITable key={activeKey} {model} {inverse} />
        </div>
      </div>
    {/if}
  {/snippet}
</QINavigator>

<DownloadModal
  bind:open={downloadOpen}
  on:download={download}
  disableSubmit={!counts}
/>

<FilterModal
  bind:open={filterOpen}
  onsubmit={async () => {
    fetchCounts()
    filterOpen = false
  }}
/>
