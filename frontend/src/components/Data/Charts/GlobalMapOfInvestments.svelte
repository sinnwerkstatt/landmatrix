<script lang="ts">
  import type { Client } from "@urql/svelte"
  import { gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import { filters } from "$lib/filters"

  import LoadingPulse from "$components/LoadingPulse.svelte"

  import type { Investments, TooltipData } from "./globalMapOfInvestments"
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
    globalMap = createGlobalMapOfInvestments(
      "#svg",
      id => ($filters.country_id = +id),
      tooltipData => {
        tooltip = tooltipData
      },
    )
    globalMap.drawCountries()
  }

  $: $filters && grabInvestments()
  $: browser &&
    globalMap &&
    investments &&
    globalMap.injectData(investments, $filters.country_id)

  let tooltip: TooltipData | undefined
</script>

{#if !investments}
  <LoadingPulse />
{/if}
<svg id="svg">
  <defs>
    <pattern id="diagonalHatch" patternUnits="userSpaceOnUse" width="10" height="10">
      <rect width="10" height="10" class="fill-lm-purple" />
      <path
        class="stroke-lm-red stroke-[3]"
        d="
            M -2 2 L 2 -2
            M 0 10 L 10 0
            M 12 8 L 8 12
          "
      />
    </pattern>
  </defs>
</svg>

{#if tooltip}
  <div
    class="absolute z-10 rounded border border-gray-dark bg-white p-2 text-left dark:bg-gray-dark"
    style="top:{tooltip.y}px;left:{tooltip.x}px;"
  >
    <h4 class="my-0 dark:text-white">{tooltip.name}</h4>
    <div class="flex flex-col">
      <span class="font-bold text-lm-purple">
        {tooltip.nTargets}
        {tooltip.nTargets === 1 ? $_("target country") : $_("target countries")}
      </span>
      <span class="font-bold text-lm-red">
        {tooltip.nInvestors}
        {tooltip.nInvestors === 1 ? $_("investor country") : $_("investor countries")}
      </span>
    </div>
  </div>
{/if}

<style lang="css">
  :global(svg .country) {
    @apply cursor-pointer fill-white stroke-black stroke-[0.3] hover:fill-gray-light;
  }
  :global(svg .selected-country) {
    @apply fill-gray-dark hover:fill-gray-medium;
  }
  :global(svg .target-country) {
    @apply fill-lm-purple hover:fill-lm-purple-300;
  }
  :global(svg .investor-country) {
    @apply fill-lm-red hover:fill-lm-red-300;
  }
  :global(svg .investor-country.target-country) {
    @apply fill-[url(#diagonalHatch)] hover:opacity-70;
  }
  :global(svg .background) {
    fill: #7cb4d5;
  }
</style>
