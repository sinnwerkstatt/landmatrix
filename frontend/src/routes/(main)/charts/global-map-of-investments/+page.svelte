<script lang="ts">
  import { _ } from "svelte-i18n"
  import { onMount } from "svelte"

  import { isMobile, chartDescriptions } from "$lib/stores"

  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import CountryInvestorInfo from "$components/Data/Charts/CountryInvestorInfo.svelte"
  import GlobalMapOfInvestments from "$components/Data/Charts/GlobalMapOfInvestments.svelte"

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })
  $: title = $_("Global Map of Investments")
</script>

<svelte:head>
  <title>{title} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <h2 class="mt-0">{title}</h2>
  <GlobalMapOfInvestments />

  <div slot="ContextBar">
    <h2>{title}</h2>
    <div>{@html $chartDescriptions?.global_web_of_investments ?? ""}</div>
    <CountryInvestorInfo />
  </div>
</ChartsContainer>
