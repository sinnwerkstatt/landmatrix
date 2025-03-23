<script lang="ts">
  import type { Contract } from "$lib/types/data"
  import type { SubmodelEntry } from "$lib/utils/dataProcessing"

  import DisplayField from "$components/Fields/DisplayField.svelte"

  interface Props {
    entry: SubmodelEntry
  }

  let { entry }: Props = $props()

  const contract = $derived(entry as Contract)
</script>

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
