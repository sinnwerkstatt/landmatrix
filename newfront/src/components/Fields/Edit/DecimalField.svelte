<script lang="ts">
  import type { FormField } from "../fields";
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte";

  export let formfield: FormField;
  export let value: number;
</script>

<div class="decimal_field">
  <LowLevelDecimalField
    bind:value
    required={formfield.required}
    unit={formfield.unit === "FloatField" ? "" : "%"}
    max={formfield.max_value}
    min={formfield.min_value === "FloatField" ? "" : "0"}
    decimals={formfield.class === "IntegerField" ? 0 : 2}
  />
</div>
