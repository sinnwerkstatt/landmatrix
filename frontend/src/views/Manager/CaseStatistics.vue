<template>
  <div class="container">
    <LoadingPulse v-if="$apollo.loading" />
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
                :deal-statistics="current_deal_statistics"
                :investor-statistics="current_investor_statistics"
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
                        <select v-model="selectedDateOption" @change="updateDateRange">
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
                        :max-date="new Date()"
                        mode="date"
                        is-range
                        :first-day-of-week="2"
                        :masks="{ input: 'YYYY-MM-DD' }"
                        @input="selectedDateOption = null"
                      >
                        <template #default="{ inputValue, inputEvents, isDragging }">
                          <div
                            class="flex flex-col sm:flex-row justify-start items-center"
                          >
                            <div class="relative flex-grow">
                              <CalendarIcon
                                cls="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                              />
                              <input
                                class="flex-grow !pl-6 pr-2 py-1 bg-gray-100 border rounded w-full"
                                :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                                :value="inputValue.start"
                                v-on="inputEvents.start"
                              />
                            </div>
                            <div class="relative flex-grow">
                              <CalendarIcon
                                cls="text-gray-600 w-4 h-full mx-2 absolute pointer-events-none"
                              />
                              <input
                                class="flex-grow !pl-6 pr-2 py-1 bg-gray-100 border rounded w-full"
                                :class="isDragging ? 'text-gray-600' : 'text-gray-900'"
                                :value="inputValue.end"
                                v-on="inputEvents.end"
                              />
                            </div>
                          </div>
                        </template>
                      </DatePicker>
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
                :deal-statistics="historic_deal_statistics"
                :investor-statistics="historic_investor_statistics"
                :selected-country="selectedCountry"
                :selected-region="selectedRegion"
              />
            </b-card-text>
          </b-tab>
        </b-tabs>
      </b-card>
    </div>
  </div>
</template>

<script lang="ts">
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import CalendarIcon from "$components/icons/Calendar.vue";
  import type { Deal, DealVersion } from "$types/deal";
  import type { GQLFilter } from "$types/filters";
  import type { Investor } from "$types/investor";
  import type { User } from "$types/user";
  import type { Country, Region } from "$types/wagtail";
  import GoalsTable from "./Statistics/GoalsTable.vue";
  import LocationFilter from "./Statistics/LocationFilter.vue";
  import StatisticsTable from "./Statistics/StatisticsTable.vue";
  import dayjs from "dayjs";
  import isSameOrAfter from "dayjs/plugin/isSameOrAfter";
  import isSameOrBefore from "dayjs/plugin/isSameOrBefore";
  import gql from "graphql-tag";
  // @ts-ignore
  import DatePicker from "v-calendar/lib/components/date-picker.umd";
  import Vue from "vue";

  dayjs.extend(isSameOrBefore);
  dayjs.extend(isSameOrAfter);

  function uniq<S extends Deal | Investor>(
    objs: Array<S>,
    keepLatest = false
  ): Array<S> {
    if (keepLatest) {
      objs.sort((a, b) => {
        if (a.modified_at > b.modified_at) return -1;
        if (a.modified_at < b.modified_at) return 1;
        return 0;
      });
    }
    let seen = new Set();
    return objs.filter((item) => {
      let k = item.id;
      return seen.has(k) ? false : seen.add(k);
    });
  }

  export type Stat<S> = {
    name: string;
    objs: S[];
    value: number;
  };

  export default Vue.extend({
    name: "CaseStatistics",
    components: {
      CalendarIcon,
      LoadingPulse,
      LocationFilter,
      GoalsTable,
      StatisticsTable,
      DatePicker,
    },
    data: function () {
      return {
        today: dayjs().format("YYYY/MM/DD"),
        daterange: {
          start: dayjs().subtract(30, "day").toDate(),
          end: new Date(),
        },
        selectedCountry: null as Country | null,
        selectedRegion: null as Region | null,

        historic_deals: [] as Deal[],
        historic_investors: [] as Investor[],
        selectedDateOption: 30,
        date_pre_options: [
          { name: "Last 30 days", value: 30 },
          { name: "Last 60 days", value: 60 },
          { name: "Last 180 days", value: 180 },
          { name: "Last 365 days", value: 365 },
        ],
        goal_statistics: {},
        simple_deals: [] as Deal[],
        simple_investors: [] as Investor[],
      };
    },
    apollo: {
      goal_statistics: {
        query: gql`
          query ($c_id: Int, $r_id: Int) {
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
              country {
                id
              }
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
                status
                draft_status
                confidential
                country_id
                country {
                  id
                }
                created_at
                modified_at
                fully_updated
                fully_updated_at
              }
            }
          }
        `,
        variables() {
          return {
            filters: [
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
            ],
            c_id: this.selectedCountry?.id,
            r_id: this.selectedRegion?.id,
          };
        },
        update({ dealversions }) {
          return dealversions.map((v: DealVersion) => v.deal);
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
              field: "created_by.country.id",
              operation: "EQ",
              value: this.selectedCountry.id,
            });

          if (this.selectedRegion && this.selectedRegion.id !== -1)
            filters.push({
              field: "created_by.region.id",
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
      regions(): Region[] {
        let world = {
          id: -1,
          name: "Global",
          slug: "global",
        };
        return [...this.$store.state.regions, world];
      },
      countries(): Country[] {
        return this.$store.state.countries;
      },
      user(): User {
        return this.$store.state.user;
      },
      location_filters(): GQLFilter[] {
        if (this.selectedCountry)
          return [
            {
              field: "country.id",
              operation: "EQ",
              value: this.selectedCountry.id,
            },
          ];
        if (this.selectedRegion && this.selectedRegion.id !== -1)
          return [
            {
              field: "country.region.id",
              operation: "EQ",
              value: this.selectedRegion.id,
            },
          ];
        return [];
      },
      // simple_deals_with_combi(): Deal[] {
      //   return this.simple_deals.map((o: Deal) => ({
      //       ...o,
      //       combined_status: [o.status, o.draft_status],
      //     }));
      // },
      deals_active(): Deal[] {
        return this.simple_deals.filter((d) => [2, 3].includes(d.status));
      },
      deals_pending(): Deal[] {
        return this.simple_deals.filter(
          (d) => d.draft_status && [1, 2, 3].includes(d.draft_status)
        );
      },
      deals_rejected(): Deal[] {
        return this.simple_deals.filter((d) => d.draft_status === 4);
      },
      deals_pending_deletion(): Deal[] {
        return this.simple_deals.filter((d) => d.draft_status === 5);
      },
      investors_active(): Investor[] {
        return this.simple_investors.filter((i) => [2, 3].includes(i.status));
      },
      investors_pending(): Investor[] {
        return this.simple_investors.filter(
          (i) => i.draft_status && [1, 2, 3].includes(i.draft_status)
        );
      },
      investors_rejected(): Investor[] {
        return this.simple_investors.filter((i) => i.draft_status === 4);
      },
      investors_pending_deletion(): Investor[] {
        return this.simple_investors.filter((i) => i.draft_status === 5);
      },
      historic_deal_statistics(): Stat<Deal>[] {
        const stats = [
          {
            name: "Deals added",
            objs: uniq(
              this.historic_deals.filter((d: Deal) => {
                let dateCreated = dayjs(d.created_at);
                return (
                  [2, 3].includes(d.status) &&
                  dateCreated.isSameOrAfter(this.daterange.start, "day") &&
                  dateCreated.isSameOrBefore(this.daterange.end, "day")
                );
              })
            ),
          },
          {
            name: "Deals updated",
            objs: uniq(this.historic_deals.filter((d: Deal) => d.status === 3)),
          },
          {
            name: "Deals fully updated",
            objs: uniq(this.historic_deals, true).filter((d: Deal) => {
              if (!d.fully_updated_at) return false;
              let dateFU = dayjs(d.fully_updated_at);
              return (
                (d.status === 3 || d.status === 2) &&
                dateFU.isSameOrAfter(this.daterange.start, "day") &&
                dateFU.isSameOrBefore(this.daterange.end, "day")
              );
            }),
          },
          {
            name: "Deals activated",
            objs: uniq(this.historic_deals, true).filter((d: Deal) => {
              return d.draft_status === null && (d.status === 2 || d.status === 3);
            }),
          },
        ];
        for (let stat of stats as Stat<Deal>[]) {
          stat.value = stat.objs.length;
        }
        return stats as Stat<Deal>[];
      },
      current_deal_statistics(): Stat<Deal>[] {
        let stats = [
          { name: "Deals pending", objs: this.deals_pending },
          { name: "Deals rejected", objs: this.deals_rejected },
          { name: "Deals pending deletion", objs: this.deals_pending_deletion },
          { name: "Deals active", objs: this.deals_active },
          {
            name: "Deals active, but not public",
            objs: this.deals_active.filter((d) => !d.is_public),
          },
          {
            name: "Deals active, but confidential",
            objs: this.deals_active.filter((d) => d.confidential),
          },
        ];
        for (let stat of stats as Stat<Deal>[]) {
          stat.value = stat.objs.length;
        }
        return stats as Stat<Deal>[];
      },
      historic_investor_statistics(): Stat<Investor>[] {
        const stats = [
          {
            name: "Investors added",
            objs: uniq(
              this.historic_investors.filter(
                (o) => o.status === 1 && o.created_at === o.modified_at
              )
            ),
          },
          {
            name: "Investors updated",
            objs: uniq(
              this.historic_investors.filter((o: Investor) => {
                // not added investors
                if (o.status === 1 && o.created_at === o.modified_at) return false;
                // not deleted investors
                if (o.status === 4) return false;
                // finally
                return true;
              })
            ),
          },
          {
            name: "Investors published",
            objs: uniq(this.historic_investors, true).filter(
              (d) => d.draft_status === null && (d.status === 2 || d.status === 3)
            ),
          },
        ];
        for (let stat of stats as Stat<Investor>[]) {
          stat.value = stat.objs.length;
        }
        return stats as Stat<Investor>[];
      },
      current_investor_statistics(): Stat<Investor>[] {
        const stats = [
          {
            name: "Investors pending",
            objs: this.investors_pending,
          },
          {
            name: "Investors rejected",
            objs: this.investors_rejected,
          },
          {
            name: "Investors pending deletion",
            objs: this.investors_pending_deletion,
          },
          {
            name: "Investors active",
            objs: this.investors_active,
          },
        ];
        for (let stat of stats as Stat<Investor>[]) {
          stat.value = stat.objs.length;
        }
        return stats as Stat<Investor>[];
      },
    },
    watch: {
      user(): void {
        this.triggerUserRegion();
      },
    },
    methods: {
      updateRegion(region: Region): void {
        this.selectedRegion = region;
        this.selectedCountry = null;
      },
      updateCountry(country: Country): void {
        this.selectedCountry = country;
        this.selectedRegion = null;
      },
      triggerUserRegion(): void {
        if (this.user.region) {
          this.selectedRegion =
            this.regions.find((r) => r.id === this.user.region.id) || null;
        }
        if (this.user.country) {
          this.selectedCountry =
            this.countries.find((c) => c.id === this.user.country.id) || null;
        }
      },
      updateDateRange(): void {
        this.daterange = {
          start: dayjs().subtract(this.selectedDateOption, "day").toDate(),
          end: new Date(),
        };
      },
    },
  });
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
