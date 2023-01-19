<script lang="ts">
  import cn from "classnames"
  import { _ } from "svelte-i18n"

  import type { Deal } from "$lib/types/deal"
  import { DraftStatus, Status } from "$lib/types/generics"
  import type { Investor } from "$lib/types/investor"

  import CaseStatisticsTable from "./CaseStatisticsTable.svelte"

  export let deals: Deal[] = []
  export let investors: Investor[] = []

  let model: "deal" | "investor" = "deal"
  let activeTabId: string | undefined = undefined

  $: navTabs =
    model === "deal"
      ? [
          { id: "pending", name: $_("Deals pending") },
          { id: "rejected", name: $_("Deals rejected") },
          { id: "pending_deletion", name: $_("Deals pending deletion") },
          { id: "active", name: $_("Deals active") },
          { id: "active_not_public", name: $_("Deals active, but not public") },
          { id: "active_confidential", name: $_("Deals active, but confidential") },
        ]
      : [
          { id: "pending", name: $_("Investors pending") },
          { id: "rejected", name: $_("Investors rejected") },
          { id: "pending_deletion", name: $_("Investors pending deletion") },
          { id: "active", name: $_("Investors active") },
        ]

  let _active_deals: Deal[]
  $: _active_deals = deals.filter(
    deal => deal.status === Status.LIVE || deal.status === Status.UPDATED,
  )
  $: deals_buckets = {
    pending: deals.filter(
      deal =>
        deal.draft_status === DraftStatus.DRAFT ||
        deal.draft_status === DraftStatus.REVIEW ||
        deal.draft_status === DraftStatus.ACTIVATION,
    ),
    rejected: deals.filter(deal => deal.draft_status === DraftStatus.REJECTED),
    pending_deletion: deals.filter(deal => deal.draft_status === DraftStatus.TO_DELETE),
    active: _active_deals,
    active_not_public: _active_deals.filter(deal => !deal.is_public),
    active_confidential: _active_deals.filter(deal => deal.confidential),
  }

  $: investors_buckets = {
    pending: investors.filter(
      investor =>
        investor.draft_status === DraftStatus.DRAFT ||
        investor.draft_status === DraftStatus.REVIEW ||
        investor.draft_status === DraftStatus.ACTIVATION,
    ),
    rejected: investors.filter(
      investor => investor.draft_status === DraftStatus.REJECTED,
    ),
    pending_deletion: investors.filter(
      investor => investor.draft_status === DraftStatus.TO_DELETE,
    ),
    active: investors.filter(
      investor => investor.status === Status.LIVE || investor.status === Status.UPDATED,
    ),
  }
</script>

<div class="relative flex h-full w-full border bg-stone-100">
  <nav
    class="h-full shrink-0 basis-1/4 flex-col bg-white/80 p-2 drop-shadow-[2px_0px_1px_rgba(0,0,0,0.3)] xl:basis-1/6"
  >
    <div
      class="flex justify-center gap-4 border-b border-gray-200 p-1 pb-6 text-lg font-bold"
    >
      <button
        class={model === "deal"
          ? "border-b border-solid border-black text-black"
          : "text-gray-500 hover:text-gray-600"}
        on:click={() => {
          model = "deal"
          activeTabId = undefined
        }}
        type="button"
      >
        {$_("Deals")}
      </button>
      <button
        class={model === "investor"
          ? "border-b border-solid border-black text-black"
          : "text-gray-500 hover:text-gray-600"}
        on:click={() => {
          model = "investor"
          activeTabId = undefined
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
                  : "text-gray-600",
              )}
              on:click={() => (activeTabId = item.id)}
            >
              <span class="font-bold">
                {#if model === "deal"}
                  {#if deals_buckets[item.id]} {deals_buckets[item.id].length}{/if}
                {:else if investors_buckets[item.id]}
                  {investors_buckets[item.id].length}{/if}
              </span>
              {item.name}
            </button>
          </li>
        {/each}
      </ul>
    </div>
  </nav>
  <div class="mx-auto max-h-[600px]">
    {#if activeTabId}
      <CaseStatisticsTable
        {model}
        objects={model === "deal"
          ? deals_buckets[activeTabId]
          : investors_buckets[activeTabId]}
      />
    {/if}
  </div>
</div>
