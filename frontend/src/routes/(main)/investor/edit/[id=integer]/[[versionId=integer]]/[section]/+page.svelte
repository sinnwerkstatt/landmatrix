<script lang="ts">
  import { investorSectionLookup } from "$components/Data/Investor/Sections/store"

  import { mutableInvestor } from "./store"

  export let data
</script>

<svelte:component
  this={$investorSectionLookup[data.investorSection].edit}
  bind:investor={$mutableInvestor}
/>
