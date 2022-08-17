<script lang="ts">
  import { _ } from "svelte-i18n";
  import { combined_status_fn } from "$lib/choices";

  export let value: number[];

  $: display_status = $_(combined_status_fn(value[0], value[1], true));
</script>

<span class="status_field">{display_status}</span>
