<script lang="ts">
  import EditField from "$components/Fields/EditField.svelte"

  interface Props {
    entry: Record<string, never>
    onchange?: () => void
  }

  let { entry = $bindable(), onchange }: Props = $props()
</script>

<EditField fieldname="contract.number" bind:value={entry.number} showLabel {onchange} />
<EditField fieldname="contract.date" bind:value={entry.date} showLabel {onchange} />
<EditField
  fieldname="contract.expiration_date"
  bind:value={entry.expiration_date}
  showLabel
  {onchange}
/>
<EditField
  fieldname="contract.agreement_duration"
  bind:value={entry.agreement_duration}
  showLabel
  {onchange}
/>
<EditField
  fieldname="contract.comment"
  bind:value={entry.comment}
  showLabel
  {onchange}
/>
