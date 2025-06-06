<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { type DealHull, type InvestorHull } from "$lib/types/data"
  import { isReporterOrAbove } from "$lib/utils/permissions"

  import ChatBubbleLeftIcon from "$components/icons/ChatBubbleLeftIcon.svelte"
  import ChatBubbleLeftRightIcon from "$components/icons/ChatBubbleLeftRightIcon.svelte"
  import ManageFeedbackCommentModal from "$components/New/ManageFeedbackCommentModal.svelte"
  import WorkflowInfoNew from "$components/New/WorkflowInfoNew.svelte"

  interface Props {
    object: DealHull | InvestorHull
  }

  let { object }: Props = $props()

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  let showCommentOverlay = $state(false)
  let showFeedbackOverlay = $state(false)
</script>

<div
  class="col-span-2 flex flex-col rounded-tr bg-gray-100 px-3 lg:col-span-1 dark:bg-gray-700"
>
  <h3 class="mb-2 ml-1 mt-3 font-medium">{$_("Logbook")}</h3>

  <div
    class="max-h-[300px] flex-grow cursor-default overflow-y-scroll border-gray-700 px-[2px] pb-4 pt-1 shadow-inner lg:h-0"
  >
    {#each object.workflowinfos as info}
      <WorkflowInfoNew {info} isDeal={isDeal(object)} />
    {/each}
  </div>

  <div class="my-2 text-right">
    {#if isReporterOrAbove(page.data.user)}
      <button
        class="btn btn-violet btn-flat inline-flex items-center gap-2 px-2"
        onclick={() => (showFeedbackOverlay = true)}
        type="button"
      >
        {$_("Send feedback")}
        <ChatBubbleLeftRightIcon class="h-5 w-5" />
      </button>
    {/if}
    <button
      class="btn btn-purple btn-flat inline-flex items-center gap-2 px-2"
      onclick={() => (showCommentOverlay = true)}
      type="button"
    >
      {$_("Add comment")}
      <ChatBubbleLeftIcon class="h-5 w-5" />
    </button>
  </div>
</div>

<ManageFeedbackCommentModal bind:open={showFeedbackOverlay} feedbackForm {object} />
<ManageFeedbackCommentModal bind:open={showCommentOverlay} {object} />
