<script lang="ts">
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"

  interface Props {
    value: string | null
    fieldname: string
    onchange?: () => void
  }

  let { value = $bindable(), fieldname, onchange }: Props = $props()
</script>

<LowLevelDateYearField bind:value name={fieldname} {onchange} />
