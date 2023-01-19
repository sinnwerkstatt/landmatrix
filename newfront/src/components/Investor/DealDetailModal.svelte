<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Deal } from "$lib/types/deal"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  import Overlay from "../Overlay.svelte"

  export let visible: boolean
  export let deal: Deal

  const fields = [
    "country",
    "intention_of_investment",
    "implementation_status",
    "negotiation_status",
    "intended_size",
    "contract_size",
  ]
  const createTitle = deal => `${deal.name} (${deal.id})`
</script>

<Overlay on:close title={createTitle(deal)} {visible}>
  <div>
    {#each fields as fieldName}
      <DisplayField
        fieldname={fieldName}
        value={deal[fieldName]}
        model="deal"
        showLabel
      />
    {/each}
    <div class="w-100">
      <a class="deal" href="/deal/{deal.id}" target="_blank">
        {$_("More details about this deal")}
      </a>
    </div>
  </div>
</Overlay>
