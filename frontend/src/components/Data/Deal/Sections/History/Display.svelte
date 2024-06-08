<script lang="ts">
  import type { DealHull } from "$lib/types/newtypes"

  import SectionHistory from "$components/SectionHistory.svelte"

  export let deal: DealHull
</script>

<SectionHistory obj={deal} />
