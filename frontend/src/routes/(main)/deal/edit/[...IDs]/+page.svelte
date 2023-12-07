<script lang="ts">
  import DealEditForm from "$components/Deal/DealEditForm.svelte"

  export let data
</script>

<!--<DealEditForm deal={data.deal} dealID={data.dealID} dealVersion={data.dealVersion} />-->

{JSON.stringify(data)}
