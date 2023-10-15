<script lang="ts">
  import LowLevelNullBooleanField from "$components/Fields/Edit/LowLevelNullBooleanField.svelte"

  import type { FormField } from "../fields"

  export let formfield: FormField
  export let value: boolean | null
</script>

<LowLevelNullBooleanField
  bind:value
  nullable={formfield.class === "NullBooleanField"}
  fieldname={formfield.name}
/>
