<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import SectionHistory from "$components/Data/SectionHistory.svelte"

  export let investor: InvestorHull
</script>

<SectionHistory obj={investor} investorColors />
