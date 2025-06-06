<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"

  import { UserRole, type DealHull, type InvestorHull } from "$lib/types/data"
  import { getCsrfToken } from "$lib/utils"

  import UserSelect from "$components/LowLevel/UserSelect.svelte"
  import Modal from "$components/Modal.svelte"

  interface Props {
    object: DealHull | InvestorHull
    open: boolean
    feedbackForm?: boolean
  }

  let { object, open = $bindable(), feedbackForm = false }: Props = $props()

  let comment = $state("")
  let toUser: number | null = $state(object.selected_version.created_by_id)

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  async function onsubmit(e: SubmitEvent) {
    e.preventDefault()
    const objType = isDeal(object) ? "deals" : "investors"
    const ret = await fetch(`/api/${objType}/${object.id}/add_comment/`, {
      method: "PUT",
      credentials: "include",
      body: JSON.stringify({
        comment,
        toUser: toUser,
        version: object.selected_version.id,
      }),
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
      open = false
    }
  }

  let title = $derived(feedbackForm ? $_("Send feedback") : $_("Add comment"))
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">
    {title}
  </h2>
  <hr />
  <form class="mt-6 text-lg" {onsubmit}>
    <div class="mb-6">
      <label>
        <span class="font-semibold">
          {$_("Please provide a comment explaining your request")}
        </span>
        <textarea bind:value={comment} class="inpt mt-1" required></textarea>
      </label>
    </div>
    {#if feedbackForm}
      <div class="mb-6">
        <label for="">
          <span class="font-semibold">
            {$_("Assign to user")}
          </span>
          <UserSelect bind:value={toUser} minimumRole={UserRole.EDITOR} required />
        </label>
      </div>
    {/if}

    <div class="mt-14 flex justify-end gap-4">
      <button class="btn-outline" onclick={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="btn {feedbackForm ? 'btn-violet' : 'btn-purple'}" type="submit">
        {title}
      </button>
    </div>
  </form>
</Modal>
