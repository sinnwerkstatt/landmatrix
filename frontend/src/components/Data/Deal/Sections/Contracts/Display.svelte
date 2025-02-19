<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { Contract, DealHull } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SubmodelDisplayField from "$components/Fields/SubmodelDisplayField.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal }: Props = $props()

  let label = $derived($_("Contract"))
</script>

<SubmodelDisplayField entries={deal.selected_version.contracts} {label}>
  {#snippet children(contract: Contract)}
    <DisplayField fieldname="contract.number" showLabel value={contract.number} />
    <DisplayField fieldname="contract.date" showLabel value={contract.date} />
    <DisplayField
      fieldname="contract.expiration_date"
      showLabel
      value={contract.expiration_date}
    />
    <DisplayField
      fieldname="contract.agreement_duration"
      showLabel
      value={contract.agreement_duration}
    />
    <DisplayField fieldname="contract.comment" showLabel value={contract.comment} />
  {/snippet}
</SubmodelDisplayField>
