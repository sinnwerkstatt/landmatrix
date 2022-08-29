<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"

  import type { Obj } from "$lib/types/generics"
  import type { User } from "$lib/types/user"

  import UserSelect from "$components/Management/UserSelect.svelte"

  import ManageHeaderLogbookList from "./ManageHeaderLogbookList.svelte"

  const dispatch = createEventDispatcher()
  export let object: Obj

  let comment = ""
  let sendToUser: User
  let logbookForm

  function addComment() {
    if (!logbookForm.checkValidity()) {
      logbookForm.reportValidity()
      return
    }

    dispatch("addComment", { comment, sendToUser })
    comment = ""
  }
</script>

<div class="bg-lm-warmgray lg:w-1/3">
  <h3 class="mx-3">{$_("Logbook")}</h3>
  <form bind:this={logbookForm} class="mx-1">
    <textarea bind:value={comment} required rows="2" class="w-full" />

    <div class="my-2 ml-1 items-center lg:flex">
      <span class="lg:w-1/5">{$_("Send to")}:</span>
      <div class="flex-grow">
        <UserSelect bind:value={sendToUser} />
      </div>
      <button
        type="button"
        class="btn btn-pelorous btn-slim lg:w-1/5"
        on:click|preventDefault={addComment}
      >
        {$_("Send")}
      </button>
    </div>
  </form>

  <ManageHeaderLogbookList workflowinfos={object.workflowinfos} />
</div>
