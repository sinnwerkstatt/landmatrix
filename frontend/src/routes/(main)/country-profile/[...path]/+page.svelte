<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { dealsNG } from "$lib/stores"
  import { isMobile } from "$lib/stores/basics"

  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte"
  import { showContextBar, showFilterBar } from "$components/Data/stores"
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  export let data

  onMount(() => {
    showContextBar.set(!$isMobile)
    showFilterBar.set(!$isMobile)
  })
</script>

<svelte:head>
  <title>{$_("Country profile charts")} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  <div class="h-full w-full overflow-visible">
    {#if $dealsNG.length === 0}
      <LoadingPulse />
    {:else}
      <svelte:component
        this={data.profile.component}
        deals={$dealsNG.map(d => d.selected_version)}
      />
    {/if}
  </div>

  <div slot="ContextBar">
    <h2 class="heading5">{$_("Country profile charts")}</h2>
    <!-- TODO: Generalize chartDescriptions to include country profiles as well -->
    <!-- <div>{@html $chartDescriptions[data.profile.key] ?? ""}</div>-->
    <DealDisplayToggle />
  </div>
</ChartsContainer>
