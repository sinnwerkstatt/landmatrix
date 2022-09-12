<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import type { Obj } from "$lib/types/generics"
  import type { User } from "$lib/types/user"

  import ChatBubbleLeftRightIcon from "$components/icons/ChatBubbleLeftRightIcon.svelte"
  import PaperAirplaneSolidIcon from "$components/icons/PaperAirplaneSolidIcon.svelte"
  import ManageOverlay from "$components/Management/ManageOverlay.svelte"

  import ManageHeaderLogbookList from "./ManageHeaderLogbookList.svelte"

  const dispatch = createEventDispatcher()
  export let object: Obj

  let comment = ""

  function addComment(e: Event) {
    const logbookForm = e.target as HTMLFormElement
    if (!logbookForm.checkValidity()) logbookForm.reportValidity()
    dispatch("addComment", { comment })
    comment = ""
  }

  let showFeedbackOverlay = false
  function addFeedback(e: CustomEvent<{ comment: string; toUser: User }>) {
    dispatch("addComment", e.detail)
    comment = ""
    showFeedbackOverlay = false
  }
</script>

<div class="bg-lm-warmgray lg:w-1/3">
  <h3 class="mx-3 mt-2 mb-3">{$_("Logbook")}</h3>
  <form class="relative mx-3" on:submit|preventDefault={addComment}>
    <textarea
      bind:value={comment}
      class="inpt max-h-[4.8rem] min-h-[2.4rem]"
      placeholder={$_("Comment")}
      required
      rows="2"
    />

    <div class="text-right">
      <button
        class="btn btn-pelorous-secondary btn-slim inline-flex items-center gap-2 px-2"
        on:click={() => (showFeedbackOverlay = true)}
        type="button"
      >
        {$_("Feedback")}
        <ChatBubbleLeftRightIcon class="h-5 w-5" />
      </button>
      <button
        class="btn btn-pelorous btn-slim inline-flex items-center gap-2 px-2"
        type="submit"
      >
        {$_("Send")}
        <PaperAirplaneSolidIcon class="h-5 w-5" />
      </button>
    </div>
  </form>

  <ManageHeaderLogbookList workflowinfos={object.workflowinfos} />
</div>

<ManageOverlay
  assignToUserInput
  bind:visible={showFeedbackOverlay}
  {comment}
  commentRequired
  on:submit={addFeedback}
  toUserRequired
/>
