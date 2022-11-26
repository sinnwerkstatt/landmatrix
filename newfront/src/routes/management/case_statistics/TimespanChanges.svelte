<script lang="ts">
  import cn from "classnames"
  import dayjs from "dayjs"
  import isSameOrAfter from "dayjs/plugin/isSameOrAfter"
  import isSameOrBefore from "dayjs/plugin/isSameOrBefore"
  import { _ } from "svelte-i18n"

  import { loading } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import type { Country, Region } from "$lib/types/wagtail"

  import IndicatorListingsTable from "./IndicatorListingsTable.svelte"

  dayjs.extend(isSameOrBefore)
  dayjs.extend(isSameOrAfter)

  export let region: Region | undefined = undefined
  export let country: Country | undefined = undefined

  let model: "deal" | "investor" = "deal"
  let activeTabId: string

  $: navTabs =
    model === "deal"
      ? [
          { id: "added", name: $_("Deals added") },
          { id: "updated", name: $_("Deals updated") },
          { id: "fully_updated", name: $_("Deals fully updated") },
          { id: "activated", name: $_("Deals activated") },
        ]
      : [
          { id: "added", name: $_("Investors added") },
          { id: "updated", name: $_("Investors updated") },
          { id: "activated", name: $_("Investors activated") },
        ]

  let daterange = {
    start: dayjs().subtract(30, "day").toDate(),
    end: new Date(),
  }
  let selectedDateOption = 30
  let datePreOptions = [
    { name: "Last 30 days", value: 30 },
    { name: "Last 60 days", value: 60 },
    { name: "Last 180 days", value: 180 },
    { name: "Last 365 days", value: 365 },
  ]

  function updateDateRange() {
    daterange = {
      start: dayjs().subtract(selectedDateOption, "day").toDate(),
      end: new Date(),
    }
  }

  let deals: Deal[] = []
  let investors: Investor[] = []

  async function fetchObjs(r: Region | undefined, c: Country | undefined, daterange) {
    loading.set(true)

    const params = new URLSearchParams({
      action: "deal_versions",
      start: dayjs(daterange.start).format("YYYY-MM-DD"),
      end: dayjs(daterange.end).format("YYYY-MM-DD"),
    })
    if (r) params.append("region", `${r.id}`)
    else if (c) params.append("country", `${c.id}`)
    console.log(params.toString())
    let url = `${import.meta.env.VITE_BASE_URL}/api/case_statistics/?${params}`
    // if (r) url += `&region=${r.id}`
    // else if (c) url += `&country=${c.id}`
    const ret = await fetch(url)
    if (ret.ok) deals = (await ret.json())?.deals ?? []

    loading.set(false)
  }

  $: fetchObjs(region, country, daterange)

  $: deals_buckets = {
    added: deals.filter(d => {
      let dateCreated = dayjs(d.created_at)
      return (
        [2, 3].includes(d.status as number) &&
        dateCreated.isSameOrAfter(daterange.start, "day") &&
        dateCreated.isSameOrBefore(daterange.end, "day")
      )
    }),
    updated: deals.filter(d => d.status === 3),
    fully_updated: deals.filter(d => d.draft_status === 5),
    activated: deals.filter(
      d => d.draft_status === null && (d.status === 2 || d.status === 3),
    ),
  }
  $: investors_buckets = {
    added: investors.filter(o => o.status === 1 && o.created_at === o.modified_at),
    updated: investors.filter(o => {
      // not added investors
      if (o.status === 1 && o.created_at === o.modified_at) return false
      // not deleted investors
      if (o.status === 4) return false
      // finally
      return true
    }),
    activated: investors.filter(
      o => o.draft_status === null && (o.status === 2 || o.status === 3),
    ),
  }
</script>

<div class="mb-4 mt-10 flex items-center gap-4">
  <h2 class="m-0">{$_("Changes within timespan")}</h2>
  <div class="">
    <div>
      <select
        bind:value={selectedDateOption}
        class="inpt w-40"
        on:change={updateDateRange}
      >
        {#each datePreOptions as option}
          <option value={option.value}>
            {option.name}
          </option>
        {/each}
      </select>
    </div>
  </div>
</div>

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
  <div class="mx-auto max-h-[600px]">
    {#if activeTabId}
      <IndicatorListingsTable
        {model}
        objects={model === "deal"
          ? deals_buckets[activeTabId]
          : investors_buckets[activeTabId]}
      />
    {/if}
  </div>
</div>
