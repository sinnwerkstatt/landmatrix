<template>
  <div class="container">
    <div v-if="loading" class="loadingscreen">
      <div class="loader"></div>
    </div>
    <div>
      <b-card no-body>
        <b-tabs card>
          <b-tab active>
            <template #title>
              <h2>{{ $t("Current statistics") }}</h2>
            </template>
            <b-card-text>
              <div class="row my-3">
                <div class="col-md-6">
                  <LocationFilter
                    :countries="countries"
                    :regions="regions"
                    :selected-country="selectedCountry"
                    :selected-region="selectedRegion"
                    @updateCountry="updateCountry"
                    @updateRegion="updateRegion"
                  />
                </div>
              </div>
              <h3 class="mt-5">Quality goals</h3>
              <hr />
              <GoalsTable :goal-statistics="goal_statistics" />
              <h3 class="mt-5">Indicator listings</h3>
              <hr />
              <StatisticsTable
                :countries="countries"
                :deal_statistics="current_deal_statistics"
                :investor_statistics="current_investor_statistics"
                :selected-country="selectedCountry"
                :selected-region="selectedRegion"
              />
            </b-card-text>
          </b-tab>
          <b-tab>
            <template #title>
              <h2>{{ $t("Changes within timespan") }}</h2>
            </template>
            <b-card-text>
              <div class="row my-3">
                <div class="col-md-6">
                  <div class="data-filter form-group">
                    <label>Date range</label>
                    <div class="input-group datepicker-div">
                      <div class="input-group-prepend">
                        <select
                          v-model="selectedDateOption"
                          @change="updateDateRange($event)"
                        >
                          <option
                            v-for="option in date_pre_options"
                            :key="option.name"
                            :value="option.value"
                          >
                            {{ option.name }}
                          </option>
                        </select>
                      </div>
                      <DatePicker
                        v-model="daterange"
                        :input-props="{ style: 'width: 100%' }"
                        :max-date="new Date()"
                        mode="range"
                        @input="selectedDateOption = null"
                      />
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <LocationFilter
                    :countries="countries"
                    :regions="regions"
                    :selected-country="selectedCountry"
                    :selected-region="selectedRegion"
                    @updateCountry="updateCountry"
                    @updateRegion="updateRegion"
                  />
                </div>
              </div>

              <div class="my-5" />
              <StatisticsTable
                :countries="countries"
                :deal_statistics="historic_deal_statistics"
                :investor_statistics="historic_investor_statistics"
                :selected-country="selectedCountry"
                :selected-region="selectedRegion"
              >
              </StatisticsTable>
            </b-card-text>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script>
  import dayjs from "dayjs";
  import gql from "graphql-tag";
  import DatePicker from "v-calendar/lib/components/date-picker.umd";
  import { mapState } from "vuex";
  import GoalsTable from "./Statistics/GoalsTable.vue";
  import LocationFilter from "./Statistics/LocationFilter.vue";
  import StatisticsTable from "./Statistics/StatisticsTable.vue";

  function uniq(a, keepLatest = false) {
    if (keepLatest) {
      a.sort((a, b) => {
        return a.modified_at > b.modified_at
          ? -1
          : a.modified_at < b.modified_at
          ? 1
          : 0;
      });
    }
    let seen = new Set();
    return a.filter((item) => {
      let k = item.id;
      return seen.has(k) ? false : seen.add(k);
    });
  }

  function uniqByKeepLatest(a) {
    return uniq(a, true);
  }

  export default {
    name: "CaseStatistics",
    components: { LocationFilter, GoalsTable, StatisticsTable, DatePicker },
    data: function () {
      return {
        loading: false,
        today: dayjs().format("YYYY/MM/DD"),
        daterange: {
          start: dayjs().subtract(30, "day").toDate(),
          end: new Date(),
        },
        selectedCountry: null,
        selectedRegion: null,

        historic_deals: [],
        historic_investors: [],
        selectedDateOption: 30,
        date_pre_options: [
          { name: "Last 30 days", value: 30 },
          { name: "Last 60 days", value: 60 },
          { name: "Last 180 days", value: 180 },
          { name: "Last 365 days", value: 365 },
        ],
        goal_statistics: {},
        simple_deals: [],
        simple_investors: [],
      };
    },
    apollo: {
      goal_statistics: {
        query: gql`
          query Statistics($c_id: Int, $r_id: Int) {
            goal_statistics: statistics(country_id: $c_id, region_id: $r_id) {
              deals_public_count
              deals_public_multi_ds_count
              deals_public_high_geo_accuracy
              deals_public_polygons
            }
          }
        `,
        variables() {
          return { c_id: this.selectedCountry?.id, r_id: this.selectedRegion?.id };
        },
      },
      simple_deals: {
        query: gql`
          query simple_deals($filters: [Filter]) {
            simple_deals: deals(limit: 0, filters: $filters, subset: UNFILTERED) {
              id
              deal_size
              fully_updated
              fully_updated_at
              status
              draft_status
              confidential
              country_id
              created_at
              modified_at
              is_public
            }
          }
        `,
        variables() {
          return { filters: this.location_filters };
        },
      },
      simple_investors: {
        query: gql`
          query simple_investors($filters: [Filter]) {
            simple_investors: investors(
              limit: 0
              filters: $filters
              subset: UNFILTERED
            ) {
              id
              name
              country {
                id
                name
              }
              status
              draft_status
              created_at
              modified_at
            }
          }
        `,
        variables() {
          return { filters: this.location_filters };
        },
      },
      historic_deals: {
        query: gql`
          query historic_deals($filters: [Filter], $c_id: Int, $r_id: Int) {
            dealversions(filters: $filters, country_id: $c_id, region_id: $r_id) {
              id
              deal {
                id
                deal_size
                fully_updated
                fully_updated_at
                status
                draft_status
                confidential
                country_id
                created_at
                modified_at
              }
            }
          }
        `,
        variables() {
          let filters = [
            {
              field: "created_at",
              operation: "GE",
              value: dayjs(this.daterange.start).format("YYYY-MM-DD"),
            },
            {
              field: "created_at",
              operation: "LE",
              value: dayjs(this.daterange.end).format("YYYY-MM-DD"),
            },
          ];
          return {
            filters,
            c_id: this.selectedCountry?.id,
            r_id: this.selectedRegion?.id,
          };
        },
        update({ dealversions }) {
          return dealversions.map((v) => v.deal);
        },
      },
      historic_investors: {
        query: gql`
          query historic_investors($filters: [Filter]) {
            investorversions(filters: $filters) {
              id
              investor {
                id
                name
                country {
                  id
                  name
                }
                status
                draft_status
                created_at
                modified_at
              }
            }
          }
        `,
        variables() {
          let filters = [
            {
              field: "created_at",
              operation: "GE",
              value: dayjs(this.daterange.start).format("YYYY-MM-DD"),
            },
            {
              field: "created_at",
              operation: "LE",
              value: dayjs(this.daterange.end).format("YYYY-MM-DD"),
            },
          ];
          if (this.selectedCountry)
            filters.push({
              field: "created_by.userregionalinfo.country.id",
              operation: "EQ",
              value: this.selectedCountry.id,
            });

          if (this.selectedRegion && this.selectedRegion.id !== -1)
            filters.push({
              field: "created_by.userregionalinfo.region.id",
              operation: "EQ",
              value: this.selectedRegion.id,
            });

          return { filters };
        },
        update({ investorversions }) {
          return investorversions.map((v) => v.investor);
        },
      },
    },
    computed: {
      ...mapState({
        regions: (state) => {
          let world = {
            id: -1,
            name: "Global",
            slug: "global",
          };
          return state.page.regions.concat([world]);
        },
        countries: (state) => state.page.countries,
        user: (state) => state.page.user,
      }),
      location_filters() {
        let filters;
        if (this.selectedCountry)
          filters = [
            {
              field: "country.id",
              operation: "EQ",
              value: this.selectedCountry.id,
            },
          ];
        if (this.selectedRegion && this.selectedRegion.id !== -1)
          filters = [
            {
              field: "country.fk_region.id",
              operation: "EQ",
              value: this.selectedRegion.id,
            },
          ];
        return filters;
      },
      deals_active() {
        return this.simple_deals.filter((d) => [2, 3].includes(d.status));
      },
      deals_pending() {
        return this.simple_deals.filter((d) => [1, 2, 3].includes(d.draft_status));
      },
      deals_rejected() {
        return this.simple_deals.filter((d) => d.draft_status === 4);
      },
      deals_pending_deletion() {
        return this.simple_deals.filter((d) => d.draft_status === 5);
      },
      investors_active() {
        return this.simple_investors.filter((i) => [2, 3].includes(i.status));
      },
      investors_pending() {
        return this.simple_investors.filter((i) => [1, 2, 3].includes(i.draft_status));
      },
      investors_rejected() {
        return this.simple_investors.filter((i) => i.draft_status === 4);
      },
      investors_pending_deletion() {
        return this.simple_investors.filter((i) => i.draft_status === 5);
      },
      historic_deal_statistics() {
        let stats = [
          {
            name: "Deals added",
            deals: uniq(
              this.historic_deals.filter(
                (d) => d.status === 1 && d.created_at === d.modified_at
              )
            ),
          },
          {
            name: "Deals updated",
            deals: uniq(
              this.historic_deals.filter((d) => {
                // not added deals
                if (d.status === 1 && d.created_at === d.modified_at) return false;
                // not deleted deals
                if (d.status === 4) return false;
                // finally
                return true;
              })
            ),
          },
          {
            name: "Deals Fully Updated",
            deals: uniqByKeepLatest(this.historic_deals).filter((d) => {
              if (d.fully_updated_at) {
                let dateFU = dayjs(d.fully_updated_at);
                return this.daterange.start <= dateFU && dateFU <= this.daterange.end;
              }
              return false;
            }),
          },
          {
            name: "Deals approved",
            deals: uniqByKeepLatest(this.historic_deals).filter(
              (d) => d.draft_status === null && (d.status === 2 || d.status === 3)
            ),
          },
        ];
        for (let stat of stats) {
          stat.value = stat.deals.length;
        }
        return stats;
      },
      current_deal_statistics() {
        let stats = [
          { name: "Deals pending", deals: this.deals_pending },
          { name: "Deals rejected", deals: this.deals_rejected },
          { name: "Deals pending deletion", deals: this.deals_pending_deletion },
          { name: "Deals active", deals: this.deals_active },
          {
            name: "Deals active, but not public",
            deals: this.deals_active.filter((d) => !d.is_public),
          },
          {
            name: "Deals active, but confidential",
            deals: this.deals_active.filter((d) => d.confidential),
          },
        ];
        for (let stat of stats) {
          stat.value = stat.deals.length;
        }
        return stats;
      },
      historic_investor_statistics() {
        let stats = [
          {
            name: "Investors added",
            investors: uniq(
              this.historic_investors.filter(
                (d) => d.status === 1 && d.created_at === d.modified_at
              )
            ),
          },
          {
            name: "Investors updated",
            investors: uniq(
              this.historic_investors.filter((d) => {
                // not added deals
                if (d.status === 1 && d.created_at === d.modified_at) return false;
                // not deleted deals
                if (d.status === 4) return false;
                // finally
                return true;
              })
            ),
          },
          {
            name: "Investors published",
            investors: uniqByKeepLatest(this.historic_investors).filter(
              (d) => d.draft_status === null && (d.status === 2 || d.status === 3)
            ),
          },
        ];
        for (let stat of stats) {
          stat.value = stat.investors.length;
        }
        return stats;
      },
      current_investor_statistics() {
        let stats = [
          {
            name: "Investors pending",
            investors: this.investors_pending,
          },
          {
            name: "Investors rejected",
            investors: this.investors_rejected,
          },
          {
            name: "Investors pending deletion",
            investors: this.investors_pending_deletion,
          },
          {
            name: "Investors active",
            investors: this.investors_active,
          },
        ];
        for (let stat of stats) {
          stat.value = stat.investors.length;
        }
        return stats;
      },
    },
    watch: {
      user() {
        this.triggerUserRegion();
      },
    },
    methods: {
      updateRegion(region) {
        this.selectedRegion = region;
        this.selectedCountry = null;
      },
      updateCountry(country) {
        this.selectedCountry = country;
        this.selectedRegion = null;
      },
      triggerUserRegion() {
        if (this.user.userregionalinfo) {
          let uri = this.user.userregionalinfo;
          if (uri.region.length) {
            this.selectedRegion = this.regions.find((r) => r.id === uri.region[0].id);
          }
          if (uri.country.length) {
            this.selectedCountry = this.countries.find(
              (c) => c.id === uri.country[0].id
            );
          }
        }
      },
      updateDateRange() {
        this.daterange = {
          start: dayjs().subtract(this.selectedDateOption, "day").toDate(),
          end: new Date(),
        };
      },
    },
  };
</script>

<style lang="scss" scoped>
  .input-group {
    width: 100%;
  }

  .datepicker-div > span {
    width: 60%;
    max-width: 100%;
  }

  .multiselect-div {
    width: 50%;
    padding-right: 5px;

    .multiselect {
      width: 100%;
    }
  }

  .actions {
    margin-bottom: 1em;
    text-align: right;

    > div {
      display: inline-block;
    }
  }

  .nav-tabs {
    h2,
    h3 {
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  .loadingscreen {
    position: fixed;

    .loader {
      margin-top: calc(50vh - 100px);
    }
  }
</style>

<style lang="scss">
  .nav-link.active.teal-background {
    background: var(--color-lm-investor) !important;
  }

  .tab-content {
    overflow: hidden;
  }
</style>
