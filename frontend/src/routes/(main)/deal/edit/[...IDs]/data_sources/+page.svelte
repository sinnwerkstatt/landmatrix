<script lang="ts">
  import EditSectionDataSources from "$components/EditSectionDataSources.svelte"

  import { mutableDeal } from "../store"

  export let data

  let datasources = data.deal.selected_version.datasources
  $: $mutableDeal.selected_version.datasources = datasources
</script>

<EditSectionDataSources bind:datasources />
