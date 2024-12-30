<script lang="ts">
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"

  interface Props {
    value: string | null
    fieldname: string
  }

  let { value = $bindable(), fieldname }: Props = $props()
</script>

<LowLevelDateYearField bind:value name={fieldname} />
