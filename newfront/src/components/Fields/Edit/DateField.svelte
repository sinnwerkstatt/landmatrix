<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "../fields";
  import LowLevelDateYearField from "./LowLevelDateYearField.svelte";

  export let formfield: FormField;
  export let value;
</script>

<div class="date_field">
  <LowLevelDateYearField bind:value name={formfield.name} />
</div>
