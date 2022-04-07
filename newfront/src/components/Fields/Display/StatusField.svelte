<script lang="ts">
  import type { FormField } from "$components/Fields/fields";
  import { _ } from "svelte-i18n";
  import { combined_status_fn } from "./choices";

  export let formfield: FormField;
  export let value: number[];
  export let model: string;

  $: display_status = $_(combined_status_fn(value[0], value[1], true));
</script>

<span class="status_field">{display_status}</span>
