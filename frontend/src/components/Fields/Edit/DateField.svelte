<script lang="ts">
  import type { FormField } from "../fields"
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte"

  export let formfield: FormField
  export let value
</script>

<LowLevelDateYearField bind:value name={formfield.name} />
