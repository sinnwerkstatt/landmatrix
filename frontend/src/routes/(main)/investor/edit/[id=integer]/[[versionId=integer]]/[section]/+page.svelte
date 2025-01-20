<script lang="ts">
  import { investorSectionLookup } from "$components/Data/Investor/Sections/store"

  import { mutableInvestor } from "../store"

  let { data } = $props()

  const SvelteComponent = $derived($investorSectionLookup[data.investorSection].edit)
</script>

<SvelteComponent bind:investor={$mutableInvestor} />
