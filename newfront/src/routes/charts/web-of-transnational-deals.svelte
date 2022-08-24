<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";
  import { showContextBar } from "$components/Data";

  export const load: Load = async () => {
    showContextBar.set(true);
    return {};
  };
</script>

<script lang="ts">
  import { gql } from "@urql/svelte";
  import { _ } from "svelte-i18n";
  import { browser } from "$app/env";
  import { page } from "$app/stores";
  import { filters } from "$lib/filters";
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte";
  import ContextBarWebOfTransnationalDeals from "$components/Data/Charts/ContextBarWebOfTransnationalDeals.svelte";
  import LoadingPulse from "$components/LoadingPulse.svelte";
  import { LandMatrixRadialSpider } from "./d3_hierarchical_edge_bundling";

  let transnational_deals = [];

  function redrawSpider(deals, country_id): void {
    LandMatrixRadialSpider(
      deals,
      "#svg-container > svg",
      country_id,
      (country) => ($filters.country_id = +country)
    );
  }

  const grabTransnationalDeals = async () => {
    const { data } = await $page.stuff.urqlClient
      .query(
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
    transnational_deals = data.transnational_deals;
  };

  $: $filters && grabTransnationalDeals();
  $: browser && redrawSpider(transnational_deals, $filters.country_id);
</script>

<svelte:head>
  <title>{$_("Web of transnational deals | Land Matrix")}</title>
</svelte:head>

<ChartsContainer>
  {#if transnational_deals.length === 0}
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
