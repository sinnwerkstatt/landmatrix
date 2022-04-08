<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "$components/Fields/fields";

  export let value: string;
  export let model: string;
  export let formfield: FormField;

  $: val = !value ? "n/a" : formfield?.choices ? $_(formfield.choices[value]) : value;
</script>

<div class="text_field">
  {#if formfield.class === "URLField"}
    <a href="value" target="_blank">{new URL(value).hostname}</a>
  {:else}
    {val}
  {/if}
</div>
