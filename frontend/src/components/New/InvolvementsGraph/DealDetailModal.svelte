<script lang="ts">
  import { _ } from "svelte-i18n"

  import { dealFields } from "$lib/fieldLookups"
  import type { DealHull } from "$lib/types/newtypes"

  import Overlay from "$components/Overlay.svelte"

  export let visible: boolean
  export let deal: DealHull

  const fields = [
    "country_id",
    "intention_of_investment",
    "implementation_status",
    "negotiation_status",
    "intended_size",
    "contract_size",
  ]
  const createTitle = (deal: DealHull) => `${deal.id}`
</script>

<Overlay on:close title={createTitle(deal)} {visible}>
  <div>
    {JSON.stringify(deal)}
    {#each fields as field}
      {@const dealField = $dealFields[field]}
      {#if dealField}
        {#if field === "country_id"}
          <svelte:component
            this={dealField.displayField}
            value={deal[field]}
            wrapperClass=""
            label={dealField.label}
          />
        {:else}
          <svelte:component
            this={dealField.displayField}
            fieldname={field}
            value={deal[field]}
            wrapperClass=""
            label={dealField.label}
            extras={dealField.extras}
          />
        {/if}
      {:else}
        unknown field {field}
      {/if}
    {/each}

    <div class="w-100 mt-8">
      <a class="deal" href="/deal/{deal._id}" rel="noreferrer" target="_blank">
        {$_("More details about this deal")}
      </a>
    </div>
  </div>
</Overlay>
