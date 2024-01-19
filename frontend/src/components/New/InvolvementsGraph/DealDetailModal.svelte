<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/newtypes"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import Overlay from "$components/Overlay.svelte"

  export let visible: boolean
  export let deal: DealHull

  const fields = [
    "country_id",
    // TODO
    // "intention_of_investment",
    // "implementation_status",
    // "negotiation_status",
    // "intended_size",
    "contract_size",
  ]
  const createTitle = (deal: DealHull) => `${deal.id}`
</script>

<Overlay on:close title={createTitle(deal)} {visible}>
  <div>
    {JSON.stringify(deal)}
    {#each fields as fieldname}
      {#if fieldname === "country_id"}
        <DisplayField {fieldname} value={deal[fieldname]} wrapperClass="" />
      {:else}
        <DisplayField
          {fieldname}
          value={deal.selected_version[fieldname]}
          wrapperClass=""
        />
      {/if}
    {/each}

    <div class="w-100 mt-8">
      <a class="deal" href="/deal/{deal._id}" rel="noreferrer" target="_blank">
        {$_("More details about this deal")}
      </a>
    </div>
  </div>
</Overlay>
