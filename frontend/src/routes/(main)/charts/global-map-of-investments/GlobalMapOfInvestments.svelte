<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"

  import { browser } from "$app/environment"
  import { page } from "$app/stores"

  import { filters, FilterValues } from "$lib/filters"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  import CountryTooltip from "./CountryTooltip.svelte"
  import type {
    CountryInvestments,
    CountryInvestmentsMap,
    GlobalMap,
    Investments,
  } from "./globalMapOfInvestments"
  import { createGlobalMapOfInvestments } from "./globalMapOfInvestments"

  export let title: string

  let globalMap: GlobalMap | null = null
  let investments: Investments | null = null
  let svgElement: SVGElement

  let hoverCountryId: number | undefined
  let selectedCountryId: number | undefined
  $: selectedCountryId = $filters.country_id

  const setSelectedCountryId = (id: number | undefined) => {
    $filters.country_id = id
    $filters.region_id = undefined
  }
  const setHoverCountryId = (id: number | undefined) => {
    hoverCountryId = id
  }

  const grabInvestments = async (fltrs: FilterValues) => {
    const f1 = new FilterValues().copyNoCountry(fltrs)
    const ret = await fetch(
      `/api/charts/global_map_of_investments/?${f1.toRESTFilterArray()}`,
    )
    investments = await ret.json()
  }
  $: grabInvestments($filters)

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

  export const toJSON = (data: CountryInvestments): string =>
    JSON.stringify(data, null, 2)

  export const toCSV = (data: CountryInvestments): string => {
    let ret = "country,incoming,outgoing,size(ha),count\n"
    Object.entries(data.incoming).forEach(
      ([countryName, investment]) =>
        (ret += `${countryName},1,0,${investment.size},${investment.count}\n`),
    )
    Object.entries(data.outgoing).forEach(
      ([countryName, investment]) =>
        (ret += `${countryName},0,1,${investment.size},${investment.count}\n`),
    )
    return ret
  }

  const mapCountryNames = (countryInvestmentsMap: CountryInvestmentsMap) =>
    Object.fromEntries(
      Object.entries(countryInvestmentsMap)
        .map(([countryId, investment]) => {
          const country = $page.data.countries.find(c => c.id === +countryId)
          return [country?.name, investment]
        })
        .filter(([name]) => !!name),
    )

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    if (!selectedCountryId || !investments) {
      alert("Select a country to enable download")
      return
    }

    const countryInvestments: CountryInvestments = {
      incoming: mapCountryNames(investments.incoming[selectedCountryId] ?? {}),
      outgoing: mapCountryNames(investments.outgoing[selectedCountryId] ?? {}),
    }
    if ($tracker) $tracker.trackEvent("Chart", "Global map of investments", fileType)

    switch (fileType) {
      case "json":
        return downloadJSON(toJSON(countryInvestments), title)
      case "csv":
        return downloadCSV(toCSV(countryInvestments), title)
      default:
        return downloadSVG(svgElement, fileType, title)
    }
  }
</script>

{#if !investments}
  <div class="mt-10">
    <LoadingPulse />
  </div>
{:else}
  <ChartWrapper {title} on:download={handleDownload}>
    <svg bind:this={svgElement} class="rounded">
      <defs>
        <pattern
          id="diagonalHatch"
          patternUnits="userSpaceOnUse"
          width="10"
          height="10"
        >
          <rect width="10" height="10" class="fill-purple" style="fill: #7886ec;" />
          <path
            class="stroke-red stroke-[3]"
            style="stroke: #e8726a; stroke-width: 3;"
            d="
            M -2 2 L 2 -2
            M 0 10 L 10 0
            M 12 8 L 8 12
          "
          />
        </pattern>
      </defs>
      <style lang="css">
        .country {
          fill: white;
          stroke: black;
          stroke-width: 0.3;
        }
        .selected-country {
          fill: #666666;
        }
        .target-country {
          fill: #7886ec;
        }
        .investor-country {
          fill: #e8726a;
        }
        .investor-country.target-country {
          fill: url(#diagonalHatch);
        }
        .background {
          fill: #7cb4d5;
        }
      </style>
    </svg>
    <CountryTooltip {investments} {selectedCountryId} {hoverCountryId} />
  </ChartWrapper>
{/if}

<style lang="postcss">
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
