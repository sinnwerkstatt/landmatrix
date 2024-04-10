<script lang="ts">
  import { page } from "$app/stores"

  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"

  export let value: number | null
</script>

{#if $page.data.countries.length}
  {$page.data.countries.find(c => c.id === value)?.name ?? ""}
{:else}
  <LoadingSpinner />
{/if}
