<script lang="ts">
  import cn from "classnames"
  import { _ } from "svelte-i18n"

  import CaseStatisticsTable from "./CaseStatisticsTable.svelte"

  interface CaseStatisticsDeal {
    id: number
    mode: string
    active_version_id: number | null
    draft_version_id: number | null
    draft_version__status: string
    fully_updated_at: string | null
    active_version__fully_updated: boolean
    confidential: boolean
    country_id: number | null
    country__region_id: number | null
    active_version__deal_size: number | null
    active_version__is_public: boolean

    first_created_at: string
    active_version__modified_at: string | null
  }
  interface CaseStatisticsInvestor {
    id: number
    mode: string
    active_version_id: number | null
    draft_version_id: number | null
    draft_version__status: string
    active_version__name: string
    active_version__country_id: number | null
    active_version__country__region_id: number | null

    first_created_at: string
    active_version__modified_at: string | null
  }
  export let deals: CaseStatisticsDeal[] = []
  export let investors: CaseStatisticsInvestor[] = []

  let model: "deal" | "investor" = "deal"
  let activeTabId: string | undefined = "pending"

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

  let _active_deals: CaseStatisticsDeal[]
  $: _active_deals = deals.filter(deal => deal.active_version_id !== null)
  $: deals_buckets = {
    pending: deals.filter(deal =>
      ["DRAFT", "REVIEW", "ACTIVATION"].includes(deal.draft_version__status),
    ),
    rejected: deals.filter(deal => deal.draft_version__status === "REJECTED"),
    pending_deletion: deals.filter(deal => deal.draft_version__status === "TO_DELETE"),
    active: _active_deals,
    active_not_public: _active_deals.filter(
      deal => deal.active_version_id && !deal.active_version__is_public,
    ),
    active_confidential: _active_deals.filter(deal => deal.confidential),
  }

  $: investors_buckets = {
    pending: investors.filter(investor =>
      ["DRAFT", "REVIEW", "ACTIVATION"].includes(investor.draft_version__status),
    ),
    rejected: investors.filter(
      investor => investor.draft_version__status === "REJECTED",
    ),
    pending_deletion: investors.filter(
      investor => investor.draft_version__status === "TO_DELETE",
    ),
    active: investors.filter(investor => investor.active_version_id !== null),
  }
</script>

<h2 class="heading5">{$_("Indicator listings")}</h2>

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
                  {#if deals_buckets[item.id]}
                    {deals_buckets[item.id].length}
                  {/if}
                {:else if investors_buckets[item.id]}
                  {investors_buckets[item.id].length}
                {/if}
              </span>
              {item.name}
            </button>
          </li>
        {/each}
      </ul>
    </div>
  </nav>
  <div class="basis-3/4 xl:basis-4/5">
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
