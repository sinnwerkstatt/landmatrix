<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { MutableDealHull } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import { createContract, isEmptyContract } from "./contracts"
  import Entry from "./Entry.svelte"

  interface Props {
    deal: MutableDealHull
  }

  let { deal = $bindable() }: Props = $props()

  let contracts = $state(deal.selected_version.contracts)

  const onchange = () => {
    deal.selected_version.contracts = contracts
  }
</script>

<SubmodelEditField
  model="deal"
  fieldname="contracts"
  label={$_("Contract")}
  bind:entries={contracts}
  createEntry={createContract}
  isEmpty={isEmptyContract}
  entryComponent={Entry}
  {onchange}
/>
