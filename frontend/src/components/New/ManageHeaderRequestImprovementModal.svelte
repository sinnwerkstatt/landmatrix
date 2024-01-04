<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"
  import { UserRole, type User } from "$lib/types/user"
  import { getCsrfToken } from "$lib/utils"

  import UserSelect from "$components/LowLevel/UserSelect.svelte"
  import Modal from "$components/Modal.svelte"

  export let object: DealHull | InvestorHull
  export let open = false

  let comment = ""
  let toUser: User | number | null = null

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  onMount(() => {
    toUser = object.selected_version.created_by_id
  })
  onDestroy(() => (comment = ""))

  async function submit() {
    const objType = isDeal(object) ? "dealversions" : "investorversions"
    const ret = await fetch(
      `/api/${objType}/${object.selected_version.id}/change_status/`,
      {
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({
          comment,
          toUser: toUser?.id,
          transition: "TO_DRAFT",
        }),
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
      const retJson = await ret.json()
      await goto(`/deal/${retJson.dealID}/${retJson.versionID}/`, {
        invalidateAll: true,
      })

      open = false
    }
  }
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">
    {$_("Request improvement")}
  </h2>
  <hr />
  <form class="mt-6 text-lg" on:submit={submit}>
    <div class="mb-6">
      <label>
        <span class="font-semibold">
          {$_("Please provide a comment explaining your request")}
        </span>
        <textarea bind:value={comment} class="inpt mt-1" required />
      </label>
    </div>
    <div class="mb-6">
      <label for="">
        <span class="font-semibold">
          {$_("Assign to user")}
        </span>
        <UserSelect bind:value={toUser} minimumRole={UserRole.EDITOR} required />
      </label>
    </div>
    <div class="mt-14 flex justify-end gap-4">
      <button class="butn-outline" on:click={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="butn butn-primary" type="submit">
        {$_("Submit")}
      </button>
    </div>
  </form>
</Modal>
