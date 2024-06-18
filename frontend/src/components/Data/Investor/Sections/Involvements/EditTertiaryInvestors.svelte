<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import EditBase from "./Edit.svelte"

  export let investor: InvestorHull
</script>

<EditBase bind:investor tertiary />
