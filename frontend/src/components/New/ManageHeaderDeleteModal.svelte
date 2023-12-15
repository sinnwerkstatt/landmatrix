<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"
  import { getCsrfToken } from "$lib/utils"

  import Modal from "$components/Modal.svelte"

  export let object: DealHull | InvestorHull
  export let showDeleteOverlay = false

  let modalComment = ""

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  $: i18nValues = { values: { object: isDeal(object) ? "deal" : "investor" } }

  async function deleteDeal() {
    const objType = isDeal(object) ? "deals" : "investors"
    const ret = await fetch(
      `/api/${objType}/${object.id}/${object.selected_version.id}/`,
      {
        method: "DELETE",
        credentials: "include",
        body: JSON.stringify({ comment: modalComment }),
        headers: {
          "X-CSRFToken": await getCsrfToken(),
          "Content-Type": "application/json",
        },
      },
    )
    if (!ret.ok) {
      const retJson = await ret.json()
      toast.push(`${ret.status}: ${retJson.detail}`, { classes: ["error"] })
    } else {
      await goto(`/deal/${object.id}/`, { invalidateAll: true })
    }
  }
</script>

<Modal bind:open={showDeleteOverlay} dismissible>
  <h2 class="heading4">
    {$_("Remove this {object} version?", i18nValues)}
  </h2>
  <hr />
  <form on:submit={deleteDeal}>
    <p class="mb-12 mt-6 text-lg">
      {$_(
        "Completely removes this version of the {object}. This action cannot be undone.",
        i18nValues,
      )}
    </p>
    <p>
      <label class="mb-6 block underline">
        {$_("Please provide a comment explaining your request")}
        <textarea bind:value={modalComment} class="inpt mt-1" required />
      </label>
    </p>
    <div class="flex justify-end gap-4">
      <button
        autofocus
        class="butn-outline"
        on:click={() => (showDeleteOverlay = false)}
        type="button"
      >
        {$_("Cancel")}
      </button>
      <button class="butn butn-red" type="submit">
        {$_("Remove")}
      </button>
    </div>
  </form>
</Modal>
