<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"

  import type { DealHull, InvestorHull } from "$lib/types/newtypes.js"
  import { getCsrfToken } from "$lib/utils"

  import Modal from "$components/Modal.svelte"

  export let object: DealHull | InvestorHull
  export let open = false

  let fullyUpdated = false
  let comment = ""
  let dataPolicyChecked = false

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  async function submitToReview() {
    const objType = isDeal(object) ? "dealversions" : "investors"
    const ret = await fetch(
      `/api/${objType}/${object.selected_version.id}/change_status/`,
      {
        method: "PUT",
        credentials: "include",
        body: JSON.stringify({ comment, fullyUpdated, transition: "TO_REVIEW" }),
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
      open = false
    }
  }
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">
    {$_("Submit for review")}
  </h2>
  <hr />
  <form on:submit={submitToReview} class="mt-6 text-lg">
    <div>
      <div class="mb-2 font-semibold">Fully updated</div>
      <p>
        {$_(
          'If you have checked the information entered for every single variable, please tick the box beside "I fully updated this deal" - even if no additional information was found, but a complete search through the deal was conducted.',
        )}
      </p>
      <label>
        <input bind:checked={fullyUpdated} type="checkbox" />
        {$_("I fully updated this deal.")}
      </label>
    </div>

    <div class="my-6">
      <label>
        <span class="font-semibold">{$_("Additional comment")}</span>
        <textarea autofocus bind:value={comment} class="inpt mt-1" />
      </label>
    </div>

    <label class="mt-1 font-bold">
      <input
        id="data-policy-checkbox"
        required
        bind:checked={dataPolicyChecked}
        type="checkbox"
      />
      {$_("I've read and agree to the")}
      <a href="/about/data-policy/" target="_blank">{$_("Data policy")}</a>
      .
    </label>

    <div class="mt-14 flex justify-end gap-4">
      <button class="butn-outline" on:click={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="butn butn-primary" type="submit" disabled={!dataPolicyChecked}>
        {$_("Submit")}
      </button>
    </div>
  </form>
</Modal>
