<script lang="ts">
  import { _ } from "svelte-i18n"

  import { filters, FilterValues } from "$lib/filters"
  import { countries } from "$lib/stores"
  import type { Country } from "$lib/types/wagtail"

  interface CountryStat {
    country_id: number
    count: number
    size: number
    name?: string
  }

  let country: Country | undefined
  $: country = $countries.find(c => c.id === $filters.country_id)

  let investingCountries: CountryStat[] = []
  let investedCountries: CountryStat[] = []

  async function grabInvestmentsAndRankings(
    country: Country | undefined,
    fltrs: FilterValues,
  ) {
    if (!country) return

    const f1 = new FilterValues().copyNoCountry(fltrs)

    const ret = await fetch(
      `/api/charts/country_investments_and_rankings/?CID=${
        country.id
      }&${f1.toRESTFilterArray()}`,
    )
    const rankings = await ret.json()

    investingCountries = rankings.investing.map(x => ({
      name: $countries.find(c => c.id === x.country_id)?.name,
      ...x,
      size: +x.size,
    }))
    investingCountries.sort(sortByDealSizeAndCount)

    investedCountries = rankings.invested.map(x => ({
      name: $countries.find(c => c.id === x.country_id)?.name,
      ...x,
      size: +x.size,
    }))
    investedCountries.sort(sortByDealSizeAndCount)
  }

  const sortByDealSizeAndCount = (a: CountryStat, b: CountryStat): number => {
    if (a.size > b.size) return -1
    if (a.size < b.size) return 1

    if (a.count > b.count) return -1
    else if (a.count < b.count) return 1
    else return 0
  }

  $: grabInvestmentsAndRankings(country, $filters)
</script>

<div class="text-gray-700 dark:text-white">
  {#if country}
    <h3 class="heading4 text-center text-gray-700">{country.name}</h3>

    {#if investedCountries.length > 0}
      <h4
        class="heading5 my-0 rounded-t border-2 border-b-0 border-purple py-2 text-center"
      >
        {$_("invests in")}
      </h4>
      <div class="mb-5 rounded-b border-2 border-purple p-4 text-sm shadow-inner">
        <table class="table-striped w-full">
          <tbody>
            {#each investedCountries as country}
              <tr>
                <th class="text-left">{country.name}</th>
                <td class="whitespace-nowrap text-right">
                  {country.count}
                  {country.count === 1 ? "deal" : "deals"}
                  <br />
                  {country.size.toLocaleString("fr")} ha
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}

    {#if investingCountries.length > 0}
      <h4
        class="heading5 my-0 rounded-t border-2 border-b-0 border-red py-2 text-center"
      >
        {$_("investments from")}
      </h4>
      <div class="mb-5 rounded-b border-2 border-red p-4 text-sm shadow-inner">
        <table class="table-striped w-full">
          <tbody>
            {#each investingCountries as country}
              <tr>
                <th class="text-left">{country.name}</th>
                <td class="whitespace-nowrap text-right">
                  {country.count}
                  {country.count === 1 ? "deal" : "deals"}
                  <br />
                  {country.size.toLocaleString("fr")} ha
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {/if}
  {:else}
    <span class="font-bold">
      {$_("Select or click on a country for investment details.")}
    </span>
  {/if}
</div>
