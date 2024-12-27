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

  async function onsubmit(e: SubmitEvent) {
    e.preventDefault()
    const objType = isDeal(object) ? "dealversions" : "investorversions"
    const ret = await fetch(
      `/api/${objType}/${object.selected_version.id}/change_status/`,
      {
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({ comment, transition: "ACTIVATE" }),
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
      if (isDeal(object)) invalidate("deal:detail").then()
      else invalidate("investor:detail").then()
      open = false
    }
  }
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">{$_("Activate")}</h2>
  <hr />
  <form class="mt-6 text-lg" {onsubmit}>
    <div class="my-6">
      <label>
        <span class="font-semibold">{$_("Additional comment")}</span>
        <!-- svelte-ignore a11y_autofocus -->
        <textarea autofocus bind:value={comment} class="inpt mt-1"></textarea>
      </label>
    </div>

    <div class="mt-14 flex justify-end gap-4">
      <button class="btn-outline" onclick={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="btn btn-primary" type="submit">
        {$_("Submit")}
      </button>
    </div>
  </form>
</Modal>
