<script lang="ts">
  import type { Client } from "@urql/svelte"
  import { gql } from "@urql/svelte"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import { filters } from "$lib/filters"

  import LoadingPulse from "$components/LoadingPulse.svelte"

  import type { Investments } from "./globalMapOfInvestments"
  import { createGlobalMapOfInvestments } from "./globalMapOfInvestments"

  let globalMap: ReturnType<typeof createGlobalMapOfInvestments> | null = null
  let investments: Investments | null = null

  const grabInvestments = async () => {
    const { data } = await ($page.data.urqlClient as Client)
      .query<{
        global_map_of_investments: Investments
      }>(
        gql`
          query GlobalMapOfInvestments($filters: [Filter]) {
            global_map_of_investments(filters: $filters)
          }
        `,
        {
          filters: $filters
            .toGQLFilterArray()
            .filter(
              f => f.field !== "country_id" && f.field !== "country.fk_region_id",
            ),
        },
      )
      .toPromise()
    investments = data?.global_map_of_investments ?? null
  }

  $: if (investments) {
    globalMap = createGlobalMapOfInvestments("#svg", id => ($filters.country_id = +id))
    globalMap.drawCountries()
  }

  $: $filters && grabInvestments()
  $: browser &&
    globalMap &&
    investments &&
    globalMap.injectData(investments, $filters.country_id)
</script>

<div class="svg-container">
  {#if !investments}
    <LoadingPulse />
  {/if}
  <svg id="svg" />
</div>

<style lang="css">
  :global(svg .country) {
    fill: white;
    stroke-width: 0.3;
    stroke: black;
    stroke-linejoin: round;
  }

  :global(svg .hover) {
    fill: hsla(0, 0%, 62%, 0.5);
  }
  :global(svg .selected-country) {
    fill: hsl(0, 0%, 32%);
  }
  :global(svg .target-country) {
    fill: var(--color-lm-orange);
  }
  :global(svg .investor-country) {
    fill: var(--color-lm-investor);
  }

  /*from https://codepen.io/chrislaskey/pen/jqabBQ*/
  /*.world-outline {*/
  /*  fill: #942a25;*/
  /*  stroke: rgba(0, 0, 0, 0.1);*/
  /*  stroke-width: 5px;*/
  /*  color: #942a25;*/
  /*}*/

  :global(svg .background) {
    fill: #7cb4d5;
  }

  :global(svg .target-country-line) {
    fill: none;
    /*stroke: var(--color-lm-orange);*/
    stroke: black;
    /*stroke-dasharray: 5px 2px;*/
    stroke-width: 0.6;
    marker-end: url(#outgoing-marker);
  }
  :global(svg .investor-country-line) {
    fill: none;
    /*stroke: var(--color-lm-investor);*/
    stroke: black;
    /*stroke-dasharray: 5px 2px;*/
    stroke-width: 0.6;
    marker-end: url(#incoming-marker);
  }

  :global(svg #incoming-marker) {
    fill: none;
  }
  :global(svg #outgoing-marker) {
    fill: none;
  }
</style>
