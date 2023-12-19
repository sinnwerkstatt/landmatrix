<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes"
  import { UserRole } from "$lib/types/user"

  import ChatBubbleLeftIcon from "$components/icons/ChatBubbleLeftIcon.svelte"
  import ChatBubbleLeftRightIcon from "$components/icons/ChatBubbleLeftRightIcon.svelte"
  import ManageFeedbackCommentModal from "$components/New/ManageFeedbackCommentModal.svelte"
  import WorkflowInfoNew from "$components/New/WorkflowInfoNew.svelte"

  export let object: DealHull | InvestorHull
  export let extraUserIDs: number[] = []

  let showCommentOverlay = false
  let showFeedbackOverlay = false
</script>

<div
  class="col-span-2 flex flex-col rounded-tr bg-gray-100 px-3 dark:bg-gray-700 lg:col-span-1"
>
  <h3 class="my-1 ml-1 font-medium">{$_("Logbook")}</h3>

  <div
    class="h-0 flex-grow cursor-default overflow-y-scroll border-gray-700 px-[2px] pb-4 pt-1 shadow-inner"
  >
    {#each object.workflowinfos as info}
      <WorkflowInfoNew {info} />
    {/each}
  </div>

  <div class="my-2 text-right">
    {#if $page.data.user.role > UserRole.REPORTER}
      <button
        class="butn butn-violet butn-flat inline-flex items-center gap-2 px-2"
        on:click={() => (showFeedbackOverlay = true)}
        type="button"
      >
        {$_("Send feedback")}
        <ChatBubbleLeftRightIcon class="h-5 w-5" />
      </button>
    {/if}
    <button
      class="butn butn-purple butn-flat inline-flex items-center gap-2 px-2"
      on:click={() => (showCommentOverlay = true)}
      type="submit"
    >
      {$_("Add comment")}
      <ChatBubbleLeftIcon class="h-5 w-5" />
    </button>
  </div>
</div>

<ManageFeedbackCommentModal bind:open={showFeedbackOverlay} feedbackForm {object} />
<ManageFeedbackCommentModal bind:open={showCommentOverlay} {object} />
