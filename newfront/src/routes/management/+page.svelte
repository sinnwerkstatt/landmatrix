<script lang="ts">
  import cn from "classnames";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { formfields, loading } from "$lib/stores";
  import type { Deal } from "$lib/types/deal";
  import { UserLevel } from "$lib/types/user";
  import FilterCollapse from "$components/Data/FilterCollapse.svelte";
  import DisplayField from "$components/Fields/DisplayField.svelte";
  import DownloadIcon from "$components/icons/DownloadIcon.svelte";
  import Table from "$components/table/Table.svelte";
  import RequestedImprovementView from "./RequestedImprovementView.svelte";
  import TodoFeedbackView from "./TodoFeedbackView.svelte";

  interface Tab {
    id: string;
    name: string;
    staff?: boolean;
    count?: number;
  }

  const user = $page.data.user;

  let model: "deal" | "investor" = "deal";
  let activeTab;
  let deals: Deal[] = [];

  let navTabs: { name: string; expanded?: boolean; items: Tab[] }[];
  $: navTabs = [
    {
      name: "Todo",
      items: [
        { id: "todo_feedback", name: "Feedback for me" },
        { id: "todo_improvement", name: "Improvement requests for me" },
        { id: "todo_review", name: "Review", staff: true },
        { id: "todo_activation", name: "Activation", staff: true },
      ],
    },
    {
      name: "My requests",
      items: [
        { id: "requested_feedback", name: "Feedback by me" },
        {
          id: "requested_improvement",
          name: "Improvements requested by me",
          staff: true,
        },
      ],
    },
    {
      name: "My data",
      items: [
        { id: "my_drafts", name: "My drafts" },
        { id: "created_by_me", name: "Created by me" },
        { id: "reviewed_by_me", name: "Reviewed by me", staff: true },
        { id: "activated_by_me", name: "Activated by me", staff: true },
      ],
    },
    {
      name: "Data overview",
      items: [
        { id: "all_items", name: "All deals", staff: true },
        { id: "all_drafts", name: "All non active", staff: true },
        { id: "all_deleted", name: "All deleted", staff: true },
      ],
    },
  ];

  const selectTab = (tab: Tab) => {
    goto("#" + tab.id);
    activeTab = tab;
  };

  $: tableHeaders =
    model === "deal"
      ? [
          "id",
          "country",
          "deal_size",
          "created_at",
          "created_by",
          // "modified_at",
          // "modified_by",
          // "fully_updated_at",
          "workflowinfos",
          // "combined_status",
        ]
      : [
          "id",
          "name",
          "country",
          "created_at",
          "current_draft.modified_at",
          "workflowinfos",
          "combined_status",
          "deals",
        ];

  const allColumnsWithSpan = {
    id: 1,
    name: 3,
    country: 3,
    deal_size: 2,
    created_at: 2,
    created_by: 3,
    fully_updated_at: 2,
    workflowinfos: 5,
    combined_status: 2,
  };
  $: labels = tableHeaders.map((col) => $formfields.deal[col].label);
  $: spans = Object.entries(allColumnsWithSpan)
    .filter(([col, _]) => tableHeaders.includes(col))
    .map(([_, colSpan]) => colSpan);

  let controller: AbortController;

  async function fetchDeals(acTab: Tab) {
    if (!acTab) return;
    if (controller) controller.abort();

    loading.set(true);
    controller = new AbortController();
    const x = await fetch(`/api/management?action=${acTab.id}`, {
      signal: controller.signal,
    });
    if (x.ok) {
      deals = (await x.json()).deals;
      acTab.count = deals.length;
      navTabs = navTabs;
    }

    loading.set(false);
  }

  $: fetchDeals(activeTab);

  async function getCounts() {
    const x = await fetch(`/api/management?action=counts`);
    if (x.ok) {
      const counts = await x.json();
      console.log(counts);
      navTabs.forEach((navTab) =>
        navTab.items.forEach((i) => {
          if (counts?.[i.id]) i.count = counts[i.id];
        })
      );
      navTabs = navTabs;
    }
  }

  onMount(() => {
    getCounts();

    navTabs.some((navTab) => {
      const hash = $page.url.hash || "#todo_feedback";
      console.log(hash);
      const item = navTab.items.find((i) => "#" + i.id === hash);
      if (item) {
        selectTab(item);
        return true;
      }
    });
  });

  function trackDownload(format) {
    // TODO implement this? ${format}
  }
</script>

<svelte:head>
  <title>{$_("Management | Land Matrix")}</title>
</svelte:head>

<div class="flex min-h-full w-full">
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
        type="button"
        on:click={() => (model = "deal")}
      >
        {$_("Deals")}
      </button>
      <button
        class={model === "investor"
          ? "border-b border-solid border-black text-black"
          : "text-gray-500 hover:text-gray-600"}
        type="button"
        on:click={() => (model = "investor")}
      >
        {$_("Investors")}
      </button>
    </div>
    <div class="w-full self-start">
      {#each navTabs as { name, items }}
        {@const aggCount = items.map((i) => i.count ?? 0).reduce((a, b) => a + b, 0)}
        {#if user.level > UserLevel.EDITOR || !items.every((i) => i.staff)}
          <FilterCollapse
            title="{$_(name)} (Σ {aggCount})"
            expanded={items.some((i) => i.count > 0)}
          >
            <ul>
              {#each items.filter((i) => user.level > UserLevel.EDITOR || !i.staff) as item}
                <li
                  class={cn(
                    "py-2 pr-4",
                    model === "deal" ? "border-orange" : "border-pelorous",
                    activeTab === item ? "border-r-4" : "border-r"
                  )}
                >
                  <button
                    class={activeTab === item
                      ? model === "deal"
                        ? "text-orange"
                        : "text-pelorous"
                      : "text-gray-600"}
                    class:text-black={activeTab === item}
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
                {$_("All attributes (xlsx)")}
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
                {$_("All attributes (csv)")}
              </a>
            </li>
          </ul>
        </FilterCollapse>
      {/if}
    </div>
  </nav>

  <div class="px-6 py-4">
    {#if activeTab?.id === "todo_feedback"}
      <TodoFeedbackView {deals} />
    {:else if activeTab?.id === "requested_improvement"}
      <RequestedImprovementView {deals} />
    {:else}
      <Table
        items={deals}
        columns={tableHeaders}
        {spans}
        {labels}
        rowClasses="flex items-center"
      >
        <DisplayField
          slot="field"
          let:fieldName
          let:obj
          wrapperClasses="p-1"
          valueClasses=""
          fieldname={fieldName}
          value={obj[fieldName]}
          objectVersion={obj.draft_id}
        />
      </Table>
    {/if}
  </div>
</div>
