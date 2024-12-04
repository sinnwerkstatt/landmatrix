<script lang="ts">
  // import { deals } from "$lib/accountability/placeholders"
  import { currentDeal, currentVariable, deals } from "$lib/accountability/stores"

  import DrawerScoring from "$components/Accountability/DrawerScoring.svelte"
  import TableDeals from "$components/Accountability/TableDeals.svelte"
</script>

<div class="h-full overflow-auto">
  <TableDeals deals={$deals} />
</div>

{#if $currentDeal && $currentVariable}
  <DrawerScoring />
{/if}
