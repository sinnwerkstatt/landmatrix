<script lang="ts">
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"

  import { showContextBar } from "$components/Data/stores"
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import ContextBarWebOfTransnationalDeals from "$components/Data/Charts/ContextBarWebOfTransnationalDeals.svelte"
  import GlobalMapOfInvestments from "$components/Data/Charts/GlobalMapOfInvestments.svelte"

  onMount(() => showContextBar.set(true))

  $: title = $_("Global Map of Investments")
</script>

<svelte:head>
  <title>{title} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <GlobalMapOfInvestments />

  <div slot="ContextBar">
    <ContextBarWebOfTransnationalDeals />
  </div>
</ChartsContainer>
