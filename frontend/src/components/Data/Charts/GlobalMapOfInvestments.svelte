<script lang="ts">
  import gql from "graphql-tag";
  import { onMount } from "svelte";
  import { browser } from "$app/env";
  import { client } from "$lib/apolloClient";
  import { filters } from "$lib/filters";
  import LoadingPulse from "$components/LoadingPulse.svelte";
  import type { Investments } from "./globalMapOfInvestments";
  import { createGlobalMapOfInvestments } from "./globalMapOfInvestments.ts";

  let globalMap: ReturnType<createGlobalMapOfInvestments> | null = null;
  let investments: Investments | null = null;

  const grabInvestments = async () => {
    const { data } = await $client.query<{
      global_map_of_investments: Investments;
    }>({
      query: gql`
        query GlobalMapOfInvestments($filters: [Filter]) {
          global_map_of_investments(filters: $filters)
        }
      `,
      variables: {
        filters: $filters
          .toGQLFilterArray()
          .filter(
            (f) => f.field !== "country_id" && f.field !== "country.fk_region_id"
          ),
      },
    });
    investments = data.global_map_of_investments;
  };

  onMount(() => {
    globalMap = createGlobalMapOfInvestments(
      "#svg",
      (id) => ($filters.country_id = +id)
    );
    globalMap.drawCountries();
  });

  $: $filters && grabInvestments();
  $: browser &&
    globalMap &&
    investments &&
    globalMap.injectData(investments, $filters.country_id);
</script>

<div class="svg-container">
  {#if !investments}
    <LoadingPulse />
  {/if}
  <svg id="svg" />
</div>

<style global lang="scss">
  .svg-container {
    height: 100%;
    width: 100%;
    overflow: hidden;
    background: #dff0fa;
  }

  svg {
    .country {
      fill: white;
      stroke-width: 0.3;
      stroke: black;
      stroke-linejoin: round;
      &.hover {
        fill: hsla(0, 0%, 62%, 0.5);
      }
      &.selected-country {
        fill: hsl(0, 0%, 32%);
      }
      &.target-country {
        fill: var(--color-lm-orange);
      }
      &.investor-country {
        fill: var(--color-lm-investor);
      }
    }

    //from https://codepen.io/chrislaskey/pen/jqabBQ
    //.world-outline {
    //  fill: #942a25;
    //  stroke: rgba(0, 0, 0, 0.1);
    //  stroke-width: 5px;
    //  color: #942a25;
    //}

    .background {
      fill: #7cb4d5;
    }

    .target-country-line {
      fill: none;
      stroke: var(--color-lm-orange-light);
      stroke-width: 0.6;
      marker-end: url(#outgoing-marker);
    }
    .investor-country-line {
      fill: none;
      stroke: var(--color-lm-investor-light);
      stroke-width: 0.6;
      marker-end: url(#incoming-marker);
    }

    #incoming-marker {
      fill: var(--color-lm-investor-dark);
    }
    #outgoing-marker {
      fill: var(--color-lm-orange-dark);
    }
  }
</style>
