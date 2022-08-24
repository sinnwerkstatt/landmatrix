<script lang="ts">
  import { gql } from "@urql/svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { filters, FilterValues } from "$lib/filters";
  import { chartDescriptions, countries } from "$lib/stores";

  $: country =
    $filters.country_id && $countries.find((c) => c.id === $filters.country_id);

  let global_rankings;
  let country_investments_and_rankings: {
    investing: [];
    invested: [];
    ranking_deal: null;
    ranking_investor: null;
  };
  let investing_countries = [];
  let invested_countries = [];

  async function _grabInvestmentsAndRankings(countryID: number, fltrs: FilterValues) {
    if (!countryID) return;
    const { data } = await $page.stuff.urqlClient
      .query(
        gql`
          query InvestmentsAndRankings($id: Int!, $filters: [Filter]) {
            country_investments_and_rankings(id: $id, filters: $filters)
          }
        `,
        {
          id: countryID,
          filters: fltrs
            .toGQLFilterArray()
            .filter((f) => f.field !== "country_id" && f.field !== "country.region_id"),
        }
      )
      .toPromise();

    let countryInvestmentsAndRankings = data.country_investments_and_rankings;
    investing_countries = countryInvestmentsAndRankings.investing.map((x) => ({
      country_name: $countries.find((c) => c.id === x.country_id).name,
      ...x,
    }));
    invested_countries = countryInvestmentsAndRankings.invested.map((x) => ({
      country_name: $countries.find((c) => c.id === x.country_id).name,
      ...x,
    }));
  }

  $: _grabInvestmentsAndRankings($filters.country_id, $filters);

  //     apollo: {
  //     global_rankings: {
  //       query: gql`
  //         query GlobalRankings($filters: [Filter]) {
  //           global_rankings(filters: $filters)
  //         }
  //       `,
  //       variables() {
  //         return {
  //           filters: this.$store.getters.defaultFiltersForGQL,
  //         };
  //       },
  //     },
  // global_ranking_deals() {
  //   if (!this.global_rankings) return;
  //   if (this.$store.state.countries.length === 0) return;
  //   return this.global_rankings.ranking_deal.map((x) => {
  //     let country_name = this.getCountryOrRegion({
  //       id: +x.country_id,
  //     }).name;
  //     return { country_name, ...x };
  //   });
  // },
  // global_ranking_investors() {
  //   if (!this.global_rankings) return;
  //   if (this.$store.state.countries.length === 0) return;
  //   return this.global_rankings.ranking_investor.map((x) => {
  //     let country_name = this.getCountryOrRegion({
  //       id: +x.country_id,
  //     }).name;
  //     return { country_name, ...x };
  //   });
  // },
</script>

<div>
  <h2>{$_("Web of transnational deals")}</h2>
  <div>{@html $chartDescriptions?.web_of_transnational_deals}</div>
  {#if country}
    <div class="p-4 text-sm mb-5 bg-gray-100 border border-gray-300 shadow-inner">
      <h4 class="mt-0">{country.name}</h4>
      <!--      <div class="mx-3">-->
      <!--        <b-->
      <!--          class="deal-ranking"-->
      <!--          v-if="this.country_investments_and_rankings.ranking_deal"-->
      <!--        >-->
      <!--          <i class="fas fa-compress-arrows-alt"></i> #{{-->
      <!--            this.country_investments_and_rankings.ranking_deal-->
      <!--          }}-->
      <!--        </b>-->
      <!--        &nbsp;-->
      <!--        <b-->
      <!--          class="investor-ranking"-->
      <!--          v-if="this.country_investments_and_rankings.ranking_investor"-->
      <!--        >-->
      <!--          <i class="fas fa-expand-arrows-alt"></i> #{{-->
      <!--            this.country_investments_and_rankings.ranking_investor-->
      <!--          }}-->
      <!--        </b>-->
      <!--      </div>-->
      {#if investing_countries.length > 0}
        <div>
          <b class="text-lg">
            {$_("Countries investing in {country}", {
              values: { country: country.name },
            })}
          </b>
          <table class="w-full table-striped">
            <tbody>
              {#each investing_countries as icountry}
                <tr>
                  <th class="text-left">{icountry.country_name}</th>
                  <td class="text-right whitespace-nowrap">
                    {icountry.count} deals<br />
                    {icountry.size} ha
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
      {#if invested_countries.length > 0}
        <div class="mt-6">
          <b class="text-lg">
            {$_("Countries {country} invests in", {
              values: { country: country.name },
            })}
          </b>
          <table class="w-full table-striped">
            <tbody>
              {#each invested_countries as icountry}
                <tr>
                  <th class="text-left">{icountry.country_name}</th>
                  <td class="text-right whitespace-nowrap">
                    {icountry.count} deals<br />
                    {icountry.size} ha
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>
  {/if}
  <!--    <div v-else class="hint-box">-->
  <!--      <h4>{{ $t("Global ranking") }}</h4>-->
  <!--      <div v-if="global_rankings">-->
  <!--        <b><i class="fas fa-compress-arrows-alt"></i> Top invested-in Countries</b>-->
  <!--        <table class="table-striped">-->
  <!--          <tbody>-->
  <!--            <tr v-for="rank in global_ranking_deals">-->
  <!--              <th class="text-left">{{ rank.country_name }}</th>-->
  <!--              <td class="text-right whitespace-nowrap">{{ rank.deal_size__sum.toLocaleString() }} ha</td>-->
  <!--            </tr>-->
  <!--          </tbody>-->
  <!--        </table>-->

  <!--        <b><i class="fas fa-expand-arrows-alt"></i> Top investing Countries</b>-->
  <!--        <table class="table-striped">-->
  <!--          <tbody>-->
  <!--            <tr v-for="rank in global_ranking_investors">-->
  <!--              <th class="text-left">{{ rank.country_name }}</th>-->
  <!--              <td class="text-right whitespace-nowrap">{{ rank.deal_size__sum.toLocaleString() }} ha</td>-->
  <!--            </tr>-->
  <!--          </tbody>-->
  <!--        </table>-->
  <!--      </div>-->
  <!--    </div>-->
</div>
