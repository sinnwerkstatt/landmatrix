<script lang="ts">
  import SectionDataSources from "$components/SectionDataSources.svelte"

  export let data
</script>

<SectionDataSources version={data.deal.selected_version} />
