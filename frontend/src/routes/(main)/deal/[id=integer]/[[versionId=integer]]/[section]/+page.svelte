<script lang="ts">
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"

  export let data
</script>

<div class="pb-20">
  <svelte:component
    this={$dealSectionLookup[data.dealSection].display}
    deal={data.deal}
  />
</div>
