<script lang="ts">
  import { _ } from "svelte-i18n";
  import { user } from "$lib/stores";
  import FilterCollapse from "$components/Data/FilterCollapse.svelte";

  $: xTabs = [
    {
      name: "Todo",
      initExpanded: true,
      items: [
        {
          name: "Feedback for me",
          id: "todo_clarification",
          filters: [
            { field: "workflowinfos.draft_status_before", value: null },
            { field: "workflowinfos.draft_status_after", value: null },
            { field: "workflowinfos.to_user_id", value: $user.id },
          ],
        },
        {
          name: "Improvement requests for me",
          id: "todo_improve",
          filters: [
            { field: "draft_status", value: 1 },
            { field: "workflowinfos.draft_status_before", value: 2 },
            { field: "workflowinfos.draft_status_after", value: 1 },
            { field: "workflowinfos.to_user_id", value: $user.id },
          ],
        },
        {
          name: "Review",
          id: "todo_review",
          staff: true,
          filters: [{ field: "draft_status", value: 2 }],
        },
        {
          name: "Activation",
          id: "todo_activation",
          staff: true,
          filters: [{ field: "draft_status", value: 3 }],
        },
      ],
    },
    {
      name: "My requests",
      items: [
        {
          name: "Feedback by me",
          id: "requested_feedback",
          filters: [
            { field: "workflowinfos.draft_status_before", value: null },
            { field: "workflowinfos.draft_status_after", value: null },
            { field: "workflowinfos.from_user_id", value: $user.id },
          ],
        },
        {
          name: "Improvements requested by me",
          id: "requested_improvement",
          staff: true,
          filters: [
            { field: "workflowinfos.draft_status_before", value: 2 },
            { field: "workflowinfos.draft_status_after", value: 1 },
            { field: "workflowinfos.from_user_id", value: $user.id },
          ],
        },
      ],
    },
    {
      name: "My data",
      items: [
        {
          name: "My drafts",
          id: "my_drafts",
          filters: [
            { field: "draft_status", value: 1 },
            {
              field: "current_draft.created_by_id",
              value: $user.id,
            },
          ],
        },
        {
          name: "Created by me",
          id: "created_by_me",
          filters: [{ field: "created_by_id", value: $user.id }],
        },
        {
          name: "Reviewed by me",
          id: "reviewed_by_me",
          staff: true,
          filters: [
            { field: "workflowinfos.draft_status_before", value: 2 },
            { field: "workflowinfos.draft_status_after", value: 3 },
            { field: "workflowinfos.from_user_id", value: $user.id },
          ],
        },
        {
          name: "Activated by me",
          id: "activated_by_me",
          staff: true,
          filters: [
            { field: "workflowinfos.draft_status_before", value: 3 },
            { field: "workflowinfos.from_user_id", value: $user.id },
          ],
        },
      ],
    },
    {
      name: "Data overview",
      items: [
        {
          name: "All deals",
          id: "all_items",
          staff: true,
          filters: [],
        },
        {
          name: "All deleted",
          id: "all_deleted",
          staff: true,
          filters: [{ field: "status", value: 4 }],
        },
        {
          name: "All non active",
          id: "all_drafts",
          staff: true,
          filters: [{ field: "current_draft", exclusion: true, value: null }],
        },
      ],
    },
  ];

  let activeTab;
</script>

<div class="flex min-h-full">
  <nav class="p-2 flex-initial">
    {#each xTabs as { name, items, initExpanded }}
      <FilterCollapse title={$_(name)} {initExpanded}>
        <ul>
          {#each items as { id, name }}
            <li
              class="py-2 pr-4 border-orange {activeTab === id
                ? 'border-r-4'
                : 'border-r'}"
            >
              {#if name}
                <a href="#{id}" class:text-black={activeTab === id}>{name}</a>
              {:else}
                <hr />
              {/if}
            </li>
          {/each}
        </ul>
      </FilterCollapse>
    {/each}
  </nav>
  <div>asdfasdfasdfa</div>
</div>
