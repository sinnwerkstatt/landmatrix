<script lang="ts">
  import { error } from "@sveltejs/kit"
  import { Client, gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { filters, FilterValues } from "$lib/filters"
  import { chartDescriptions, countries } from "$lib/stores"

  $: country = $filters.country_id && $countries.find(c => c.id === $filters.country_id)

  interface CountryStat {
    country_id: number
    count: number
    size: string
    country_name?: string
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
      country_name: $countries.find(c => c.id === x.country_id)?.name,
      ...x,
    }))
    investing_countries.sort(sortByDealSizeAndCount)
    invested_countries = countryInvestmentsAndRankings.invested.map(x => ({
      country_name: $countries.find(c => c.id === x.country_id)?.name,
      ...x,
    }))
    invested_countries.sort(sortByDealSizeAndCount)
  }

  const sortByDealSizeAndCount = (a: CountryStat, b: CountryStat): number => {
    if (+a.size > +b.size) return -1
    if (+a.size < +b.size) return 1

    if (a.count > b.count) return -1
    else if (a.count < b.count) return 1
    else return 0
  }

  $: _grabInvestmentsAndRankings($filters.country_id, $filters)
</script>

<div>
  <h2>{$_("Web of transnational deals")}</h2>
  <div>{@html $chartDescriptions?.web_of_transnational_deals}</div>
  {#if country}
    {#if investing_countries.length > 0}
      <div
        class="mb-5 border border-gray-300 bg-gray-100 p-4 text-sm shadow-inner dark:bg-gray-700"
      >
        <div>
          <b class="text-lg">
            {$_("Countries investing in {country}", {
              values: { country: country.name },
            })}
          </b>
          <table class="table-striped w-full">
            <tbody>
              {#each investing_countries as icountry}
                <tr>
                  <th class="text-left">{icountry.country_name}</th>
                  <td class="whitespace-nowrap text-right">
                    {icountry.count} deals
                    <br />
                    {icountry.size} ha
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    {/if}

    {#if invested_countries.length > 0}
      <div
        class="mb-5 border border-gray-300 bg-gray-100 p-4 text-sm shadow-inner dark:bg-gray-700"
      >
        <div>
          <b class="text-lg">
            {$_("Countries {country} invests in", {
              values: { country: country.name },
            })}
          </b>
          <table class="table-striped w-full">
            <tbody>
              {#each invested_countries as icountry}
                <tr>
                  <th class="text-left">{icountry.country_name}</th>
                  <td class="whitespace-nowrap text-right">
                    {icountry.count} deals
                    <br />
                    {icountry.size} ha
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </div>
    {/if}
  {/if}
</div>
