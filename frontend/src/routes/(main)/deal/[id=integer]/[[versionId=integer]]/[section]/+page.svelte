<script lang="ts">
  import { dealSectionLookup } from "$components/Data/Deal/Sections/store"

  let { data } = $props()

  const SvelteComponent = $derived($dealSectionLookup[data.dealSection].display)
</script>

<div class="pb-20">
  <SvelteComponent deal={data.deal} />
</div>
