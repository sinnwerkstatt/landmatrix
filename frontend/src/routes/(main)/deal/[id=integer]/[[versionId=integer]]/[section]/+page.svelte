<script lang="ts">
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"

  export let data
</script>

<svelte:component
  this={$dealSectionLookup[data.dealSection].display}
  deal={data.deal}
/>
