<script lang="ts">
  import cn from "classnames"
  import { DateInput } from "date-picker-svelte"
  import dayjs from "dayjs"
  import isSameOrAfter from "dayjs/plugin/isSameOrAfter"
  import isSameOrBefore from "dayjs/plugin/isSameOrBefore"
  import { _ } from "svelte-i18n"

  import { loading } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import type { Country, Region } from "$lib/types/wagtail"

  import CaseStatisticsTable from "./CaseStatisticsTable.svelte"

  dayjs.extend(isSameOrBefore)
  dayjs.extend(isSameOrAfter)

  export let region: Region | undefined = undefined
  export let country: Country | undefined = undefined

  let model: "deal" | "investor" = "deal"
  let activeTabId: string | undefined = undefined

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

  let selectedDateOption = 30
  let daterange = {
    start: dayjs().subtract(selectedDateOption, "day").toDate(),
    end: new Date(),
  }

  $: selectedDateOption = dayjs(daterange.end).diff(daterange.start, "days")

  const datePreOptions = [
    { name: "Last 30 days", value: 30 },
    { name: "Last 60 days", value: 60 },
    { name: "Last 180 days", value: 180 },
    { name: "Last 365 days", value: 365 },
  ]

  let dealBuckets: { [key: string]: Deal[] } = {}
  let investorBuckets: { [key: string]: Investor[] } = {}

  async function _fetchDeals(
    region: Region | undefined,
    country: Country | undefined,
    daterange,
  ) {
    const params = new URLSearchParams({
      action: "deal_buckets",
      start: dayjs(daterange.start).format("YYYY-MM-DD"),
      end: dayjs(daterange.end).format("YYYY-MM-DD"),
    })
    if (region) params.append("region", `${region.id}`)
    if (country) params.append("country", `${country.id}`)

    const ret = await fetch(`/api/case_statistics/?${params}`)
    if (ret.ok) dealBuckets = (await ret.json()).buckets
  }

  async function _fetchInvestors(
    region: Region | undefined,
    country: Country | undefined,
    daterange,
  ) {
    const params = new URLSearchParams({
      action: "investor_buckets",
      start: dayjs(daterange.start).format("YYYY-MM-DD"),
      end: dayjs(daterange.end).format("YYYY-MM-DD"),
    })
    if (region) params.append("region", `${region.id}`)
    if (country) params.append("country", `${country.id}`)

    const ret = await fetch(`/api/case_statistics/?${params}`)
    if (ret.ok) investorBuckets = (await ret.json()).buckets
  }

  async function fetchObjs(
    region: Region | undefined,
    country: Country | undefined,
    daterange,
  ) {
    loading.set(true)
    await Promise.all([
      _fetchDeals(region, country, daterange),
      _fetchInvestors(region, country, daterange),
    ])
    loading.set(false)
  }

  $: fetchObjs(region, country, daterange)
</script>

<div class="mb-4 mt-10 flex items-center gap-8">
  <h2 class="m-0 whitespace-nowrap">{$_("Changes within timespan")}</h2>
  <div class="flex items-center gap-6">
    <select
      bind:value={selectedDateOption}
      class="inpt w-40"
      on:change={() =>
        (daterange = {
          start: dayjs().subtract(selectedDateOption, "day").toDate(),
          end: new Date(),
        })}
    >
      {#each datePreOptions as option}
        <option value={option.value}>
          {option.name}
        </option>
      {/each}
    </select>
    <div class="flex gap-2">
      <DateInput bind:value={daterange.start} format="yyyy-MM-dd" />
      <DateInput bind:value={daterange.end} format="yyyy-MM-dd" />
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
                  {#if dealBuckets[item.id]} {dealBuckets[item.id].length}{/if}
                {:else if investorBuckets[item.id]}
                  {investorBuckets[item.id].length}
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
      <CaseStatisticsTable
        {model}
        objects={model === "deal"
          ? dealBuckets[activeTabId]
          : investorBuckets[activeTabId]}
      />
    {/if}
  </div>
</div>
