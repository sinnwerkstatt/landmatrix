<script lang="ts">
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"

  import { mutableDeal } from "./store"

  export let data
</script>

<svelte:component
  this={$dealSectionLookup[data.dealSection].edit}
  bind:deal={$mutableDeal}
/>
