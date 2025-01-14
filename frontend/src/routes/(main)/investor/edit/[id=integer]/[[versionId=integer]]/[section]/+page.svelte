<script lang="ts">
  import { investorSectionLookup } from "$components/Data/Investor/Sections/store"
  import { getMutableObject } from "$components/Data/stores"

  let { data } = $props()

  const mutableInvestor = getMutableObject("investor")
  const SvelteComponent = $derived($investorSectionLookup[data.investorSection].edit)
</script>

<SvelteComponent bind:investor={$mutableInvestor} />
