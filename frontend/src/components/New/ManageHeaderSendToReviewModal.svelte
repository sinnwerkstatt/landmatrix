<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { invalidate } from "$app/navigation"

  import type { DealHull, InvestorHull } from "$lib/types/data.js"
  import { getCsrfToken } from "$lib/utils"

  import Modal from "$components/Modal.svelte"

  export let object: DealHull | InvestorHull
  export let open = false

  let fullyUpdated = false
  let comment = ""
  let dataPolicyChecked = false

  const isDeal = (obj: DealHull | InvestorHull): obj is DealHull =>
    "fully_updated_at" in obj

  async function submit() {
    const objType = isDeal(object) ? "dealversions" : "investorversions"
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
      if (isDeal(object)) invalidate("deal:detail").then()
      else invalidate("investor:detail").then()
      open = false
    }
  }
</script>

<Modal bind:open dismissible>
  <h2 class="heading4">{$_("Submit for review")}</h2>
  <hr />
  <form class="mt-6 text-lg" on:submit={submit}>
    {#if isDeal(object)}
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
    {/if}

    <div class="my-6">
      <label>
        <span class="font-semibold">{$_("Additional comment")}</span>
        <textarea bind:value={comment} class="inpt mt-1" />
      </label>
    </div>

    <label class="mt-1 font-bold">
      <input
        bind:checked={dataPolicyChecked}
        id="data-policy-checkbox"
        required
        type="checkbox"
      />
      {$_("I've read and agree to the")}
      <a href="/about/data-policy/" target="_blank">{$_("Data policy")}</a>
      .
    </label>

    <div class="mt-14 flex justify-end gap-4">
      <button class="btn-outline" on:click={() => (open = false)} type="button">
        {$_("Cancel")}
      </button>
      <button class="btn btn-primary" disabled={!dataPolicyChecked} type="submit">
        {$_("Submit")}
      </button>
    </div>
  </form>
</Modal>
