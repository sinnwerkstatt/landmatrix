<script lang="ts">
  import cn from "classnames"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import { formfields, loading } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"
  import type { Investor } from "$lib/types/investor"
  import { UserLevel } from "$lib/types/user"

  import FilterCollapse from "$components/Data/FilterCollapse.svelte"
  import DisplayField from "$components/Fields/DisplayField.svelte"
  import AdjustmentsIcon from "$components/icons/AdjustmentsIcon.svelte"
  import DownloadIcon from "$components/icons/DownloadIcon.svelte"
  import Table from "$components/table/Table.svelte"

  import FilterOverlay from "./FilterOverlay.svelte"
  import RequestedFeedbackView from "./RequestedFeedbackView.svelte"
  import RequestedImprovementView from "./RequestedImprovementView.svelte"
  import { managementFilters } from "./state"
  import TodoFeedbackView from "./TodoFeedbackView.svelte"

  interface Tab {
    id: string
    name: string
    staff?: boolean
    count?: number
  }

  const user = $page.data.user

  let model: "deal" | "investor" = "deal"
  let activeTab: Tab
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

  const selectTab = (tab: Tab) => {
    goto("#" + tab.id)
    activeTab = tab
  }

  const dealColumns = {
    id: 1,
    country: 2,
    deal_size: 1,
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
    name: 2,
    country: 3,
    deals: 1,
    created_at: 2,
    created_by: 2,
    workflowinfos: 5,
    // combined_status: 1,
  }

  $: columnsWithSpan = model === "deal" ? dealColumns : investorColumns
  $: columns = Object.keys(columnsWithSpan)
  $: labels = columns.map(col => $formfields?.[model]?.[col]?.label)
  $: spans = Object.entries(columnsWithSpan).map(([_, colSpan]) => colSpan)

  let controller: AbortController

  async function getCounts(model) {
    if (!browser) return
    const x = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/management/?model=${model}&action=counts`,
    )
    if (x.ok) {
      const counts = await x.json()
      navTabs = navTabs.map(navTab => ({
        ...navTab,
        items: navTab.items.map(item => ({ ...item, count: counts?.[item.id] ?? 0 })),
      }))
    }
  }

  async function fetchObjects(acTab: Tab, model: "deal" | "investor") {
    if (!acTab) return
    if (controller) controller.abort()

    loading.set(true)
    controller = new AbortController()
    const x = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/management/?model=${model}&action=${
        acTab.id
      }`,
      {
        signal: controller.signal,
      },
    )
    if (x.ok) {
      objects = (await x.json()).objects
      acTab.count = objects.length
      navTabs = [...navTabs]
    }

    loading.set(false)
  }

  $: getCounts(model)
  $: fetchObjects(activeTab, model)

  onMount(() => {
    navTabs.some(navTab => {
      const hash = $page.url.hash || "#todo_feedback"
      const item = navTab.items.find(i => "#" + i.id === hash)
      if (item) {
        selectTab(item)
        return true
      }
    })
  })

  function trackDownload(format) {
    // TODO implement this? ${format}
  }

  let showFilterOverlay = false

  $: filteredObjects = objects.filter(d => {
    if ($managementFilters.country?.id)
      return d.country?.id === $managementFilters.country.id
    return true
  })
</script>

<svelte:head>
  <title>{$_("Management")} | {$_("Land Matrix")}</title>
</svelte:head>

<div class="relative flex min-h-full w-full">
  <nav
    class="flex min-h-full flex-initial flex-shrink-0 flex-col bg-white/80 p-2 drop-shadow-[3px_-3px_3px_rgba(0,0,0,0.3)]"
  >
    <div
      class="flex justify-center gap-4 border-b border-gray-200 p-1 pb-6 text-lg font-bold"
    >
      <button
        class={model === "deal"
          ? "border-b border-solid border-black text-black"
          : "text-gray-500 hover:text-gray-600"}
        on:click={() => (model = "deal")}
        type="button"
      >
        {$_("Deals")}
      </button>
      <button
        class={model === "investor"
          ? "border-b border-solid border-black text-black"
          : "text-gray-500 hover:text-gray-600"}
        on:click={() => (model = "investor")}
        type="button"
      >
        {$_("Investors")}
      </button>
    </div>
    <div class="w-full self-start">
      {#each navTabs as { name, items }}
        {#if user.level > UserLevel.EDITOR || !items.every(i => i.staff)}
          <FilterCollapse title={name} expanded>
            <ul>
              {#each items.filter(i => user.level > UserLevel.EDITOR || !i.staff) as item}
                <li
                  class={cn(
                    "py-2 pr-4",
                    model === "deal" ? "border-orange" : "border-pelorous",
                    activeTab === item ? "border-r-4" : "border-r",
                  )}
                >
                  <button
                    class={cn(
                      "w-full text-left",
                      activeTab === item
                        ? model === "deal"
                          ? "font-bold text-orange"
                          : "font-bold text-pelorous"
                        : "text-gray-600",
                    )}
                    on:click={() => selectTab(item)}
                  >
                    {item.name}
                    {#if item.count} ({item.count}){/if}
                  </button>
                </li>
              {/each}
            </ul>
          </FilterCollapse>
        {/if}
      {/each}
    </div>
    <div class="mt-auto w-full self-end pt-10">
      {#if activeTab}
        <FilterCollapse title={$_("Download")}>
          <ul>
            <li>
              <a
                href="/api/management?format=xlsx&action={activeTab.id}"
                on:click={() => trackDownload("xlsx")}
                rel="external"
              >
                <DownloadIcon />
                {$_("All attributes")} (xlsx)
              </a>
            </li>
            <li>
              <a
                href="/api/management?format=csv&action={activeTab.id}"
                on:click={() => trackDownload("csv")}
                rel="external"
              >
                <i class="fas fa-file-download" />
                <DownloadIcon />
                {$_("All attributes")} (csv)
              </a>
            </li>
          </ul>
        </FilterCollapse>
      {/if}
    </div>
  </nav>

  <button
    class="group absolute right-4 top-2 rounded-full bg-gray-700 p-1 drop-shadow-[3px_3px_1px_rgba(125,125,125,.7)] transition-colors hover:bg-gray-100 hover:drop-shadow-lg"
    on:click={() => (showFilterOverlay = true)}
    type="button"
  >
    <AdjustmentsIcon
      class="h-8 w-8 text-white transition-colors group-hover:text-orange"
    />
  </button>

  <div class="mt-[50px] w-4/5 flex-1 px-6 py-4">
    {#if activeTab?.id === "todo_feedback"}
      <TodoFeedbackView objects={filteredObjects} {model} />
    {:else if activeTab?.id === "requested_feedback"}
      <RequestedFeedbackView objects={filteredObjects} {model} />
    {:else if activeTab?.id === "requested_improvement"}
      <RequestedImprovementView objects={filteredObjects} {model} />
    {:else}
      <Table items={filteredObjects} {columns} {spans} {labels} rowClasses="p-1">
        <DisplayField
          slot="field"
          let:fieldName
          let:obj
          wrapperClasses=""
          valueClasses=""
          fieldname={fieldName}
          value={obj[fieldName]}
          objectVersion={obj.current_draft_id}
          {model}
        />
      </Table>
    {/if}
  </div>
</div>

<FilterOverlay bind:visible={showFilterOverlay} {objects} {model} />
