<script lang="ts">
  import { countries } from "$lib/stores"

  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"

  export let value: number | null
</script>

{#if $countries.length}
  {$countries.find(c => c.id === value)?.name ?? ""}
{:else}
  <LoadingSpinner />
{/if}
