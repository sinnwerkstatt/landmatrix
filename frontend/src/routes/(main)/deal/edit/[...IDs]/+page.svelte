<script lang="ts">
  import DealEditForm from "./DealEditForm.svelte"

  export let data
</script>

<DealEditForm deal={data.deal} dealID={data.dealID} versionID={data.versionID} />
