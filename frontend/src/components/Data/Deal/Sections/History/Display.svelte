<script lang="ts">
  import type { DealHull } from "$lib/types/data"

  import SectionHistory from "$components/Data/SectionHistory.svelte"

  interface Props {
    deal: DealHull
  }

  let { deal }: Props = $props()
</script>

<SectionHistory obj={deal} />
