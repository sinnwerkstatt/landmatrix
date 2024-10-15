<script lang="ts">
  import { onMount } from "svelte"
  import { slide } from "svelte/transition"

  import { page } from "$app/stores"

  import type { components } from "$lib/openAPI"
  import type { DealQIKey, InvestorQIKey, Model } from "$lib/types/data"

  import QIDownloadStats from "../QIComponents/QIDownloadStats.svelte"
  import QIInverseSwitcher from "../QIComponents/QIInverseSwitcher.svelte"
  import QINavigator from "../QIComponents/QINavigator.svelte"
  import QITable from "../QIComponents/QITable.svelte"

  const model: Model = "investor"

  let activeKey: DealQIKey | InvestorQIKey | null = null
  let inverse = false

  let counts: components["schemas"]["QICountsResponse"] | null = null

  const fetchCounts = () => {
    counts = null
    $page.data.apiClient
      .GET("/api/quality-indicators/count/")
      .then(res => ("error" in res ? Promise.reject(res.error) : res.data!))
      .then(res => (counts = res))
  }

  onMount(fetchCounts)
</script>

<div class="mx-10 mb-4 flex items-baseline justify-end space-y-2">
  <QIDownloadStats {counts} {model} />
</div>

<QINavigator {model} {counts} bind:activeKey>
  <svelte:fragment slot="list">
    <div class="p-2" transition:slide={{ duration: 300 }}>
      <QIInverseSwitcher bind:inverse {model} />
      <div class="h-[300px] overflow-y-auto">
        <QITable key={activeKey} {model} {inverse} />
      </div>
    </div>
  </svelte:fragment>
</QINavigator>
