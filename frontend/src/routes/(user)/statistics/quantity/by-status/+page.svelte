<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import { page } from "$app/state"

  import { filters } from "$lib/filters"
  import type { Model } from "$lib/types/data"
  import { aDownload } from "$lib/utils/download"

  import AdjustmentsIcon from "$components/icons/AdjustmentsIcon.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import DownloadModal, {
    type DownloadEvent,
  } from "$components/New/DownloadModal.svelte"

  import ActionButton from "../../ActionButton.svelte"
  import {
    createBlob,
    createFilename,
    resolveCountryAndRegionNames,
    type DownloadContext,
  } from "../../download"
  import FilterModal from "../../FilterModal.svelte"
  import CaseStatisticsTable, {
    type CaseStatisticsDeal,
    type CaseStatisticsInvestor,
  } from "../CaseStatisticsTable.svelte"

  let model: Model = $state("deal")
  let activeTabId: string | undefined = $state("pending")

  let navTabs = $derived(
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
        ],
  )

  let simpleDeals: CaseStatisticsDeal[] = $state([])
  let simpleInvestors: CaseStatisticsInvestor[] = $state([])

  async function getDealsInvestors() {
    let dealsUrl = `/api/case_statistics/?action=deals`
    const dealsRet = await fetch(dealsUrl)
    if (dealsRet.ok) simpleDeals = (await dealsRet.json()).deals

    let investorsUrl = `/api/case_statistics/?action=investors`
    const investorsRet = await fetch(investorsUrl)
    if (investorsRet.ok) simpleInvestors = (await investorsRet.json()).investors
  }

  onMount(() => getDealsInvestors())

  let deals = $derived(
    $filters.country_id
      ? simpleDeals.filter(d => d.country_id === $filters.country_id)
      : $filters.region_id
        ? simpleDeals.filter(d => d.region_id === $filters.region_id)
        : simpleDeals,
  )

  let _active_deals: CaseStatisticsDeal[] = $derived(
    deals.filter(deal => deal.active_version_id !== null),
  )

  let dealsBuckets: { [key: string]: CaseStatisticsDeal[] } = $derived({
    pending: deals.filter(deal =>
      ["DRAFT", "REVIEW", "ACTIVATION"].includes(deal.draft_version__status as string),
    ),
    active: _active_deals,
    active_not_public: _active_deals.filter(
      deal => deal.active_version_id && !deal.active_version__is_public,
    ),
    active_confidential: _active_deals.filter(deal => deal.confidential),
  })

  let investors = $derived(
    $filters.country_id
      ? simpleInvestors.filter(inv => inv.country_id === $filters.country_id)
      : $filters.region_id
        ? simpleInvestors.filter(inv => inv.region_id === $filters.region_id)
        : simpleInvestors,
  )

  let investorsBuckets: { [key: string]: CaseStatisticsInvestor[] } = $derived({
    pending: investors.filter(investor =>
      ["DRAFT", "REVIEW", "ACTIVATION"].includes(
        investor.draft_version__status as string,
      ),
    ),
    active: investors.filter(investor => investor.active_version_id !== null),
  })

  let showDownloadModal = $state(false)
  let showFilterModal = $state(false)

  const download = (e: DownloadEvent) => {
    const context: DownloadContext = {
      filters: $filters,
      regions: page.data.regions,
      countries: page.data.countries,
    }
    const objects = (model === "deal" ? dealsBuckets : investorsBuckets)[activeTabId!]
    const enrichedObjects = resolveCountryAndRegionNames(objects, context)
    const blob = createBlob(e.detail, enrichedObjects)

    const filename = createFilename(`${model}s_${activeTabId}`, e.detail, context)

    if (blob) aDownload(blob, filename)

    showDownloadModal = false
  }
</script>

<h2 class="heading3">
  {$_("Deals and investors by activation status")}
</h2>

<ul class="my-2 flex justify-end gap-6">
  <li>
    <ActionButton
      onclick={() => (showFilterModal = true)}
      icon={AdjustmentsIcon}
      highlight={!$filters.isEmpty()}
      label={$_("Filter")}
    />
  </li>
  <li>
    <ActionButton
      onclick={() => (showDownloadModal = true)}
      icon={DownloadIcon}
      label={$_("Download")}
    />
  </li>
</ul>

<FilterModal
  bind:open={showFilterModal}
  disableAdvanced
  onsubmit={() => (showFilterModal = false)}
/>

<DownloadModal
  bind:open={showDownloadModal}
  on:download={download}
  fileTypes={["csv", "xlsx"]}
/>

<div class="relative flex h-[400px] w-full border">
  <nav
    class="h-full shrink-0 basis-1/4 border-r bg-gray-50 p-2 drop-shadow-[2px_0px_1px_rgba(0,0,0,0.3)] xl:basis-1/5 dark:bg-gray-700"
  >
    <div
      class="flex justify-center gap-4 border-b border-gray-200 pb-6 pt-1 text-lg font-bold"
    >
      <button
        type="button"
        class={model === "deal"
          ? "border-b border-orange text-orange"
          : "text-gray-600 hover:text-orange dark:text-white"}
        onclick={() => {
          model = "deal"
          activeTabId = "pending"
        }}
      >
        {$_("Deals")}
      </button>
      <button
        type="button"
        class={model === "investor"
          ? "border-b border-pelorous text-pelorous"
          : "text-gray-600 hover:text-pelorous dark:text-white"}
        onclick={() => {
          model = "investor"
          activeTabId = "pending"
        }}
      >
        {$_("Investors")}
      </button>
    </div>

    <div class="w-full self-start">
      <ul>
        {#each navTabs as item}
          <li
            class={twMerge(
              "py-2 pr-4",
              model === "deal" ? "border-orange" : "border-pelorous",
              activeTabId === item.id ? "border-r-4" : "border-r",
            )}
          >
            <button
              type="button"
              class={twMerge(
                "block text-left",
                activeTabId === item.id
                  ? model === "deal"
                    ? "font-bold text-orange"
                    : "font-bold text-pelorous"
                  : "text-gray-700 dark:text-white",
              )}
              onclick={() => (activeTabId = item.id)}
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
