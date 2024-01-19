<script lang="ts">
  export let value: string

  export let extras = { url: false }
</script>

{#if extras.url}
  <a href={value} target="_blank" rel="noreferrer">{new URL(value).hostname}</a>
{:else}
  {value ?? "—"}
{/if}
