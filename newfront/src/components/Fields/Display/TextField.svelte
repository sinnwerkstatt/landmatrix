<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { FormField } from "$components/Fields/fields";

  export let value: string;
  export let formfield: FormField;
</script>

<div class="text_field">
  {#if !value}
    n/a
  {:else if formfield.class === "URLField"}
    <a href={value} target="_blank">{new URL(value).hostname}</a>
  {:else if formfield?.choices}
    {$_(formfield.choices[value])}
  {:else}
    {value}
  {/if}
</div>
