<script lang="ts">
  import DealEditForm from "$views/DealEditForm.svelte";
  import type { Deal } from "$lib/types/deal";

  // import type { PageData } from "./$types";

  // export let data: PageData;
  export let data: { deal: Deal; dealID: number; dealVersion: number };
</script>

<DealEditForm deal={data.deal} dealID={data.dealID} dealVersion={data.dealVersion} />
