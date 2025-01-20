<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"

  import { page } from "$app/state"

  import { filters, FilterValues } from "$lib/filters"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    downloadCSV,
    downloadJSON,
    downloadSVG,
    type FileType,
  } from "$components/Data/Charts/utils"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  import CountryTooltip from "./CountryTooltip.svelte"
  import type {
    CountryInvestments,
    CountryInvestmentsMap,
    GlobalMap,
    Investments,
  } from "./globalMapOfInvestments"
  import { createGlobalMapOfInvestments } from "./globalMapOfInvestments"

  interface Props {
    title: string
  }

  let { title }: Props = $props()

  let globalMap: GlobalMap | null = $state(null)
  let investments: Investments | null = $state(null)
  let svgElement: SVGElement | undefined = $state()

  let hoverCountryId: number | undefined = $state()
  let selectedCountryId: number | undefined = $derived($filters.country_id)

  const setSelectedCountryId = (id: number | undefined) => {
    if ($filters.country_id === id) return // without this, we have a reacitivity loop
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
  $effect(() => {
    grabInvestments($filters)
  })

  $effect(() => {
    if (!investments) return

    globalMap = createGlobalMapOfInvestments(
      svgElement!,
      investments,
      setSelectedCountryId,
      setHoverCountryId,
    )
  })
  $effect(() => {
    if (!globalMap) return
    globalMap.selectCountry(selectedCountryId)
  })

  const toJSON = (data: CountryInvestments): string => JSON.stringify(data, null, 2)

  const toCSV = (data: CountryInvestments): string => {
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
          const country = page.data.countries.find(c => c.id === +countryId)
          return [country?.name, investment]
        })
        .filter(([name]) => !!name),
    )

  const handleDownload = (fileType: FileType) => {
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
  <ChartWrapper {title} ondownload={handleDownload}>
    <svg bind:this={svgElement} class="global-map-of-investments rounded">
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
      <!--suppress CssUnusedSymbol -->
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

<!--suppress CssUnusedSymbol -->
<style lang="postcss">
  :global {
    .global-map-of-investments .country {
      @apply cursor-pointer fill-white stroke-black stroke-[0.3] hover:fill-gray-100;
    }
    .global-map-of-investments .selected-country {
      @apply fill-gray-600 hover:fill-gray-300;
    }

    .global-map-of-investments .target-country {
      @apply fill-purple hover:fill-purple-300;
    }

    .global-map-of-investments .investor-country {
      @apply fill-red hover:fill-red-300;
    }

    .global-map-of-investments .investor-country.target-country {
      @apply fill-[url(#diagonalHatch)] hover:opacity-70;
    }

    .global-map-of-investments .background {
      fill: #7cb4d5;
    }
  }
</style>
