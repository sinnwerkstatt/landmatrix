<script lang="ts">
  import LowLevelNullBooleanField from "$components/Fields/Edit2/LowLevelNullBooleanField.svelte"

  interface Props {
    value: boolean | null
    fieldname: string
    extras?: { nullable: boolean }
  }

  let { value = $bindable(), fieldname, extras }: Props = $props()
</script>

<LowLevelNullBooleanField bind:value {fieldname} nullable={extras?.nullable ?? false} />
