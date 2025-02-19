<script lang="ts">
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"
  import { getMutableObject } from "$components/Data/stores"

  let { data } = $props()

  const mutableDeal = getMutableObject("deal")
  const SvelteComponent = $derived($dealSectionLookup[data.dealSection].edit)
</script>

<SvelteComponent bind:deal={$mutableDeal} />
