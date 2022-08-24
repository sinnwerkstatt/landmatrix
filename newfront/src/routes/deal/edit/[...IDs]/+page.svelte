<script lang="ts">
  import DealEditForm from "$views/DealEditForm.svelte";
  import type { PageData } from "./$types";

  export let data: PageData;
</script>

<DealEditForm deal={data.deal} dealID={data.dealID} dealVersion={data.dealVersion} />
