<script lang="ts">
  import cn from "classnames"
  import dayjs from "dayjs"
  import isSameOrAfter from "dayjs/plugin/isSameOrAfter"
  import isSameOrBefore from "dayjs/plugin/isSameOrBefore"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import { dealFields, investorFields } from "$lib/fieldLookups"
  import { loading } from "$lib/stores/basics"
  import type { DealHull, InvestorHull } from "$lib/types/newtypes"
  import { UserRole } from "$lib/types/user"

  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import AdjustmentsIcon from "$components/icons/AdjustmentsIcon.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import Table, { type Column } from "$components/Table/Table.svelte"

  import { downloadAsCSV, downloadAsXLSX } from "./downloadObjects.js"
  import RightFilterBar from "./RightFilterBar.svelte"
  import { managementFilters } from "./state"
  import WorkflowInfoView from "./WorkflowInfoView.svelte"

  dayjs.extend(isSameOrBefore)
  dayjs.extend(isSameOrAfter)

  $: userIsEditorOrAbove = $page.data.user.role > UserRole.EDITOR

  let model: "deal" | "investor" = "deal"
  let activeTabId: string
  let objects: Array<DealHull | InvestorHull> = []

  interface Tab {
    id: string
    name: string
    staff?: boolean
    count?: number
    useWorkflowInfoView?: boolean
  }

  let navTabs: { name: string; expanded?: boolean; items: Tab[] }[] = []
  $: navTabs = [
    {
      name: $_("Todo"),
      items: [
        { id: "todo_feedback", name: $_("Feedback for me"), useWorkflowInfoView: true },
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
  ]
  $: flatTabs = navTabs.map(x => x.items).reduce((acc, items) => [...acc, ...items], [])

  let activeTab: Tab
  $: activeTab = flatTabs.find(item => item.id === activeTabId)!

  let dealColumns: Column[]
  $: dealColumns = [
    { key: "id", colSpan: 1 },
    { key: "status", colSpan: 2 },
    { key: "country_id", colSpan: 2 },
    { key: "deal_size", colSpan: 2, submodel: "selected_version" },
    { key: "first_created_at", colSpan: 2 },
    { key: "first_created_by_id", colSpan: 2 },
    { key: "modified_at", colSpan: 2, submodel: "selected_version" },
    { key: "modified_by_id", colSpan: 2, submodel: "selected_version" },
    { key: "fully_updated", colSpan: 2, submodel: "selected_version" },
    { key: "workflowinfos", colSpan: 5 },
  ].map(c => ({ ...c, label: $dealFields[c.key].label }))

  let investorColumns: Column[]
  $: investorColumns = [
    { key: "id", colSpan: 1 },
    { key: "status", colSpan: 2 },
    { key: "name", colSpan: 3, submodel: "selected_version" },
    { key: "country_id", colSpan: 4, submodel: "selected_version" },
    { key: "first_created_at", colSpan: 2 },
    { key: "first_created_by_id", colSpan: 3 },
    { key: "workflowinfos", colSpan: 5 },
  ].map(c => ({ ...c, label: $investorFields[c.key].label }))

  $: columns = model === "deal" ? dealColumns : investorColumns

  async function getCounts(model: "deal" | "investor") {
    if (!browser) return
    const ret = await fetch(`/api/management/?model=${model}&action=counts`)
    if (ret.ok) {
      const counts = await ret.json()
      navTabs = navTabs.map(navTab => ({
        ...navTab,
        items: navTab.items.map(item => ({ ...item, count: counts?.[item.id] ?? 0 })),
      }))
    }
  }

  let controller: AbortController
  let createdByUserIDs = new Set<number>()
  let modifiedByUserIDs = new Set<number>()

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

      navTabs = navTabs.map(navTab => ({
        ...navTab,
        items: navTab.items.map(item => {
          if (item.id === acTab) return { ...item, count: objects.length }
          return item
        }),
      }))
      navTabs = [...navTabs]
    }

    loading.set(false)
  }

  onMount(() => {
    if (!$page.url.hash) goto("#todo_feedback")
  })

  const activateTab = (hash: string): void => {
    const item = flatTabs.find(item => `#${item.id}` === hash)
    if (item) {
      activeTabId = item.id
    }
  }

  $: activateTab($page.url.hash)

  let showFilterOverlay = false

  $: getCounts(model)
  $: fetchObjects(activeTabId, model)
  $: filteredObjects = objects.filter(obj => {
    if ($managementFilters.status)
      if (obj.status !== $managementFilters.status) return false
    if ($managementFilters.country)
      if (model === "deal") {
        if ((obj as DealHull).country_id !== $managementFilters.country.id) return false
      } else {
        if (
          (obj as InvestorHull).selected_version.country_id !==
          $managementFilters.country.id
        )
          return false
      }
    if ($managementFilters.createdAtFrom)
      if (dayjs(obj.first_created_at).isBefore($managementFilters.createdAtFrom, "day"))
        return false
    if ($managementFilters.createdAtTo)
      if (dayjs(obj.first_created_at).isAfter($managementFilters.createdAtTo, "day"))
        return false
    if ($managementFilters.createdBy)
      if (obj.first_created_by_id !== $managementFilters.createdBy.id) return false

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
    if ($managementFilters.modifiedBy)
      if (obj.selected_version.modified_by_id !== $managementFilters.modifiedBy.id)
        return false

    if (model === "deal") {
      const deal = obj as DealHull

      if ($managementFilters.dealSizeFrom)
        if (deal.selected_version.deal_size < $managementFilters.dealSizeFrom)
          return false
      if ($managementFilters.dealSizeTo)
        if (deal.selected_version.deal_size > $managementFilters.dealSizeTo)
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
  })

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
        class={model === "deal"
          ? "border-b border-orange text-orange"
          : "text-gray-600 hover:text-orange dark:text-white"}
        on:click={() => (model = "deal")}
        type="button"
      >
        {$_("Deals")}
      </button>
      <button
        class={model === "investor"
          ? "border-b border-pelorous text-pelorous"
          : "text-gray-600 hover:text-pelorous dark:text-white"}
        on:click={() => (model = "investor")}
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
                  class={cn(
                    "py-2 pr-4",
                    model === "deal" ? "border-orange" : "border-pelorous",
                    activeTabId === item.id ? "border-r-4" : "border-r",
                  )}
                >
                  <a
                    class={cn(
                      "block text-left",
                      model === "deal" ? "hover:text-orange" : "hover:text-pelorous",
                      activeTabId === item.id
                        ? model === "deal"
                          ? "font-bold text-orange"
                          : "font-bold text-pelorous"
                        : "text-gray-700 dark:text-white",
                    )}
                    href="#{item.id}"
                  >
                    {item.name}
                    {#if item.count}
                      ({item.count})
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
                on:click={() => downloadAsXLSX(filteredObjects, model, activeTabId)}
              >
                <DownloadIcon />
                {$_("All attributes")} (xlsx)
              </button>
            </li>
            <li>
              <button
                class="text-orange hover:text-orange-200"
                on:click={() => downloadAsCSV(filteredObjects, model, activeTabId)}
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
        <svelte:fragment slot="field" let:fieldName let:obj>
          {@const col = columns.find(c => c.key === fieldName)}
          <DisplayField
            fieldname={col.key}
            value={col.submodel ? obj[col.submodel][col.key] : obj[col.key]}
            {model}
            {wrapperClass}
            {valueClass}
            extras={col.key === "id"
              ? { model, objectVersion: obj.draft_version_id }
              : {}}
          />
        </svelte:fragment>
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
    on:click={() => (showFilterOverlay = !showFilterOverlay)}
    type="button"
  >
    <AdjustmentsIcon
      class="h-8 w-8 text-white transition-colors group-hover:text-orange"
    />
  </button>
</div>
