<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { page } from "$app/state"

  import { filters } from "$lib/filters"
  import type { components } from "$lib/openAPI"
  import type { InvestorQIKey, Model } from "$lib/types/data"
  import { aDownload } from "$lib/utils/download"

  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import DownloadModal, {
    type DownloadEvent,
  } from "$components/New/DownloadModal.svelte"

  import ActionButton from "../../ActionButton.svelte"
  import { createBlob, createFilename, type DownloadContext } from "../../download"
  import QIInverseSwitcher from "../QIInverseSwitcher.svelte"
  import QINavigator from "../QINavigator.svelte"
  import QITable from "../QITable.svelte"

  const model: Model = "investor"

  let activeKey: InvestorQIKey | null = $state(null)
  let inverse = $state(false)

  let counts: components["schemas"]["InvestorQICounts"] | null = $state(null)

  const fetchCounts = () => {
    counts = null

    page.data.apiClient
      .GET("/api/quality-indicators/counts/investor/")
      .then(res => ("error" in res ? Promise.reject(res.error) : res.data!))
      .then(res => (counts = res))
  }

  onMount(fetchCounts)

  let downloadOpen: boolean = $state(false)

  const download = (e: DownloadEvent) => {
    const blob = createBlob(e.detail, counts)
    const context: DownloadContext = {
      filters: $filters,
      regions: page.data.regions,
      countries: page.data.countries,
    }
    const filename = createFilename("investor-quality-indicators", e.detail, context)

    aDownload(blob, filename)

    downloadOpen = false
  }
</script>

<h2 class="heading3">
  {$_("Quality indicators for investor data")}
</h2>

<ul class="mb-4 ml-4 mr-8 flex flex-wrap items-baseline justify-end gap-x-8">
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
    <div class="p-2" transition:slide={{ duration: 300 }}>
      <QIInverseSwitcher bind:inverse {model} />
      <!--      <QITableDownload />-->
      <div class="h-[300px] overflow-y-auto">
        {#if activeKey}
          <QITable key={activeKey} {model} {inverse} />
        {/if}
      </div>
    </div>
  {/snippet}
</QINavigator>

<DownloadModal
  bind:open={downloadOpen}
  on:download={download}
  disableSubmit={!counts}
/>
