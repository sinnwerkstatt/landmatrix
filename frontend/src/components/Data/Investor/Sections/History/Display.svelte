<script lang="ts">
  import type { InvestorHull } from "$lib/types/data"

  import SectionHistory from "$components/Data/SectionHistory.svelte"

  interface Props {
    investor: InvestorHull
  }

  let { investor }: Props = $props()
</script>

<SectionHistory obj={investor} investorColors />
