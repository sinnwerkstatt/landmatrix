<script lang="ts">
  import dayjs from "dayjs"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { WorkflowInfo as WFInfo } from "$lib/types/generics"

  export let info: WFInfo
  const status_map = {
    1: "Draft",
    2: "Active", //"Live",
    3: "Active", // "Updated",
    4: "Deleted",
    5: "Rejected", // legacy
    6: "To Delete", // legacy
  }
  const draft_status_map = {
    1: "Draft",
    2: "Review",
    3: "Activation",
    4: "Rejected", // legacy
    5: "Deleted",
  }
  $: confidential_status_change = info.comment?.startsWith("[SET_CONFIDENTIAL]")
    ? "set_confidential"
    : info.comment?.startsWith("[UNSET_CONFIDENTIAL]")
    ? "unset_confidential"
    : false

  $: comment_wo_head = info.comment
    ?.replace("[SET_CONFIDENTIAL]", "")
    .replace("[UNSET_CONFIDENTIAL] ", "")

  $: unread =
    info.to_user?.username === $page.data.user.username &&
    !info.processed_by_receiver &&
    comment_wo_head.length > 0

  async function processInfo() {
    // let res = await this.$apollo.mutate({
    //   mutation: gql`
    //     mutation ($id: Int!, $type: String!) {
    //       toggle_workflow_info_unread(id: $id, type: $type)
    //     }
    //   `,
    //   variables: { id: this.info.id, type: this.info.__typename },
    // });
    // if (res.data.toggle_workflow_info_unread)
    //   // eslint-disable-next-line vue/no-mutating-props
    //   this.info.processed_by_receiver = true;
  }
</script>

<div class="mx-1 mb-2 bg-neutral-200 text-sm shadow-md p-1{unread ? '!font-bold' : ''}">
  <div class="meta">
    <span class="font-semibold">
      {dayjs(info.timestamp).format("YYYY-MM-DD HH:mm")}
    </span>
    <span class="from-to">
      {$_("From")}
      {info.from_user.username}
      {#if info.to_user}
        <span>{$_("to")} {info.to_user.username}</span>
      {/if}
    </span>
  </div>

  {#if info.draft_status_before !== info.draft_status_after}
    <div class="status-change">
      {#if info.draft_status_before}
        <div
          class="status my-1 inline-block bg-pelorous py-1 px-2 leading-4 text-white"
        >
          {draft_status_map[info.draft_status_before]}
        </div>
        →
      {/if}
      <div class="status my-1 inline-block bg-pelorous py-1 px-2 leading-4 text-white">
        {draft_status_map[info.draft_status_after] || status_map[2]}
      </div>
    </div>
  {/if}
  {#if confidential_status_change}
    <div class="status-change">
      <div
        class="status my-1 inline-block bg-pelorous py-1 px-2 leading-4 text-white {confidential_status_change}"
      >
        {$_("Confidential")}
      </div>
    </div>
  {/if}
  {#if comment_wo_head}
    <div class="relative whitespace-pre-line bg-neutral-200 py-1 px-2">
      {comment_wo_head}
      {#if unread}
        <button
          class="absolute top-1 right-4 border-0 bg-inherit opacity-70 transition-opacity	 hover:opacity-100"
          on:click|preventDefault={processInfo}
        >
          <i class="fas fa-check-circle fa-lg orange" />
        </button>
      {/if}
    </div>
  {/if}
</div>

<!--<style scoped lang="scss">-->
<!--  .status-change .status {-->
<!--    padding: 2px 5px 3px;-->
<!--    background-color: darken(#e4e4e4, 8%);-->
<!--    color: #5e5e64;-->
<!--    border-radius: 8px;-->
<!--    filter: drop-shadow(-1px 1px 1px rgba(0, 0, 0, 0.1));-->

<!--    &:last-child {-->
<!--      background-color: #93c7c8;-->
<!--      color: white;-->
<!--    }-->
<!--    &.set_confidential {-->
<!--      background: red;-->
<!--    }-->
<!--    &.unset_confidential {-->
<!--      background: #5dbe00;-->
<!--      text-decoration: line-through;-->
<!--    }-->
<!--  }-->
<!--</style>-->
