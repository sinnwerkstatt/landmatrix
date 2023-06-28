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

  import { formfields, loading } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import type { User } from "$lib/types/user"
  import { UserRole } from "$lib/types/user"

  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import AdjustmentsIcon from "$components/icons/AdjustmentsIcon.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import Table from "$components/Table/Table.svelte"

  import RightFilterBar from "./RightFilterBar.svelte"
  import { managementFilters } from "./state"
  import { downloadAsCSV, downloadAsXLSX } from "./downloadObjects.js"
  import WorkflowInfoView from "./WorkflowInfoView.svelte"

  dayjs.extend(isSameOrBefore)
  dayjs.extend(isSameOrAfter)

  interface Tab {
    id: string
    name: string
    staff?: boolean
    count?: number
  }

  const user = $page.data.user

  let model: "deal" | "investor" = "deal"
  let activeTabId: string
  let objects: Array<Deal | Investor> = []

  let navTabs: { name: string; expanded?: boolean; items: Tab[] }[]
  $: navTabs = [
    {
      name: $_("Todo"),
      items: [
        { id: "todo_feedback", name: $_("Feedback for me") },
        { id: "todo_improvement", name: $_("Improvement requests for me") },
        { id: "todo_review", name: $_("Review"), staff: true },
        { id: "todo_activation", name: $_("Activation"), staff: true },
      ],
    },
    {
      name: $_("My requests"),
      items: [
        { id: "requested_feedback", name: $_("Feedback by me") },
        {
          id: "requested_improvement",
          name: $_("Improvements requested by me"),
          staff: true,
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
        { id: "all_items", name: $_("All objects"), staff: true },
        { id: "all_drafts", name: $_("All non active"), staff: true },
        { id: "all_deleted", name: $_("All deleted"), staff: true },
      ],
    },
  ]

  const dealColumns = {
    id: 1,
    country: 2,
    deal_size: 2,
    created_at: 2,
    created_by: 2,
    modified_at: 2,
    modified_by: 2,
    fully_updated_at: 2,
    workflowinfos: 5,
    // combined_status: 1,
  }

  const investorColumns = {
    id: 1,
    name: 3,
    country: 4,
    deals: 1,
    created_at: 2,
    created_by: 3,
    workflowinfos: 5,
    // combined_status: 1,
  }

  $: columnsWithSpan = model === "deal" ? dealColumns : investorColumns
  $: columns = Object.keys(columnsWithSpan)
  $: labels = columns.map(col => $formfields?.[model]?.[col]?.label)
  $: spans = Object.entries(columnsWithSpan).map(([, colSpan]) => colSpan)

  async function getCounts(model) {
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
  let createdByUsers: User[] = []
  let modifiedByUsers: User[] = []

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
      createdByUsers = []
      modifiedByUsers = []
      const createdBy = new Set<number>()
      const modifiedBy = new Set<number>()
      objects.forEach(o => {
        if (o.created_by && !createdBy.has(o.created_by.id)) {
          createdByUsers.push(o.created_by)
          createdBy.add(o.created_by.id)
        }
        if (o.modified_by && !modifiedBy.has(o.modified_by.id)) {
          modifiedByUsers.push(o.modified_by)
          modifiedBy.add(o.modified_by.id)
        }
      })
      createdByUsers = createdByUsers.sort((a, b) =>
        a.full_name.localeCompare(b.full_name),
      )
      modifiedByUsers = modifiedByUsers.sort((a, b) =>
        a.full_name.localeCompare(b.full_name),
      )

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

  async function activateTab(hash) {
    navTabs.some(navTab => {
      const item = navTab.items.find(i => "#" + i.id === hash)
      if (item) {
        activeTabId = item.id
        return true
      }
    })
  }

  let showFilterOverlay = false

  $: activateTab($page.url.hash)
  $: getCounts(model)
  $: fetchObjects(activeTabId, model)
  $: filteredObjects = objects.filter(d => {
    if ($managementFilters.country)
      if (d.country?.id !== $managementFilters.country.id) return false

    if ($managementFilters.createdAtFrom)
      if (dayjs(d.created_at).isBefore($managementFilters.createdAtFrom, "day"))
        return false
    if ($managementFilters.createdAtTo)
      if (dayjs(d.created_at).isAfter($managementFilters.createdAtTo, "day"))
        return false
    if ($managementFilters.createdBy)
      if (d.created_by?.id !== $managementFilters.createdBy.id) return false

    if ($managementFilters.modifiedAtFrom)
      if (dayjs(d.modified_at).isBefore($managementFilters.modifiedAtFrom, "day"))
        return false
    if ($managementFilters.modifiedAtTo)
      if (dayjs(d.modified_at).isAfter($managementFilters.modifiedAtTo, "day"))
        return false
    if ($managementFilters.modifiedBy)
      if (d.modified_by?.id !== $managementFilters.modifiedBy.id) return false

    if (model === "deal") {
      if ($managementFilters.dealSizeFrom)
        if (d.deal_size < $managementFilters.dealSizeFrom) return false
      if ($managementFilters.dealSizeTo)
        if (d.deal_size > $managementFilters.dealSizeTo) return false

      if ($managementFilters.fullyUpdatedAtFrom)
        if (
          dayjs(d.fully_updated_at).isBefore(
            $managementFilters.fullyUpdatedAtFrom,
            "day",
          )
        )
          return false
      if ($managementFilters.fullyUpdatedAtTo)
        if (
          dayjs(d.fully_updated_at).isAfter($managementFilters.fullyUpdatedAtTo, "day")
        )
          return false
    }

    return true
  })
  const WORKFLOWINFO_VIEWS = [
    "todo_feedback",
    "todo_improvement",
    "requested_feedback",
    "requested_improvement",
  ]
</script>

<svelte:head>
  <title>{$_("Management")} | {$_("Land Matrix")}</title>
</svelte:head>

<div class="relative flex h-full w-full">
  <nav
    class="h-full shrink-0 basis-1/4 flex-col overflow-y-scroll bg-white/80 p-2 drop-shadow-[3px_-3px_1px_rgba(0,0,0,0.3)] dark:bg-gray-700 xl:basis-1/6"
  >
    <div
      class="flex justify-center gap-4 border-b border-gray-200 pt-1 pb-6 text-lg font-bold"
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
        {#if user.role > UserRole.EDITOR || !items.every(i => i.staff)}
          <FilterCollapse title={name} expanded>
            <ul>
              {#each items.filter(i => user.role > UserRole.EDITOR || !i.staff) as item}
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
                        : "text-lm-dark dark:text-white",
                    )}
                    href="#{item.id}"
                  >
                    {item.name}
                    {#if item.count} ({item.count}){/if}
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
    {#if WORKFLOWINFO_VIEWS.includes(activeTabId)}
      <WorkflowInfoView objects={filteredObjects} {model} tabId={activeTabId} />
    {:else}
      <Table items={filteredObjects} {columns} {spans} {labels}>
        <DisplayField
          slot="field"
          let:fieldName
          let:obj
          wrapperClasses="p-1"
          valueClasses="text-lm-dark dark:text-white"
          fieldname={fieldName}
          value={obj[fieldName]}
          objectVersion={obj.current_draft_id}
          {model}
        />
      </Table>
    {/if}
  </div>

  <RightFilterBar
    {model}
    {objects}
    {createdByUsers}
    {modifiedByUsers}
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
