<script lang="ts">
  import { investorSectionLookup } from "$components/Data/Investor/Sections/store"
  import { mutableInvestor } from "$components/Data/stores"

  let { data } = $props()

  const SvelteComponent = $derived($investorSectionLookup[data.investorSection].edit)
</script>

<SvelteComponent bind:investor={$mutableInvestor} />
