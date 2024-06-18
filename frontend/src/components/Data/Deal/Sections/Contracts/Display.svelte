<script lang="ts">
  import { _ } from "svelte-i18n"

  import type { DealHull } from "$lib/types/data"

  import DisplayField from "$components/Fields/DisplayField.svelte"
  import SubmodelDisplayField from "$components/Fields/SubmodelDisplayField.svelte"

  export let deal: DealHull

  $: label = $_("Contract")
</script>

<SubmodelDisplayField
  entries={deal.selected_version.contracts}
  {label}
  let:entry={contract}
>
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
</SubmodelDisplayField>
