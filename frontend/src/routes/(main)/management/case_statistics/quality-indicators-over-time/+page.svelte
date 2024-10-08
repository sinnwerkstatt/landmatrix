<script lang="ts">
  import { DateInput } from "date-picker-svelte"
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"
  import { fade, slide } from "svelte/transition"

  import { page } from "$app/stores"

  import { clickOutside } from "$lib/helpers"
  import type { components } from "$lib/openAPI"
  import type { Model } from "$lib/types/data"

  import { a_download } from "$components/Data/Charts/utils"
  import DateTimeField from "$components/Fields/Display2/DateTimeField.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import EyeIcon from "$components/icons/EyeIcon.svelte"
  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"
  import Table, { type Column } from "$components/Table/Table.svelte"

  let model: Model = "deal"
  type Item = components["schemas"]["DealQISnapshot"]

  $: qiPromise = $page.data.apiClient
    .GET("/api/quality-indicators/")
    .then(res => ("error" in res ? Promise.reject(res.error) : res.data!))

  $: statsPromise = $page.data.apiClient
    .GET("/api/quality-indicators/stats/")
    .then(res => ("error" in res ? Promise.reject(res.error) : res.data!))

  const formatRatio = (a: number, b: number): string =>
    `${((a / b) * 100).toFixed(1)} %`

  let columns: Column[]
  $: columns = [
    // { key: "id", colSpan: 1, label: $_("ID") },
    { key: "created_at", colSpan: 2, label: $_("Date") },
    { key: "region", colSpan: 5, label: $_("LM Region") },
    { key: "subset_key", colSpan: 5, label: $_("Subset") },
    { key: "TOTAL", colSpan: 3, label: $_("#Total deals"), submodel: "data" },
    { key: "actions", colSpan: 3, label: $_("Actions") },
  ]

  let selectedItemId: number | null = null

  const onClickEntry = (id: number) => {
    selectedItemId = id === selectedItemId ? null : id
  }
  const download = (item: Item) => {
    a_download(
      "data:application/json;charset=utf-8," + encodeURIComponent(JSON.stringify(item)),
      "data-quality-indicators.json",
    )
  }

  interface Filter {
    startDate: Date
    endDate: Date
    region: number | null | "none"
    subset: string | null | "none"
  }
  let filter: Filter = {
    startDate: dayjs().subtract(90, "day").toDate(),
    endDate: new Date(),
    region: "none",
    subset: "none",
  }

  $: satisfiesFilter = (item: components["schemas"]["DealQISnapshot"]): boolean => {
    const date = new Date(item.created_at)
    return (
      date >= filter.startDate &&
      date <= filter.endDate &&
      (filter.region === "none" || item.region === filter.region) &&
      (filter.subset === "none" || item.subset_key === filter.subset)
    )
  }
</script>

<div class="flex items-center gap-4 p-2">
  <DateInput
    id="qi-start-date-input"
    bind:value={filter.startDate}
    format="yyyy-MM-dd"
    browseWithoutSelecting
  />
  <DateInput
    id="qi-end-date-input"
    bind:value={filter.endDate}
    format="yyyy-MM-dd"
    browseWithoutSelecting
  />

  <select id="qi-region-select" class="inpt w-40" bind:value={filter.region}>
    <option value={"none"} selected>{$_("All Regions")}</option>
    <option value={null}>{$_("Global")}</option>
    {#each $page.data.regions as region}
      <option value={region.id}>{region.name}</option>
    {/each}
  </select>

  <select id="qi-subset-select" class="inpt w-40" bind:value={filter.subset}>
    <option value={"none"} selected>{$_("Any Subset")}</option>
    <option value={null}>{$_("Unfiltered")}</option>
    {#await qiPromise then qiSpecs}
      {#each qiSpecs.deal_subset as subset}
        <option value={subset.key}>{subset.description}</option>
      {/each}
    {/await}
  </select>
</div>

<div class="h-[400px] border border-white">
  {#await Promise.all([qiPromise, statsPromise])}
    <LoadingSpinner />
  {:then [data, stats]}
    {@const filtered = stats[model].filter(satisfiesFilter)}
    {@const item = filtered.find(item => item.id === selectedItemId)}

    <Table {columns} items={filtered} rowHeightInPx={35} headerHeightInPx={45}>
      <svelte:fragment slot="field" let:fieldName let:obj>
        {#if fieldName === "subset_key"}
          {data.deal_subset.find(x => x.key === obj.subset_key)?.description ?? "-----"}
        {:else if fieldName === "region"}
          {$page.data.regions.find(r => r.id === obj["region"])?.name ?? "-----"}
        {:else if fieldName === "TOTAL"}
          {obj["data"]["TOTAL"]}
        {:else if fieldName === "created_at"}
          <DateTimeField value={obj["created_at"]} />
        {:else if fieldName === "actions"}
          <span class="space-x-2">
            <button
              title={$_("Download")}
              on:click|stopPropagation={() => download(obj)}
            >
              <DownloadIcon />
            </button>
            <button
              title={$_("View")}
              on:click|stopPropagation={() => onClickEntry(obj.id)}
            >
              <EyeIcon />
            </button>
          </span>
        {/if}
      </svelte:fragment>
    </Table>

    {#if item}
      <div
        transition:fade={{ duration: 100 }}
        role="none"
        class="fixed inset-0 z-[100] flex h-screen max-h-screen w-screen items-center justify-center bg-[rgba(0,0,0,0.3)] backdrop-blur-sm"
      >
        <div
          transition:slide={{ duration: 150 }}
          class="max-h-[90vh] w-2/3 overflow-y-auto border bg-white p-2 text-black shadow-xl dark:bg-gray-700 dark:text-white"
          on:outClick={() => {
            selectedItemId = null
          }}
          use:clickOutside
        >
          <h3 class="heading4">{$_("Deal Quality Indicators")}</h3>
          <div class="my-4 flex gap-4 font-bold">
            <span><DateTimeField value={item.created_at} /></span>
            <span>
              {$page.data.regions.find(r => r.id === item.region)?.name ?? "-----"}
            </span>
            <span>
              {data.deal_subset.find(x => x.key === item.subset_key)?.description ??
                "-----"}
            </span>
            <span>{item.data.TOTAL}</span>
          </div>

          <ul class="flex flex-col gap-2 border-r border-orange">
            <li class="grid grid-cols-12 gap-2 font-bold">
              <span class="col-span-8 lg:col-span-10">{$_("Name")}</span>
              <span class="col-span-2 lg:col-span-1">{$_("Count")}</span>
              <span class="col-span-2 lg:col-span-1">{$_("Ratio")}</span>
            </li>

            {#each data[model] as qi (qi.key)}
              <li
                class="grid w-full grid-cols-12 flex-nowrap items-center gap-2 text-left text-gray-700 dark:text-white"
                title={qi.description}
              >
                <span class="col-span-8 lg:col-span-10">
                  {qi.description}
                </span>
                <span class="col-span-2 lg:col-span-1">
                  {item.data[qi.key]}
                </span>
                <span class="col-span-2 lg:col-span-1">
                  {formatRatio(item.data[qi.key], item.data["TOTAL"])}
                </span>
              </li>
            {/each}
          </ul>
        </div>
      </div>
    {/if}
  {/await}
</div>
