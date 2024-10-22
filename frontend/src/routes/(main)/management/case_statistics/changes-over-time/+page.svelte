<script lang="ts">
  import cn from "classnames"
  import { DateInput } from "date-picker-svelte"
  import dayjs from "dayjs"
  import isSameOrAfter from "dayjs/plugin/isSameOrAfter"
  import isSameOrBefore from "dayjs/plugin/isSameOrBefore"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { filters, FilterValues } from "$lib/filters"
  import { loading } from "$lib/stores/basics"
  import { aDownload } from "$lib/utils/download"

  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import DownloadModal, {
    type DownloadEvent,
  } from "$components/New/DownloadModal.svelte"

  import ActionButton from "../ActionButton.svelte"
  import CaseStatisticsTable, {
    type CaseStatisticsDeal,
    type CaseStatisticsInvestor,
  } from "../CaseStatisticsTable.svelte"
  import {
    createBlob,
    createFilename,
    resolveCountryAndRegionNames,
    type DownloadContext,
  } from "../downloadObjects"

  dayjs.extend(isSameOrBefore)
  dayjs.extend(isSameOrAfter)

  let model: "deal" | "investor" = "deal"
  let activeTabId: string | undefined = "added"

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

  interface Daterange {
    start: Date
    end: Date
  }
  let daterange: Daterange = {
    start: dayjs().subtract(30, "day").toDate(),
    end: new Date(),
  }

  let selectedDateOption = dayjs(daterange.end).diff(daterange.start, "days")

  const datePreOptions = [
    { name: "Last 30 days", value: 30 },
    { name: "Last 60 days", value: 60 },
    { name: "Last 180 days", value: 180 },
    { name: "Last 365 days", value: 365 },
  ]

  let dealBuckets: { [key: string]: CaseStatisticsDeal[] } = {}
  let investorBuckets: { [key: string]: CaseStatisticsInvestor[] } = {}

  async function _fetchDeals(filters: FilterValues, daterange: Daterange) {
    const params = new URLSearchParams({
      action: "deal_buckets",
      start: dayjs(daterange.start).format("YYYY-MM-DD"),
      end: dayjs(daterange.end).format("YYYY-MM-DD"),
    })
    if (filters.region_id) params.append("region", `${filters.region_id}`)
    if (filters.country_id) params.append("country", `${filters.country_id}`)

    const ret = await fetch(`/api/case_statistics/?${params}`)
    if (ret.ok) dealBuckets = (await ret.json()).buckets
  }

  async function _fetchInvestors(filters: FilterValues, daterange: Daterange) {
    const params = new URLSearchParams({
      action: "investor_buckets",
      start: dayjs(daterange.start).format("YYYY-MM-DD"),
      end: dayjs(daterange.end).format("YYYY-MM-DD"),
    })
    if (filters.region_id) params.append("region", `${filters.region_id}`)
    if (filters.country_id) params.append("country", `${filters.country_id}`)

    const ret = await fetch(`/api/case_statistics/?${params}`)
    if (ret.ok) investorBuckets = (await ret.json()).buckets
  }

  async function fetchObjs(filters: FilterValues, daterange: Daterange) {
    loading.set(true)
    await Promise.all([
      _fetchDeals(filters, daterange),
      _fetchInvestors(filters, daterange),
    ])
    loading.set(false)
  }

  $: fetchObjs($filters, daterange)

  let showDownloadModal = false

  const download = (e: DownloadEvent) => {
    const context: DownloadContext = {
      filters: $filters,
      regions: $page.data.regions,
      countries: $page.data.countries,
    }
    const objects = (model === "deal" ? dealBuckets : investorBuckets)[activeTabId!]
    const enrichedObjects = resolveCountryAndRegionNames(objects, context)
    const blob = createBlob(e.detail, enrichedObjects)

    const filename = createFilename(`${model}s_${activeTabId}`, e.detail, context)

    blob && aDownload(blob, filename)

    showDownloadModal = false
  }
</script>

<div class="my-2 flex items-center gap-6">
  <select
    bind:value={selectedDateOption}
    class="inpt w-40"
    on:change={() => {
      daterange = {
        start: dayjs().subtract(selectedDateOption, "day").toDate(),
        end: new Date(),
      }
    }}
  >
    {#each datePreOptions as option}
      <option value={option.value}>
        {option.name}
      </option>
    {/each}
  </select>
  <DateInput bind:value={daterange.start} format="yyyy-MM-dd" />
  <DateInput bind:value={daterange.end} format="yyyy-MM-dd" />
  <span class="flex-grow" />
  <ActionButton
    on:click={() => (showDownloadModal = true)}
    icon={DownloadIcon}
    label={$_("Download")}
  />
</div>

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
        class={model === "deal"
          ? "border-b border-orange text-orange"
          : "text-gray-600 hover:text-orange dark:text-white"}
        on:click={() => {
          model = "deal"
          activeTabId = "added"
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
          activeTabId = "added"
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
                  {#if dealBuckets[item.id]}
                    {dealBuckets[item.id].length}
                  {/if}
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

  <div class="basis-3/4 overflow-auto xl:basis-4/5">
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
