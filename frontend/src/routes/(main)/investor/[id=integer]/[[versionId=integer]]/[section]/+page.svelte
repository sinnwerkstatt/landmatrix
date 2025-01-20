<script lang="ts">
  import { investorSectionLookup } from "$components/Data/Investor/Sections/store"

  let { data } = $props()

  const SvelteComponent = $derived($investorSectionLookup[data.investorSection].display)
</script>

<div class="pb-20">
  <SvelteComponent investor={data.investor} />
</div>
