<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import type { Investments } from "./globalMapOfInvestments"

  interface Props {
    investments: Investments
    selectedCountryId: number | undefined
    hoverCountryId: number | undefined
  }

  let { investments, selectedCountryId, hoverCountryId }: Props = $props()

  let selectedCountry = $derived(
    page.data.countries.find(c => c.id === selectedCountryId),
  )
  let hoverCountry = $derived(page.data.countries.find(c => c.id === hoverCountryId))
</script>

<div class="absolute z-10" id="country-tooltip">
  {#if hoverCountryId && hoverCountry}
    <div
      class="max-w-[250px] rounded border border-gray-700 bg-white p-2 text-left dark:bg-gray-700"
    >
      <h4 class="heading5 text-lm-dark my-0 text-xl dark:text-white">
        {hoverCountry.name}
      </h4>
      <div class="flex flex-col">
        {#if hoverCountryId === selectedCountryId}
          {@const nInvestingCountries = Object.values(
            investments["incoming"][hoverCountryId] ?? {},
          ).length}
          {#if nInvestingCountries > 0}
            <span class="pt-2 text-sm font-bold text-red">
              {$_(
                "Investors from {nCountries} countries are involved in {countryName}",
                {
                  values: {
                    nCountries: nInvestingCountries,
                    countryName: hoverCountry.name,
                  },
                },
              )}
            </span>
          {/if}

          {@const nTargetedCountries = Object.values(
            investments["outgoing"][hoverCountryId] ?? {},
          ).length}
          {#if nTargetedCountries > 0}
            <span class="pt-2 text-sm font-bold text-purple">
              {$_(
                "Investors from {countryName} are involved in {nCountries} countries",
                {
                  values: {
                    nCountries: nTargetedCountries,
                    countryName: hoverCountry.name,
                  },
                },
              )}
            </span>
          {/if}
        {:else if selectedCountryId && selectedCountry}
          {@const outgoingInvestments = (investments["outgoing"][hoverCountryId] ?? {})[
            selectedCountryId
          ]}
          {#if outgoingInvestments}
            <span class="pt-2 text-sm font-bold text-red">
              {$_(
                "Investors from {investingCountryName} are involved in {nDeals} deals ({totalDealSize} ha) in {targetCountryName}",
                {
                  values: {
                    investingCountryName: hoverCountry.name,
                    nDeals: outgoingInvestments.count,
                    totalDealSize: (+outgoingInvestments.size)
                      .toLocaleString("fr")
                      .replace(",", "."),
                    targetCountryName: selectedCountry.name,
                  },
                },
              )}
            </span>
          {/if}

          {@const incomingInvestments = (investments["incoming"][hoverCountryId] ?? {})[
            selectedCountryId
          ]}
          {#if incomingInvestments}
            <span class="pt-2 text-sm font-bold text-purple">
              {$_(
                "Investors from {investingCountryName} are involved in {nDeals} deals ({totalDealSize} ha) in {targetCountryName}",
                {
                  values: {
                    investingCountryName: selectedCountry.name,
                    nDeals: incomingInvestments.count,
                    totalDealSize: (+incomingInvestments.size)
                      .toLocaleString("fr")
                      .replace(",", "."),
                    targetCountryName: hoverCountry.name,
                  },
                },
              )}
            </span>
          {/if}
        {/if}
      </div>
    </div>
  {/if}
</div>
