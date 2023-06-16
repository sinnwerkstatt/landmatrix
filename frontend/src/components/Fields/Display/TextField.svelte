<script lang="ts">
  import type { FormField } from "$components/Fields/fields"

  export let value: string
  export let formfield: FormField
</script>

{#if !value}
  —
{:else if formfield.class === "URLField"}
  <a href={value} target="_blank" rel="noreferrer">{new URL(value).hostname}</a>
{:else}
  {value}
{/if}
