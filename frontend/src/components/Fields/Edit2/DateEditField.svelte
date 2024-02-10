<script lang="ts">
  import LowLevelDateYearField from "$components/Fields/Edit2/LowLevelDateYearField.svelte"

  export let value: string | null
  export let fieldname: string
</script>

<LowLevelDateYearField bind:value name={fieldname} />
