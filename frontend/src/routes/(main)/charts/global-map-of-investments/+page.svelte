<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { chartDescriptions } from "$lib/stores"
  import { isMobile } from "$lib/stores/basics"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import CountryInvestorInfo from "$components/Data/Charts/CountryInvestorInfo.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"

  import GlobalMapOfInvestments from "./GlobalMapOfInvestments.svelte"

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })
  let title = $derived($_("Global map of Investments"))
</script>

<svelte:head>
  <title>{title} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <GlobalMapOfInvestments {title} />

  {#snippet ContextBar()}
    <div>
      <h2 class="heading5">{title}</h2>
      <div>{@html $chartDescriptions.global_web_of_investments}</div>
      <CountryInvestorInfo />
    </div>
  {/snippet}
</ChartsContainer>
