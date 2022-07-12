<script lang="ts">
  import gql from "graphql-tag";
  import { onMount } from "svelte";
  import { browser } from "$app/env";
  import { client } from "$lib/apolloClient";
  import { filters } from "$lib/filters";
  import LoadingPulse from "$components/LoadingPulse.svelte";
  import { GlobalInvestmentMap } from "./globalMapOfInvestments.ts";

  let global_map: GlobalInvestmentMap | null = null;
  let global_map_of_investments = null;

  const grabInvestments = async () => {
    const { data } = await $client.query<{ transnational_deals: unknown[] }>({
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
    global_map_of_investments = data.global_map_of_investments;
    console.log("deals", global_map_of_investments);
  };

  onMount(() => (global_map = new GlobalInvestmentMap("#svg")));

  $: $filters && grabInvestments();
  $: browser && global_map && global_map.doTheThing(global_map_of_investments);
</script>

<div class="svg-container">
  {#if !global_map_of_investments}
    <LoadingPulse data-v-if="$apollo.queries.global_map_of_investments.loading" />
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

  //from https://codepen.io/chrislaskey/pen/jqabBQ
  .world-outline {
    fill: none;
    stroke: rgba(0, 0, 0, 0.1);
    stroke-width: 1px;
  }

  .back-country {
    fill: hsl(32, 57%, 90%);
    stroke: #fff;
    stroke-width: 0;
    stroke-linejoin: round;
  }

  .back-line {
    fill: none;
    stroke: #000;
    stroke-opacity: 0.05;
    stroke-width: 0.5px;
  }

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

  .line {
    fill: none;
    stroke: #000;
    stroke-opacity: 0.08;
    stroke-width: 0.5px;
  }

  .target-country-line {
    fill: none;
    stroke: var(--color-lm-orange-light);
    stroke-width: 0.6;
  }
  .investor-country-line {
    fill: none;
    stroke: var(--color-lm-investor-light);
    stroke-width: 0.6;
  }
  #incoming-marker {
    fill: var(--color-lm-investor);
  }
  #outgoing-marker {
    fill: var(--color-lm-orange);
  }
</style>
