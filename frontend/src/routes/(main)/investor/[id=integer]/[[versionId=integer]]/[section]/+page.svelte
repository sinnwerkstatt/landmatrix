<script lang="ts">
  import { investorSectionLookup } from "$components/Data/Investor/Sections/store"

  export let data
</script>

<div class="pb-20">
  <svelte:component
    this={$investorSectionLookup[data.investorSection].display}
    investor={data.investor}
  />
</div>
