<template>
  <div class="container">
    <div class="loadingscreen" v-if="loading">
      <div class="loader"></div>
    </div>
    <div>
      <b-card no-body>
        <b-tabs card>
          <b-tab active>
            <template v-slot:title>
              <h2>{{ $t("Current statistics") }}</h2>
            </template>
            <b-card-text>
              <div class="row my-3">
                <div class="col-md-6">
                  <LocationFilter
                    :regions="regions"
                    :countries="countries"
                    :selected-region="selectedRegion"
                    :selected-country="selectedCountry"
                    @updateRegion="updateRegion"
                    @updateCountry="updateCountry"
                  ></LocationFilter>
                </div>
              </div>
              <div class="row">
                <div class="col-3">
                  <button class="btn btn-primary" @click="updateStats()">Update</button>
                </div>
              </div>
              <h3 class="mt-5">Quality goals</h3>
              <hr />
              <GoalsTable :goal_statistics="goal_statistics"></GoalsTable>
              <h3 class="mt-5">Indicator listings</h3>
              <hr />
              <StatisticsTable
                :deal_statistics="current_deal_statistics"
                :investor_statistics="current_investor_statistics"
                :countries="countries"
                :selected-region="selectedRegion"
                :selected-country="selectedCountry"
              ></StatisticsTable>
            </b-card-text>
          </b-tab>
          <b-tab>
            <template v-slot:title>
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
                            :value="option.value"
                          >
                            {{ option.name }}
                          </option>
                        </select>
                      </div>
                      <v-date-picker
                        mode="range"
                        v-model="daterange"
                        :max-date="new Date()"
                        @input="selectedDateOption = null"
                        :input-props="{ style: 'width: 100%' }"
                      />
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <LocationFilter
                    :regions="regions"
                    :countries="countries"
                    :selected-region="selectedRegion"
                    :selected-country="selectedCountry"
                    @updateRegion="updateRegion"
                    @updateCountry="updateCountry"
                  ></LocationFilter>
                </div>
              </div>
              <div class="row">
                <div class="col-3">
                  <button class="btn btn-primary" @click="updateStats()">Update</button>
                </div>
              </div>
              <div class="my-5" />
              <StatisticsTable
                :deal_statistics="historic_deal_statistics"
                :investor_statistics="historic_investor_statistics"
                :countries="countries"
                :selected-region="selectedRegion"
                :selected-country="selectedCountry"
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
  import axios from "axios";
  import dayjs from "dayjs";
  import { mapState } from "vuex";
  import StatisticsTable from "./Statistics/StatisticsTable.vue";
  import GoalsTable from "./Statistics/GoalsTable.vue";
  import LocationFilter from "./Statistics/LocationFilter.vue";

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

  function isPublicDeal(deal) {
    if (deal.confidential) return false;
    if (!deal.country || deal.country.high_income) return false;
    if (!deal.datasources.length) return false;
    if (deal.has_no_known_investor) return false;
    return true;
  }

  const DEAL_QUERY_FIELDS = `id
                deal_size
                fully_updated
                fully_updated_at
                status
                draft_status
                confidential
                country_id
                created_at
                modified_at
`;

  const INVESTOR_QUERY_FIELDS = `id
            name
            country { id name }
            status
            draft_status
            created_at
            modified_at
`;

  export default {
    name: "CaseStatistics",
    components: { LocationFilter, GoalsTable, StatisticsTable },
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
        deals_pending: [],
        deals_rejected: [],
        deals_pending_deletion: [],
        deals_active: [],
        historic_investors: [],
        investors_pending: [],
        investors_rejected: [],
        investors_pending_deletion: [],
        investors_active: [],

        selectedDateOption: 30,
        date_pre_options: [
          { name: "Last 30 days", value: 30 },
          { name: "Last 60 days", value: 60 },
          { name: "Last 180 days", value: 180 },
          { name: "Last 365 days", value: 365 },
        ],
        goal_statistics: {},
      };
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
      historic_deal_statistics() {
        let stats = [
          {
            name: "Deals added",
            deals: uniq(
              this.historic_deals.filter(
                (d) => d.status === 1 && d.created_at == d.modified_at
              )
            ),
          },
          {
            name: "Deals updated",
            deals: uniq(
              this.historic_deals.filter((d) => {
                // not added deals
                if (d.status === 1 && d.created_at == d.modified_at) return false;
                // not deleted deals
                if (d.status === 4) return false;
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
          {
            name: "Deals pending",
            deals: this.deals_pending,
          },
          {
            name: "Deals rejected",
            deals: this.deals_rejected,
          },
          {
            name: "Deals pending deletion",
            deals: this.deals_pending_deletion,
          },
          {
            name: "Deals active",
            deals: this.deals_active,
          },
          {
            name: "Deals active, but not public",
            deals: this.deals_active.filter((d) => !isPublicDeal(d)),
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
                (d) => d.status === 1 && d.created_at == d.modified_at
              )
            ),
          },
          {
            name: "Investors updated",
            investors: uniq(
              this.historic_investors.filter((d) => {
                // not added deals
                if (d.status === 1 && d.created_at == d.modified_at) return false;
                // not deleted deals
                if (d.status === 4) return false;
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
            this.selectedRegion = this.regions.find((r) => r.id == uri.region[0].id);
            this.updateStats();
          }
          if (uri.country.length) {
            this.selectedCountry = this.countries.find(
              (c) => c.id == uri.country[0].id
            );
            this.updateStats();
          }
        }
      },
      updateDateRange() {
        this.daterange = {
          start: dayjs().subtract(this.selectedDateOption, "day").toDate(),
          end: new Date(),
        };
      },
      updateStats() {
        if (!this.user) return;
        if (this.loading) return;
        this.loading = true;

        let dr_start = dayjs(this.daterange.start).format("YYYY-MM-DD");
        let dr_end = dayjs(this.daterange.end).format("YYYY-MM-DD");

        let filterLocation = "";
        let filterByDealLocation = "";
        let filterByEditorLocation = "";
        if (this.selectedCountry) {
          filterLocation = `{
              field:"country.id",
              operation:EQ,
              value:"${this.selectedCountry.id}"
           }`;
          filterByDealLocation = `country_id:${this.selectedCountry.id}`;
          filterByEditorLocation = `{
              field:"revision.user.userregionalinfo.country.id",
              operation:EQ,
              value:"${this.selectedCountry.id}"
           },`;
        }
        if (this.selectedRegion && this.selectedRegion.id != -1) {
          filterLocation = `{
              field:"country.fk_region.id",
              operation:EQ,
              value:"${this.selectedRegion.id}"
           }`;
          filterByDealLocation = `region_id:${this.selectedRegion.id}`;
          filterByEditorLocation = `{
              field:"revision.user.userregionalinfo.region.id",
              operation:EQ,
              value:"${this.selectedRegion.id}"
           },`;
        }
        let filterByDealLocationBracketed = "";
        if (filterByDealLocation)
          filterByDealLocationBracketed = `(${filterByDealLocation})`;

        const query = `query {
        deals: dealversions(filters:[
            {field:"revision.date_created",operation:GE,value:"${dr_start}"},
            {field:"revision.date_created",operation:LE,value:"${dr_end}"},
          ]
          ${filterByDealLocation}
        )
        {
          deal  {
            ${DEAL_QUERY_FIELDS}
          }
        }
        investors: investorversions(filters:[
            {field:"revision.date_created",operation:GE,value:"${dr_start}"},
            {field:"revision.date_created",operation:LE,value:"${dr_end}"},
            ${filterByEditorLocation}
          ]
        )
        {
          investor {
            ${INVESTOR_QUERY_FIELDS}
          }
        }
        statistics${filterByDealLocationBracketed} {
          deals_public_count
          deals_public_multi_ds_count
          deals_public_high_geo_accuracy
          deals_public_polygons
        }
        deals_pending: deals(limit:0, filters:[
          {field:"draft_status",operation:IN,value:["1","2","3"]},
          ${filterLocation}
        ], public:false) {
          ${DEAL_QUERY_FIELDS}
        }
        deals_rejected: deals(limit:0, filters:[
          {field:"status",operation:EQ,value:"5"},
          ${filterLocation}
        ], public:false) {
          ${DEAL_QUERY_FIELDS}
        }
        deals_pending_deletion: deals(limit:0, filters:[
          {field:"status",operation:EQ,value:"6"},
          ${filterLocation}
        ], public:false) {
          ${DEAL_QUERY_FIELDS}
        }
        deals_active: deals(limit:0, filters:[
          {field:"status",operation:IN,value:["2","3"]},
          ${filterLocation}
        ], public:false) {
          ${DEAL_QUERY_FIELDS}
          country {
            id
            high_income
          }
          datasources {
            id
          }
          has_no_known_investor
        }
        investors_pending: investors(limit:0, filters:[
          {field:"draft_status",operation:IN,value:["1","2","3"]},
          ${filterLocation}
        ]) {
          ${INVESTOR_QUERY_FIELDS}
        }
        investors_rejected: investors(limit:0, filters:[
          {field:"status",operation:EQ,value:"5"},
          ${filterLocation}
        ]) {
          ${INVESTOR_QUERY_FIELDS}
        }
        investors_pending_deletion: investors(limit:0, filters:[
          {field:"status",operation:EQ,value:"6"},
          ${filterLocation}
        ]) {
          ${INVESTOR_QUERY_FIELDS}
        }
        investors_active: investors(limit:0, filters:[
          {field:"status",operation:IN,value:["2","3"]},
          ${filterLocation}
        ]) {
          ${INVESTOR_QUERY_FIELDS}
        }
      }`;

        axios
          .post("/graphql/", { query })
          .then((response) => {
            // this.historic_deals_added = response.data.data.deals_added || [];
            // this.historic_deals_updated = response.data.data.deals_updated || [];
            // this.historic_deals_fully_updated = response.data.data.deals_fully_updated || [];
            // this.historic_investors_added = response.data.data.investors_added || [];
            // this.historic_investors_updated = response.data.data.investors_updated || [];
            this.historic_deals = response.data.data.deals.map((v) => v.deal) || [];
            this.historic_investors =
              response.data.data.investors.map((v) => v.investor) || [];
            this.goal_statistics = response.data.data.statistics || {};
            this.deals_pending = response.data.data.deals_pending || [];
            this.deals_rejected = response.data.data.deals_rejected || [];
            this.deals_pending_deletion =
              response.data.data.deals_pending_deletion || [];
            this.deals_active = response.data.data.deals_active || [];
            this.investors_pending = response.data.data.investors_pending || [];
            this.investors_rejected = response.data.data.investors_rejected || [];
            this.investors_pending_deletion =
              response.data.data.investors_pending_deletion || [];
            this.investors_active = response.data.data.investors_active || [];
          })
          .finally(() => (this.loading = false));
      },
    },
    beforeRouteEnter(to, from, next) {
      next();
    },
  };
</script>

<style scoped lang="scss">
  @import "../../scss/colors";

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
  @import "../../scss/colors";

  .nav-link.active.teal-background {
    background: $lm_investor !important;
  }

  .tab-content {
    overflow: hidden;
  }
</style>
