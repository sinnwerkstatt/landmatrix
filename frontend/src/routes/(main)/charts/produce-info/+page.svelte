<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { chartDescriptions, dealsNG, isMobile } from "$lib/stores"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import ProduceInfoMap from "$components/Data/Charts/ProduceInfoMap.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  $: title = $_("Produce info map")

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })
</script>

<svelte:head>
  <title>{title} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  {#if $dealsNG.length === 0}
    <LoadingPulse />
  {:else}
    <ProduceInfoMap deals={$dealsNG} {title} />
  {/if}

  <div slot="ContextBar">
    <h2 class="heading4 text-lm-dark">{title}</h2>
    <div>{@html $chartDescriptions?.produce_info_map ?? ""}</div>
  </div>
</ChartsContainer>
