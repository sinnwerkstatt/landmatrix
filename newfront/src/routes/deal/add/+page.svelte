<script lang="ts">
  import type { Deal } from "$lib/types/deal"

  import DealEditForm from "$views/DealEditForm.svelte"

  let deal: Deal = { id: -1, contracts: [], datasources: [], locations: [] } as Deal
  let dealID: number
  let dealVersion: number
</script>

<DealEditForm bind:deal bind:dealID bind:dealVersion />
