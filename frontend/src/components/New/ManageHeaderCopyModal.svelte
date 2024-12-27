<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"

  import type { DealHull } from "$lib/types/data"
  import { getCsrfToken } from "$lib/utils"

  import Modal from "$components/Modal.svelte"

  interface Props {
    object: DealHull
    open: boolean
  }

  let { object, open = $bindable() }: Props = $props()

  async function onsubmit(e: SubmitEvent) {
    e.preventDefault()
    const ret = await fetch(`/api/deals/${object.id}/make_copy/`, {
      method: "PUT",
      credentials: "include",
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    const retJson = await ret.json()
    if (!ret.ok) {
      toast.push(`${ret.status}: ${retJson.detail}`, { classes: ["error"] })
    } else {
      await goto(`/deal/${retJson.dealID}/${retJson.versionID}/`)
      open = false
    }
  }
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">
    {$_("Copy deal")}
  </h2>
  <hr />
  <form class="mt-6 text-lg" {onsubmit}>
    <p>
      {$_(
        "This creates a completely identical copy of the deal. The copy must then be edited and adjusted to prevent identical duplicates.",
      )}
    </p>
    <div class="font-medium">{$_("Do you really want to copy this deal?")}</div>

    <div class="mt-14 flex justify-end gap-4">
      <button class="btn" onclick={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="btn btn-primary" type="submit">
        {$_("Copy deal")}
      </button>
    </div>
  </form>
</Modal>
