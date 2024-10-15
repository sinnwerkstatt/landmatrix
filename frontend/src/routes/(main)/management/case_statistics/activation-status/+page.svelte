<script lang="ts">
  import cn from "classnames"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { aDownload } from "$lib/utils/download"

  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import DownloadModal, {
    type DownloadEvent,
  } from "$components/New/DownloadModal.svelte"

  import CaseStatisticsTable, {
    type CaseStatisticsDeal,
    type CaseStatisticsInvestor,
  } from "../CaseStatisticsTable.svelte"
  import {
    createBlob,
    createFilename,
    resolveCountryAndRegionNames,
  } from "../downloadObjects"
  import { filters } from "../FilterBar.svelte"

  let model: "deal" | "investor" = "deal"
  let activeTabId: string | undefined = "pending"

  $: navTabs =
    model === "deal"
      ? [
          { id: "pending", name: $_("Deals pending") },
          { id: "active", name: $_("Deals active") },
          { id: "active_not_public", name: $_("Deals active, but not public") },
          { id: "active_confidential", name: $_("Deals active, but confidential") },
        ]
      : [
          { id: "pending", name: $_("Investors pending") },
          { id: "active", name: $_("Investors active") },
        ]

  let simpleDeals: CaseStatisticsDeal[] = []
  let simpleInvestors: CaseStatisticsInvestor[] = []

  async function getDealsInvestors() {
    let dealsUrl = `/api/case_statistics/?action=deals`
    const dealsRet = await fetch(dealsUrl)
    if (dealsRet.ok) simpleDeals = (await dealsRet.json()).deals

    let investorsUrl = `/api/case_statistics/?action=investors`
    const investorsRet = await fetch(investorsUrl)
    if (investorsRet.ok) simpleInvestors = (await investorsRet.json()).investors
  }

  onMount(() => getDealsInvestors())

  $: deals = $filters.country
    ? simpleDeals.filter(d => d.country_id === $filters.country?.id)
    : $filters.region
      ? simpleDeals.filter(d => d.region_id === $filters.region?.id)
      : simpleDeals

  let _active_deals: CaseStatisticsDeal[]
  $: _active_deals = deals.filter(deal => deal.active_version_id !== null)

  let dealsBuckets: { [key: string]: CaseStatisticsDeal[] }
  $: dealsBuckets = {
    pending: deals.filter(deal =>
      ["DRAFT", "REVIEW", "ACTIVATION"].includes(deal.draft_version__status as string),
    ),
    active: _active_deals,
    active_not_public: _active_deals.filter(
      deal => deal.active_version_id && !deal.active_version__is_public,
    ),
    active_confidential: _active_deals.filter(deal => deal.confidential),
  }

  $: investors = $filters.country
    ? simpleInvestors.filter(inv => inv.country_id === $filters.country?.id)
    : $filters.region
      ? simpleInvestors.filter(inv => inv.region_id === $filters.region?.id)
      : simpleInvestors

  let investorsBuckets: { [key: string]: CaseStatisticsInvestor[] }
  $: investorsBuckets = {
    pending: investors.filter(investor =>
      ["DRAFT", "REVIEW", "ACTIVATION"].includes(
        investor.draft_version__status as string,
      ),
    ),
    active: investors.filter(investor => investor.active_version_id !== null),
  }

  let showDownloadModal = false

  const download = (e: DownloadEvent) => {
    const objects = (model === "deal" ? dealsBuckets : investorsBuckets)[activeTabId!]
    const enrichedObjects = resolveCountryAndRegionNames(objects, $page.data)
    const blob = createBlob(e.detail, enrichedObjects)

    const filename = createFilename(`${model}s_${activeTabId}`, $filters, e.detail)

    blob && aDownload(blob, filename)

    showDownloadModal = false
  }
</script>

<div class="relative w-full">
  <button
    class="absolute -top-14 right-0 p-2"
    on:click={() => {
      showDownloadModal = true
    }}
    title={$_("Download")}
  >
    <DownloadIcon class="inline-block h-8 w-8" />
  </button>

  <DownloadModal
    bind:open={showDownloadModal}
    on:download={download}
    fileTypes={["csv", "xlsx"]}
  />
</div>

<div class="relative flex h-[400px] w-full border">
  <nav
    class="h-full shrink-0 basis-1/4 border-r bg-gray-50 p-2 drop-shadow-[2px_0px_1px_rgba(0,0,0,0.3)] xl:basis-1/5 dark:bg-gray-700"
  >
    <div
      class="flex justify-center gap-4 border-b border-gray-200 pb-6 pt-1 text-lg font-bold"
    >
      <button
        class={model === "deal"
          ? "border-b border-orange text-orange"
          : "text-gray-600 hover:text-orange dark:text-white"}
        on:click={() => {
          model = "deal"
          activeTabId = "pending"
        }}
        type="button"
      >
        {$_("Deals")}
      </button>
      <button
        class={model === "investor"
          ? "border-b border-pelorous text-pelorous"
          : "text-gray-600 hover:text-pelorous dark:text-white"}
        on:click={() => {
          model = "investor"
          activeTabId = "pending"
        }}
        type="button"
      >
        {$_("Investors")}
      </button>
    </div>

    <div class="w-full self-start">
      <ul>
        {#each navTabs as item}
          <li
            class={cn(
              "py-2 pr-4",
              model === "deal" ? "border-orange" : "border-pelorous",
              activeTabId === item.id ? "border-r-4" : "border-r",
            )}
          >
            <button
              class={cn(
                "block text-left",
                activeTabId === item.id
                  ? model === "deal"
                    ? "font-bold text-orange"
                    : "font-bold text-pelorous"
                  : "text-gray-700 dark:text-white",
              )}
              on:click={() => (activeTabId = item.id)}
            >
              <span class="font-bold">
                {#if model === "deal"}
                  {#if dealsBuckets[item.id]}
                    {dealsBuckets[item.id].length}
                  {/if}
                {:else if investorsBuckets[item.id]}
                  {investorsBuckets[item.id].length}
                {/if}
              </span>
              {item.name}
            </button>
          </li>
        {/each}
      </ul>
    </div>
  </nav>

  <div class="basis-3/4 overflow-auto xl:basis-4/5">
    {#if activeTabId}
      <CaseStatisticsTable
        {model}
        objects={model === "deal"
          ? dealsBuckets[activeTabId]
          : investorsBuckets[activeTabId]}
        linkDraftVersion={["pending"].includes(activeTabId)}
      />
    {/if}
  </div>
</div>
