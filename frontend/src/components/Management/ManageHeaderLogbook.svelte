<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { User } from "$lib/types/user"
  import { UserRole } from "$lib/types/user"

  import ChatBubbleLeftIcon from "$components/icons/ChatBubbleLeftIcon.svelte"
  import ChatBubbleLeftRightIcon from "$components/icons/ChatBubbleLeftRightIcon.svelte"
  import ManageOverlay from "$components/Management/ManageOverlay.svelte"
  import WorkflowInfo from "$components/Management/WorkflowInfo.svelte"

  export let workflowInfos: WorkflowInfo[] = []
  export let extraUserIDs: number[] = []

  const dispatch = createEventDispatcher()

  let showCommentOverlay = false
  let commentOverlayComment = ""

  function addComment(e: CustomEvent<{ comment: string; toUser: User }>) {
    dispatch("addComment", { comment: e.detail.comment })
    commentOverlayComment = ""
    showCommentOverlay = false
  }

  let showFeedbackOverlay = false
  let feedbackOverlayComment = ""

  function addFeedback(e: CustomEvent<{ comment: string; toUser: User }>) {
    dispatch("addComment", e.detail)
    feedbackOverlayComment = ""
    showFeedbackOverlay = false
  }
</script>

<div class="flex flex-col bg-lm-darkgray px-3 dark:bg-gray-700 lg:w-1/3">
  <h3 class="my-1 font-medium">{$_("Logbook")}</h3>

  <div
    class="h-0 flex-grow cursor-default overflow-y-scroll border-lm-dark px-[2px] pt-1 pb-4 shadow-inner"
  >
    {#each workflowInfos as info}
      <WorkflowInfo {info} />
    {/each}
  </div>

  <div class="my-2 text-right">
    {#if $page.data.user.role > UserRole.REPORTER}
      <button
        class="btn btn-pelorous-secondary btn-slim inline-flex items-center gap-2 px-2"
        on:click={() => (showFeedbackOverlay = true)}
        type="button"
      >
        {$_("Send feedback")}
        <ChatBubbleLeftRightIcon class="h-5 w-5" />
      </button>
    {/if}
    <button
      class="btn btn-pelorous btn-slim inline-flex items-center gap-2 px-2"
      on:click={() => (showCommentOverlay = true)}
      type="submit"
    >
      {$_("Add comment")}
      <ChatBubbleLeftIcon class="h-5 w-5" />
    </button>
  </div>
</div>

{#if showFeedbackOverlay}
  <ManageOverlay
    assignToUserInput
    bind:comment={feedbackOverlayComment}
    bind:visible={showFeedbackOverlay}
    commentRequired
    on:submit={addFeedback}
    title={$_("Send feedback")}
    submitTitle={$_("Send")}
    {extraUserIDs}
    toUserRequired
  />
{/if}

{#if showCommentOverlay}
  <ManageOverlay
    bind:comment={commentOverlayComment}
    bind:visible={showCommentOverlay}
    commentRequired
    on:submit={addComment}
    submitTitle={$_("Save")}
    title={$_("Add comment")}
  />
{/if}
