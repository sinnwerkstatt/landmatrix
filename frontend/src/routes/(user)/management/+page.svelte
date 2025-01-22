<script lang="ts">
  import dayjs from "dayjs"
  import isSameOrAfter from "dayjs/plugin/isSameOrAfter"
  import isSameOrBefore from "dayjs/plugin/isSameOrBefore"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import { twMerge } from "tailwind-merge"

  import { browser } from "$app/environment"
  import { goto } from "$app/navigation"
  import { page } from "$app/state"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { loading } from "$lib/stores/basics"
  import { type DealHull, type InvestorHull } from "$lib/types/data"
  import { isAdmin } from "$lib/utils/permissions"

  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import AdjustmentsIcon from "$components/icons/AdjustmentsIcon.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import Table, { type Column } from "$components/Table/Table.svelte"

  import { downloadAsCSV, downloadAsXLSX } from "./downloadObjects"
  import RightFilterBar from "./RightFilterBar.svelte"
  import { managementFilters } from "./state"
  import WorkflowInfoView from "./WorkflowInfoView.svelte"

  dayjs.extend(isSameOrBefore)
  dayjs.extend(isSameOrAfter)

  // FIXME
  let userIsEditorOrAbove = $derived(isAdmin(page.data.user))

  let model: "deal" | "investor" = $state("deal")
  let activeTabId: string = $state("")
  let objects: Array<DealHull | InvestorHull> = $state([])

  let isDeal = $derived(model === "deal")

  interface Tab {
    id: string
    name: string
    staff?: boolean
    count?: number
    useWorkflowInfoView?: boolean
  }

  let navTabs: { name: string; expanded?: boolean; items: Tab[] }[] = $derived([
    {
      name: $_("Todo"),
      items: [
        {
          id: "todo_feedback",
          name: $_("Feedback for me"),
          useWorkflowInfoView: true,
        },
        {
          id: "todo_improvement",
          name: $_("Improvement requests for me"),
          useWorkflowInfoView: true,
        },
        { id: "todo_review", name: $_("Review"), staff: true },
        { id: "todo_activation", name: $_("Activation"), staff: true },
      ],
    },
    {
      name: $_("My requests"),
      items: [
        {
          id: "requested_feedback",
          name: $_("Feedback by me"),
          useWorkflowInfoView: true,
        },
        {
          id: "requested_improvement",
          name: $_("Improvements requested by me"),
          staff: true,
          useWorkflowInfoView: true,
        },
      ],
    },
    {
      name: $_("My data"),
      items: [
        { id: "my_drafts", name: $_("My drafts") },
        { id: "created_by_me", name: $_("Created by me") },
        { id: "modified_by_me", name: $_("Modified by me") },
        { id: "reviewed_by_me", name: $_("Reviewed by me"), staff: true },
        { id: "activated_by_me", name: $_("Activated by me"), staff: true },
      ],
    },
    {
      name: $_("Data overview"),
      items: [
        { id: "all_active", name: $_("All active"), staff: true },
        { id: "all_drafts", name: $_("All non active"), staff: true },
        // TODO Kurt who should be allowed to see all_deleted?
        { id: "all_deleted", name: $_("All deleted"), staff: true },
      ],
    },
  ])

  let flatTabs = $derived(
    navTabs.map(x => x.items).reduce((acc, items) => [...acc, ...items], []),
  )

  let activeTab: Tab = $derived(flatTabs.find(item => item.id === activeTabId)!)

  let dealColumns: Column[] = $derived(
    [
      { key: "id", colSpan: 1 },
      { key: "status", colSpan: 2 },
      { key: "country_id", colSpan: 2 },
      { key: "deal_size", colSpan: 2, submodel: "selected_version" },
      {
        key: "current_intention_of_investment",
        colSpan: 2,
        submodel: "selected_version",
      },
      { key: "first_created_at", colSpan: 3, label: $_("Created") },
      { key: "modified_at", colSpan: 3, label: $_("Modified") },
      { key: "fully_updated", colSpan: 2, submodel: "selected_version" },
      { key: "workflowinfos", colSpan: 5 },
    ].map(c => ({ ...c, label: c.label || $dealFields[c.key].label })),
  )

  let investorColumns: Column[] = $derived(
    [
      { key: "id", colSpan: 1 },
      { key: "status", colSpan: 2 },
      { key: "name", colSpan: 3, submodel: "selected_version" },
      { key: "country_id", colSpan: 3, submodel: "selected_version" },
      { key: "first_created_at", colSpan: 3, label: $_("Created") },
      { key: "modified_at", colSpan: 3, label: $_("Modified") },
      { key: "workflowinfos", colSpan: 5 },
    ].map(c => ({ ...c, label: c.label || $investorFields[c.key].label })),
  )

  let columns = $derived(isDeal ? dealColumns : investorColumns)

  let counts: { [key: string]: number } = $state({})
  const getCounts = async (model: "deal" | "investor") => {
    if (!browser) return

    const ret = await fetch(`/api/management/?model=${model}&action=counts`)

    if (ret.ok) {
      counts = await ret.json()
    }
  }
  $effect(() => {
    getCounts(model)
  })

  let controller: AbortController
  let createdByUserIDs = $state(new Set<number>())
  let modifiedByUserIDs = $state(new Set<number>())

  async function fetchObjects(acTab: string, model: "deal" | "investor") {
    if (!acTab) return
    if (controller) controller.abort()

    loading.set(true)
    controller = new AbortController()
    const ret = await fetch(`/api/management/?model=${model}&action=${acTab}`, {
      signal: controller.signal,
    })
    if (ret.ok) {
      objects = (await ret.json()).objects

      // set User lists for the right filter bar
      createdByUserIDs = new Set<number>()
      modifiedByUserIDs = new Set<number>()
      objects.forEach(o => {
        if (o.first_created_by_id) createdByUserIDs.add(o.first_created_by_id)
        if (o.selected_version.modified_by_id)
          modifiedByUserIDs.add(o.selected_version.modified_by_id)
      })

      counts[acTab] = objects.length
    }

    loading.set(false)
  }

  onMount(() => {
    if (!page.url.hash) goto("#todo_feedback")
  })

  const activateTab = (hash: string): void => {
    const item = flatTabs.find(item => `#${item.id}` === hash)
    if (item) {
      activeTabId = item.id
    }
  }

  $effect(() => {
    activateTab(page.url.hash)
  })

  let showFilterOverlay = $state(false)

  $effect(() => {
    fetchObjects(activeTabId, model)
  })
  // TODO?: Move filters to backend
  let filteredObjects = $derived(
    objects.filter(obj => {
      if ($managementFilters.status)
        if (obj.status !== $managementFilters.status) return false
      if ($managementFilters.country)
        if (isDeal) {
          if ((obj as DealHull).country_id !== $managementFilters.country.id)
            return false
        } else {
          if (
            (obj as InvestorHull).selected_version.country_id !==
            $managementFilters.country.id
          )
            return false
        }
      if ($managementFilters.createdAtFrom)
        if (
          dayjs(obj.first_created_at).isBefore($managementFilters.createdAtFrom, "day")
        )
          return false
      if ($managementFilters.createdAtTo)
        if (dayjs(obj.first_created_at).isAfter($managementFilters.createdAtTo, "day"))
          return false
      if ($managementFilters.createdByID)
        if (obj.first_created_by_id !== $managementFilters.createdByID) return false

      if ($managementFilters.modifiedAtFrom)
        if (
          dayjs(obj.selected_version.modified_at).isBefore(
            $managementFilters.modifiedAtFrom,
            "day",
          )
        )
          return false
      if ($managementFilters.modifiedAtTo)
        if (
          dayjs(obj.selected_version.modified_at).isAfter(
            $managementFilters.modifiedAtTo,
            "day",
          )
        )
          return false
      if ($managementFilters.modifiedByID)
        if (obj.selected_version.modified_by_id !== $managementFilters.modifiedByID)
          return false

      if (isDeal) {
        const deal = obj as DealHull

        if ($managementFilters.dealSizeFrom)
          if ((deal.selected_version.deal_size ?? 0) < $managementFilters.dealSizeFrom)
            return false
        if ($managementFilters.dealSizeTo)
          if ((deal.selected_version.deal_size ?? 0) > $managementFilters.dealSizeTo)
            return false
        if ($managementFilters.intentionOfInvestment)
          if (
            !deal.selected_version.current_intention_of_investment.includes(
              $managementFilters.intentionOfInvestment,
            )
          )
            return false
        if ($managementFilters.fullyUpdatedAtFrom)
          if (
            !deal.fully_updated_at ||
            dayjs(deal.fully_updated_at).isBefore(
              $managementFilters.fullyUpdatedAtFrom,
              "day",
            )
          )
            return false
        if ($managementFilters.fullyUpdatedAtTo)
          if (
            !deal.fully_updated_at ||
            dayjs(deal.fully_updated_at).isAfter(
              $managementFilters.fullyUpdatedAtTo,
              "day",
            )
          )
            return false
      }

      return true
    }),
  )

  const wrapperClass = "p-1"
  const valueClass = "text-gray-700 dark:text-white"
</script>

<svelte:head>
  <title>{$_("Management")} | {$_("Land Matrix")}</title>
</svelte:head>

<div class="relative flex h-full w-full">
  <nav
    class="h-full shrink-0 basis-1/4 flex-col overflow-y-scroll bg-white/80 p-2 drop-shadow-[3px_-3px_1px_rgba(0,0,0,0.3)] xl:basis-1/6 dark:bg-gray-700"
  >
    <div
      class="flex justify-center gap-4 border-b border-gray-200 pb-6 pt-1 text-lg font-bold"
    >
      <button
        class={isDeal
          ? "border-b border-orange text-orange"
          : "text-gray-600 hover:text-orange dark:text-white"}
        onclick={() => (model = "deal")}
        type="button"
      >
        {$_("Deals")}
      </button>
      <button
        class={model === "investor"
          ? "border-b border-pelorous text-pelorous"
          : "text-gray-600 hover:text-pelorous dark:text-white"}
        onclick={() => (model = "investor")}
        type="button"
      >
        {$_("Investors")}
      </button>
    </div>
    <div class="w-full self-start">
      {#each navTabs as { name, items }}
        {#if userIsEditorOrAbove || !items.every(i => i.staff)}
          <FilterCollapse title={name} expanded>
            <ul>
              {#each items.filter(i => userIsEditorOrAbove || !i.staff) as item}
                <li
                  class={twMerge(
                    "py-2 pr-4",
                    isDeal ? "border-orange" : "border-pelorous",
                    activeTabId === item.id ? "border-r-4" : "border-r",
                  )}
                >
                  <a
                    class={twMerge(
                      "block text-left",
                      isDeal ? "hover:text-orange" : "hover:text-pelorous",
                      activeTabId === item.id
                        ? isDeal
                          ? "font-bold text-orange"
                          : "font-bold text-pelorous"
                        : "text-gray-700 dark:text-white",
                    )}
                    href="#{item.id}"
                  >
                    {item.name}
                    {#if counts[item.id]}
                      ({counts[item.id]})
                    {/if}
                  </a>
                </li>
              {/each}
            </ul>
          </FilterCollapse>
        {/if}
      {/each}
    </div>
    <div class="mt-auto w-full self-end pt-10">
      {#if activeTabId && filteredObjects.length > 0}
        <FilterCollapse title={$_("Download")}>
          <ul>
            <li>
              <button
                class="text-orange hover:text-orange-200"
                onclick={() => downloadAsXLSX(filteredObjects, model, activeTabId)}
              >
                <DownloadIcon />
                {$_("All attributes")} (xlsx)
              </button>
            </li>
            <li>
              <button
                class="text-orange hover:text-orange-200"
                onclick={() => downloadAsCSV(filteredObjects, model, activeTabId)}
              >
                <DownloadIcon />
                {$_("All attributes")} (csv)
              </button>
            </li>
          </ul>
        </FilterCollapse>
      {/if}
    </div>
  </nav>

  <div class="mt-[60px] w-1 grow px-6 pb-6">
    {#if activeTab?.useWorkflowInfoView}
      <WorkflowInfoView objects={filteredObjects} {model} tabId={activeTab.id} />
    {:else}
      <Table items={filteredObjects} {columns}>
        {#snippet field({ fieldName, obj })}
          {@const col = columns.find(c => c.key === fieldName)}

          {#if col?.key === "first_created_at"}
            <DisplayField
              fieldname="first_created_at"
              value={obj.first_created_at}
              {model}
              {wrapperClass}
              {valueClass}
            />
            <DisplayField
              fieldname="first_created_by_id"
              value={obj.first_created_by_id}
              {model}
              {wrapperClass}
              {valueClass}
            />
          {:else if col?.key === "modified_at"}
            <DisplayField
              fieldname="modified_at"
              value={obj.selected_version.modified_at}
              {model}
              {wrapperClass}
              {valueClass}
            />
            <DisplayField
              fieldname="modified_by_id"
              value={obj.selected_version.modified_by_id}
              {model}
              {wrapperClass}
              {valueClass}
            />
          {:else if col}
            <DisplayField
              fieldname={col.key}
              value={col.submodel ? obj[col.submodel][col.key] : obj[col.key]}
              {model}
              {wrapperClass}
              {valueClass}
              extras={col.key === "id"
                ? { model, objectVersion: obj.draft_version_id }
                : undefined}
            />
          {/if}
        {/snippet}
      </Table>
    {/if}
  </div>

  <RightFilterBar
    {createdByUserIDs}
    {model}
    {modifiedByUserIDs}
    {objects}
    showFilters={showFilterOverlay}
  />

  <button
    class="group absolute right-4 top-2 rounded-full bg-gray-700 p-1 drop-shadow-[3px_3px_1px_rgba(125,125,125,.7)] transition-colors hover:bg-gray-100 hover:drop-shadow-lg"
    onclick={() => (showFilterOverlay = !showFilterOverlay)}
    type="button"
  >
    <AdjustmentsIcon
      class="h-8 w-8 text-white transition-colors group-hover:text-orange"
    />
  </button>
</div>
