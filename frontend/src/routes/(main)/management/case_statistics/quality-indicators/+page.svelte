<script lang="ts">
  import { onMount } from "svelte"
  import { slide } from "svelte/transition"

  import { page } from "$app/stores"

  import type { components } from "$lib/openAPI"
  import type { DealQIKey, InvestorQIKey } from "$lib/types/data"

  import { filters } from "../FilterBar.svelte"
  import QIDownloadStats from "./QIComponents/QIDownloadStats.svelte"
  import QIInverseSwitcher from "./QIComponents/QIInverseSwitcher.svelte"
  import QIModelSwitcher from "./QIComponents/QIModelSwitcher.svelte"
  import QINavigator from "./QIComponents/QINavigator.svelte"
  import QITable from "./QIComponents/QITable.svelte"

  let model: "deal" | "investor" = "deal"
  let activeKey: DealQIKey | InvestorQIKey | null = null
  let inverse = false

  let counts: components["schemas"]["QICountsResponse"] | null = null

  const fetchCounts = () => {
    counts = null
    $page.data.apiClient
      .GET("/api/quality-indicators/count/", {
        params: {
          query: {
            region_id: $filters.region?.id,
            country_id: $filters.country?.id,
          },
        },
      })
      .then(res => ("error" in res ? Promise.reject(res.error) : res.data!))
      .then(res => (counts = res))
  }

  onMount(fetchCounts)

  $: $filters && fetchCounts()

  // reset on model switch
  $: model && (activeKey = null)
  $: model && (inverse = false)
</script>

<div class="mb-4 space-y-2">
  <QIDownloadStats {counts} />

  <QIModelSwitcher bind:model />
</div>
<!--<p>-->
<!--  {$_(-->
<!--    "Click on an indicator to show the list of {dealsOrInvestors} " +-->
<!--      "fulfilling the quality indicator condition.",-->
<!--    { values: { dealsOrInvestors: `${model}s` } },-->
<!--  )}-->
<!--</p>-->

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
