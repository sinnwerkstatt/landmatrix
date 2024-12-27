<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"

  import type { DealHull, InvestorHull } from "$lib/types/data"
  import { getCsrfToken } from "$lib/utils"

  import Modal from "$components/Modal.svelte"

  interface Props {
    object: DealHull | InvestorHull
    open: boolean
  }

  let { object, open = $bindable() }: Props = $props()

  let comment = $state("")

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  let objectType = $derived(isDeal(object) ? "deal" : "investor")

  let i18nValues = $derived({ values: { object: objectType } })

  async function onsubmit(e: SubmitEvent) {
    e.preventDefault()

    const ret = await fetch(`/api/${objectType}s/${object.id}/toggle_deleted/`, {
      method: "PUT",
      credentials: "include",
      body: JSON.stringify({ deleted: !object.deleted, comment }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    if (!ret.ok) {
      const retJson = await ret.json()
      toast.push(`${ret.status}: ${retJson.detail}`, { classes: ["error"] })
    } else {
      if (isDeal(object)) invalidate("deal:detail").then()
      else invalidate("investor:detail").then()
      comment = ""
      open = false
    }
  }
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">
    {object.deleted
      ? $_("Reactivate {object}", i18nValues)
      : $_("Delete {object}", i18nValues)}
  </h2>
  <hr />
  <form class="mt-6 text-lg" {onsubmit}>
    <div class="mb-6">
      <label>
        <span class="font-semibold">
          {$_("Please provide a comment explaining your request")}
        </span>
        <!-- svelte-ignore a11y_autofocus -->
        <textarea autofocus bind:value={comment} class="inpt mt-1" required></textarea>
      </label>
    </div>

    <div class="mt-14 flex justify-end gap-4">
      <button class="btn" onclick={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="btn btn-primary" type="submit">
        {$_("Submit")}
      </button>
    </div>
  </form>
</Modal>
