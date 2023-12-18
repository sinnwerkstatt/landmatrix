<script lang="ts">
  import { gql } from "@urql/svelte"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import { filters } from "$lib/filters"

  import LoadingPulse from "$components/LoadingPulse.svelte"

  import CountryTooltip from "./CountryTooltip.svelte"
  import type { GlobalMap, Investments } from "./globalMapOfInvestments"
  import { createGlobalMapOfInvestments } from "./globalMapOfInvestments"

  let globalMap: GlobalMap | null = null
  let investments: Investments | null = null
  let svgElement: SVGElement

  let selectedCountryId: number | undefined
  let hoverCountryId: number | undefined

  const setSelectedCountryId = (id: number | undefined) => {
    selectedCountryId = id
    $filters.country_id = id
    $filters.region_id = undefined
  }
  const setHoverCountryId = (id: number | undefined) => {
    hoverCountryId = id
  }

  const grabInvestments = async () => {
    const { error, data } = await $page.data.urqlClient
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

    if (error || !data) {
      console.error(error)
    } else {
      investments = data.global_map_of_investments
    }
  }

  $: if ($filters) {
    grabInvestments()
  }

  $: if (investments) {
    globalMap = createGlobalMapOfInvestments(
      svgElement,
      investments,
      setSelectedCountryId,
      setHoverCountryId,
    )
  }

  $: if (browser && globalMap && investments) {
    globalMap.selectCountry($filters.country_id)
  }
</script>

{#if !investments}
  <div class="mt-10">
    <LoadingPulse />
  </div>
{:else}
  <svg bind:this={svgElement} class="rounded">
    <defs>
      <pattern id="diagonalHatch" patternUnits="userSpaceOnUse" width="10" height="10">
        <rect width="10" height="10" class="fill-purple" />
        <path
          class="stroke-red stroke-[3]"
          d="
            M -2 2 L 2 -2
            M 0 10 L 10 0
            M 12 8 L 8 12
          "
        />
      </pattern>
    </defs>
  </svg>
  <CountryTooltip {investments} {selectedCountryId} {hoverCountryId} />
{/if}

<style lang="css">
  :global(svg .country) {
    @apply cursor-pointer fill-white stroke-black stroke-[0.3] hover:fill-gray-100;
  }
  :global(svg .selected-country) {
    @apply fill-gray-600 hover:fill-gray-300;
  }
  :global(svg .target-country) {
    @apply fill-purple hover:fill-purple-300;
  }
  :global(svg .investor-country) {
    @apply fill-red hover:fill-red-300;
  }
  :global(svg .investor-country.target-country) {
    @apply fill-[url(#diagonalHatch)] hover:opacity-70;
  }
  :global(svg .background) {
    fill: #7cb4d5;
  }
</style>
