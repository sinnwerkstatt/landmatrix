<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"

  import type { DealHull } from "$lib/types/data"
  import { getCsrfToken } from "$lib/utils"

  import Modal from "$components/Modal.svelte"

  export let object: DealHull
  export let open = false

  let comment = ""

  async function submit() {
    const ret = await fetch(`/api/deals/${object.id}/toggle_confidential/`, {
      method: "PUT",
      credentials: "include",
      body: JSON.stringify({ confidential: !object.confidential, comment }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    if (!ret.ok) {
      const retJson = await ret.json()
      toast.push(`${ret.status}: ${retJson.detail}`, { classes: ["error"] })
    } else {
      invalidate("deal:detail").then()

      open = false
    }
  }
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">
    {object.confidential ? $_("Unset confidential") : $_("Set confidential")}
  </h2>
  <hr />
  <form class="mt-6 text-lg" on:submit={submit}>
    <div class="mb-6">
      <label>
        <span class="font-semibold">
          {$_("Please provide a comment explaining your request")}
        </span>
        <!-- svelte-ignore a11y-autofocus -->
        <textarea autofocus bind:value={comment} class="inpt mt-1" required />
      </label>
    </div>

    <p>
      {#if object.confidential}
        {$_(
          "If you unset the confidential flag, this deal will be publicly visible once it is set active. If you want to keep it confidential, click on 'Cancel'.",
        )}
      {:else}
        {$_(
          "If you set the confidential flag, this deal will not be publicly visible anymore. If you want to keep it public, click on 'Cancel'.",
        )}
      {/if}
    </p>

    <div class="mt-14 flex justify-end gap-4">
      <button class="btn" on:click={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="btn btn-primary" type="submit">
        {$_("Submit")}
      </button>
    </div>
  </form>
</Modal>
