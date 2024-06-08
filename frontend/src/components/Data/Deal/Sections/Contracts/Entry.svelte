<script lang="ts">
  import EditField from "$components/Fields/EditField.svelte"

  export let entry: Record<string, never>
</script>

<EditField fieldname="contract.number" bind:value={entry.number} showLabel />
<EditField fieldname="contract.date" bind:value={entry.date} showLabel />
<EditField
  fieldname="contract.expiration_date"
  bind:value={entry.expiration_date}
  showLabel
/>
<EditField
  fieldname="contract.agreement_duration"
  bind:value={entry.agreement_duration}
  showLabel
/>
<EditField fieldname="contract.comment" bind:value={entry.comment} showLabel />
