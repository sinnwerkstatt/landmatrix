<script lang="ts">
  import DealEditForm from "$views/DealEditForm.svelte";
  import type { Deal } from "$lib/types/deal";

  let deal: Deal = { id: -1, contracts: [], datasources: [], locations: [] } as Deal;
  let dealID;
  let dealVersion;
</script>

<DealEditForm bind:deal bind:dealID bind:dealVersion />
