<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"
  import { getCsrfToken } from "$lib/utils"

  import Modal from "$components/Modal.svelte"

  export let object: DealHull | InvestorHull
  export let open = false

  let comment = ""

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  $: objectType = isDeal(object) ? "deal" : "investor"

  $: i18nValues = { values: { object: objectType } }

  async function deleteObject() {
    const objType = isDeal(object) ? "dealversions" : "investorversions"
    const ret = await fetch(`/api/${objType}/${object.selected_version.id}/`, {
      method: "DELETE",
      credentials: "include",
      body: JSON.stringify({ comment }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    if (!ret.ok) {
      const retJson = await ret.json()
      toast.push(`${ret.status}: ${retJson.detail}`, { classes: ["error"] })
    } else {
      if (object.active_version_id)
        await goto(`/${objectType}/${object.id}/`, { invalidateAll: true })
      else await goto(`/list/${objectType}s/`, { invalidateAll: true })
    }
  }
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">{$_("Remove this {object} version?", i18nValues)}</h2>
  <hr />
  <form on:submit={deleteObject}>
    <p class="mb-12 mt-6 text-lg">
      {$_(
        "Completely removes this version of the {object}. This action cannot be undone.",
        i18nValues,
      )}
    </p>
    {#if object.active_version_id}
      <div class="mb-6">
        <label>
          <span class="font-semibold">
            {$_("Please provide a comment explaining your request")}
          </span>
          <textarea bind:value={comment} class="inpt mt-1" required />
        </label>
      </div>
    {/if}
    <div class="flex justify-end gap-4">
      <button
        autofocus
        class="btn-outline"
        on:click={() => (open = false)}
        type="button"
      >
        {$_("Cancel")}
      </button>
      <button class="btn btn-red" type="submit">
        {$_("Remove")}
      </button>
    </div>
  </form>
</Modal>
