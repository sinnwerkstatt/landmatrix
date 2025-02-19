<script lang="ts">
  import LowLevelNullBooleanField from "$components/Fields/Edit2/LowLevelNullBooleanField.svelte"

  interface Props {
    value: boolean | null
    fieldname: string
    extras?: { nullable: boolean }
    onchange?: () => void
  }

  let { value = $bindable(), fieldname, extras, onchange }: Props = $props()
</script>

<LowLevelNullBooleanField
  bind:value
  name={fieldname}
  nullable={extras?.nullable ?? false}
  {onchange}
/>
