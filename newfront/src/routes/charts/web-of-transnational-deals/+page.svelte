<script lang="ts">
  import { Client, gql } from "@urql/svelte";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { browser } from "$app/environment";
  import { page } from "$app/stores";
  import { LandMatrixRadialSpider } from "$lib/data/charts/d3_hierarchical_edge_bundling";
  import type { EdgeBundlingData } from "$lib/data/charts/d3_hierarchical_edge_bundling";
  import { filters } from "$lib/filters";
  import { showContextBar } from "$components/Data";
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte";
  import ContextBarWebOfTransnationalDeals from "$components/Data/Charts/ContextBarWebOfTransnationalDeals.svelte";
  import LoadingPulse from "$components/LoadingPulse.svelte";

  let transnational_deals: EdgeBundlingData | undefined = undefined;

  function redrawSpider(deals, country_id): void {
    LandMatrixRadialSpider(
      deals,
      "#svg-container > svg",
      country_id,
      (country) => ($filters.country_id = +country)
    );
  }

  const grabTransnationalDeals = async () => {
    const { data } = await ($page.data.urqlClient as Client)
      .query<{ transnational_deals: EdgeBundlingData }>(
        gql`
          query ($filters: [Filter]) {
            transnational_deals(filters: $filters)
          }
        `,
        {
          filters: $filters
            .toGQLFilterArray()
            .filter((f) => f.field !== "country_id" && f.field !== "country.region_id"),
        }
      )
      .toPromise();
    transnational_deals = data?.transnational_deals;
  };

  $: $filters && grabTransnationalDeals();
  $: browser && redrawSpider(transnational_deals, $filters.country_id);
  onMount(() => showContextBar.set(true));
</script>

<svelte:head>
  <title>{$_("Web of transnational deals")} | {$_("Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  {#if !transnational_deals}
    <div class="absolute inset-0">
      <LoadingPulse data-v-if="$apollo.queries.transnational_deals.loading" />
    </div>
  {/if}

  <div id="svg-container" class="max-h-full w-full p-8 pt-16">
    <svg />
  </div>

  <div slot="ContextBar">
    <ContextBarWebOfTransnationalDeals />
  </div>
</ChartsContainer>

<!--suppress CssUnusedSymbol, CssUnknownTarget -->
<style>
  :global(#incoming-marker) {
    fill: var(--color-lm-orange);
  }
  :global(#outgoing-marker) {
    fill: var(--color-lm-investor);
  }

  :global(path.incoming-highlighted) {
    stroke: var(--color-lm-orange);
    stroke-width: 2;
    marker-start: url(#incoming-marker);
  }
  :global(path.outgoing-highlighted) {
    stroke: var(--color-lm-investor);
    stroke-width: 2;
    marker-start: url(#outgoing-marker);
  }

  :global(path.incoming-permahighlight) {
    stroke: var(--color-lm-orange);
    stroke-width: 2.5;
    marker-start: url(#incoming-marker);
  }
  :global(path.outgoing-permahighlight) {
    stroke: var(--color-lm-investor);
    stroke-width: 2.5;
    marker-start: url(#outgoing-marker);
  }

  :global(text.incoming-highlighted) {
    font-size: 14px;
    cursor: pointer;
    font-weight: bold;
    fill: var(--color-lm-orange);
  }
  :global(text.outgoing-highlighted) {
    font-size: 14px;
    cursor: pointer;
    font-weight: bold;
    fill: var(--color-lm-investor);
  }
</style>
