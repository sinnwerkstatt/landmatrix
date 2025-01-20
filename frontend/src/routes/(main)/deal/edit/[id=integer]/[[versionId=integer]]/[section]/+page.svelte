<script lang="ts">
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"

  import { mutableDeal } from "../store"

  let { data } = $props()

  const SvelteComponent = $derived($dealSectionLookup[data.dealSection].edit)
</script>

<SvelteComponent bind:deal={$mutableDeal} />
