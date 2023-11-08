<script lang="ts">
  import { error } from "@sveltejs/kit"
  import { Client, gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { filters, FilterValues } from "$lib/filters"
  import { countries } from "$lib/stores"

  $: country = $filters.country_id && $countries.find(c => c.id === $filters.country_id)

  interface CountryStat {
    country_id: number
    count: number
    size: number
    name?: string
  }
  let investing_countries: CountryStat[] = []
  let invested_countries: CountryStat[] = []

  async function _grabInvestmentsAndRankings(
    countryID: number | undefined,
    fltrs: FilterValues,
  ) {
    if (!countryID) return
    const ret = await ($page.data.urqlClient as Client)
      .query<{
        country_investments_and_rankings: {
          investing: CountryStat[]
          invested: CountryStat[]
        }
      }>(
        gql`
          query InvestmentsAndRankings($id: Int!, $filters: [Filter]) {
            country_investments_and_rankings(id: $id, filters: $filters)
          }
        `,
        {
          id: countryID,
          filters: fltrs
            .toGQLFilterArray()
            .filter(f => f.field !== "country_id" && f.field !== "country.region_id"),
        },
      )
      .toPromise()

    if (!ret.data?.country_investments_and_rankings)
      throw error(502, `problems fetching data: ${ret.error}`)

    let countryInvestmentsAndRankings = ret.data.country_investments_and_rankings

    investing_countries = countryInvestmentsAndRankings.investing.map(x => ({
      name: $countries.find(c => c.id === x.country_id)?.name,
      ...x,
      size: +x.size,
    }))
    investing_countries.sort(sortByDealSizeAndCount)

    invested_countries = countryInvestmentsAndRankings.invested.map(x => ({
      name: $countries.find(c => c.id === x.country_id)?.name,
      ...x,
      size: +x.size,
    }))
    invested_countries.sort(sortByDealSizeAndCount)
  }

  const sortByDealSizeAndCount = (a: CountryStat, b: CountryStat): number => {
    if (a.size > b.size) return -1
    if (a.size < b.size) return 1

    if (a.count > b.count) return -1
    else if (a.count < b.count) return 1
    else return 0
  }

  $: _grabInvestmentsAndRankings($filters.country_id, $filters)
</script>

<div class="text-lm-dark dark:text-white">
  {#if country}
    <h3>{country.name}</h3>

    {#if invested_countries.length > 0}
      <h4 class="my-0 rounded-t border-2 border-b-0 border-lm-purple py-2 text-center">
        {$_("invests in")}
      </h4>
      <div class="mb-5 rounded-b border-2 border-lm-purple p-4 text-sm shadow-inner">
        <table class="table-striped w-full">
          <tbody>
            {#each invested_countries as country}
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

    {#if investing_countries.length > 0}
      <h4 class="my-0 rounded-t border-2 border-b-0 border-lm-red py-2 text-center">
        {$_("investments from")}
      </h4>
      <div class="mb-5 rounded-b border-2 border-lm-red p-4 text-sm shadow-inner">
        <table class="table-striped w-full">
          <tbody>
            {#each investing_countries as country}
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
