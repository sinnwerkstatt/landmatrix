<script lang="ts">
  import { page } from "$app/state"

  import LoadingSpinner from "$components/icons/LoadingSpinner.svelte"

  interface Props {
    value: number | null
  }

  let { value }: Props = $props()
</script>

{#if page.data.countries.length}
  {page.data.countries.find(c => c.id === value)?.name ?? ""}
{:else}
  <LoadingSpinner />
{/if}
