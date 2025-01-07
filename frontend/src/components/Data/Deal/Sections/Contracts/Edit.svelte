<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/data"

  import SubmodelEditField from "$components/Fields/SubmodelEditField.svelte"

  import { createContract, isEmptyContract } from "./contracts"
  import Entry from "./Entry.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal = $bindable() }: Props = $props()

  let contracts = $state(deal.selected_version.contracts)

  const onchange = () => {
    deal.selected_version.contracts = contracts
  }
</script>

<SubmodelEditField
  label={$_("Contract")}
  bind:entries={contracts}
  createEntry={createContract}
  isEmpty={isEmptyContract}
  entryComponent={Entry}
  {onchange}
/>
