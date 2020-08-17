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
              <h2>Filtered Statistics</h2>
            </template>
            <b-card-text>
              <div class="row my-5">
                <div class="col-md-6">
                  <div class="data-filter form-group">
                    <label>Date range</label>
                    <div class="input-group datepicker-div">
                      <div class="input-group-prepend">
                        <select v-model="selectedDateOption" @change="updateDateRange($event)">
                          <option v-for="option in date_pre_options" :value="option.value">
                            {{ option.name }}
                          </option>
                        </select>
                      </div>
                      <v-date-picker
                        mode="range"
                        v-model="daterange"
                        :max-date="new Date()"
                        @input="updateStats"
                        :input-props="{ style: 'width: 100%' }"
                      />
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <LocationFilter :regions="regions" :countries="countries"
                                  :selected-region="selectedRegion"
                                  :selected-country="selectedCountry"
                                  @updateRegion="updateRegion"
                                  @updateCountry="updateCountry"
                  ></LocationFilter>
                </div>
              </div>
              <StatisticsTable
                :deal_statistics="historic_deal_statistics"
                :investor_statistics="historic_investor_statistics"
                :countries="countries"
              >
              </StatisticsTable>
            </b-card-text>
          </b-tab>
          <b-tab>
            <template v-slot:title>
              <h2>Goals</h2>
            </template>
            <b-card-text>
              <div class="row my-5">
                <div class="col-md-6">
                  <LocationFilter :regions="regions" :countries="countries"
                                  :selected-region="selectedRegion"
                                  :selected-country="selectedCountry"
                                  @updateRegion="updateRegion"
                                  @updateCountry="updateCountry"
                  ></LocationFilter>
                </div>
              </div>
              <GoalsTable :goal_statistics="goal_statistics"></GoalsTable>
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
import {mapState} from "vuex";
import StatisticsTable from "./Statistics/StatisticsTable.vue";
import GoalsTable from "./Statistics/GoalsTable.vue";
import LocationFilter from "./Statistics/LocationFilter.vue";

function uniq(a, keepLatest = false) {
  if (keepLatest) {
    a.sort((a, b) => {
      return a.modified_at > b.modified_at ? -1 : a.modified_at < b.modified_at ? 1 : 0;
    });
  }
  let seen = new Set();
  return a.filter(item => {
    let k = item.id;
    return seen.has(k) ? false : seen.add(k);
  });
}

function uniqByKeepLatest(a) {
  return uniq(a, true);
}

function isPublicDeal(deal) {
  if (!deal.country || deal.country.high_income) return false;
  if (!deal.datasources_count) return false;
  if (deal.cached_has_no_known_investor) return false;
  return true;
}

export default {
  name: "CaseStatistics",
  components: {LocationFilter, GoalsTable, StatisticsTable },
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
      dealFields: [
        "country",
        "deal_size",
        "status",
        "draft_status",
        "confidential",
        "created_at",
        "modified_at",
        "fully_updated_at"
      ],
      historic_investors: [],
      selectedDateOption: 30,
      date_pre_options: [
        {name: "Last 30 days", value: 30},
        {name: "Last 60 days", value: 60},
        {name: "Last 180 days", value: 180},
        {name: "Last 365 days", value: 365},
      ],
      goal_statistics: {},
    };
  },
  computed: {
    ...mapState({
      regions: (state) => {
        let world = {
          id: -1,
          name: "World",
          slug: "world"
        }
        return state.page.regions.concat([world]);
      },
      countries: (state) => state.page.countries,
      user: (state) => state.page.user,
    }),
    historic_deal_statistics() {
      let stats = [
        {
          name: "Deals added",
          deals: uniq(this.historic_deals
            .filter((d) => d.status === 1 && d.created_at == d.modified_at)
          ),
        },
        {
          name: "Deals updated",
          deals: uniq(this.historic_deals
            .filter((d) => {
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
          deals: uniqByKeepLatest(this.historic_deals)
            .filter((d) => {
                if (d.fully_updated_at) {
                  let dateFU = dayjs(d.fully_updated_at);
                  return this.daterange.start <= dateFU && dateFU <= this.daterange.end;
                }
                return false;
              }
            )
        },
        {
          name: "Deals published",
          deals: uniqByKeepLatest(this.historic_deals)
            .filter((d) => d.draft_status === null && (d.status === 2 || d.status === 3))
        },
        {
          name: "Deals pending",
          deals: uniqByKeepLatest(this.historic_deals)
            .filter((d) => d.draft_status !== null)
        },
        {
          name: "Deals rejected",
          deals: uniqByKeepLatest(this.historic_deals)
            .filter((d) => d.status === 5)
        },
        {
          name: "Deals pending deletion",
          deals: uniqByKeepLatest(this.historic_deals)
            .filter((d) => d.status === 6)
        },
        {
          name: "Deals active, but not public",
          deals: uniqByKeepLatest(this.historic_deals)
            .filter((d) => {
              // only consider deals that are "live/updated"
              if (!(d.status === 2 || d.status === 3)) return false;
              if (d.confidential) return true;
              if (!isPublicDeal(d)) return true;
              return false;
            })
        },
        {
          name: "Deals active, but confidential",
          deals: uniqByKeepLatest(this.historic_deals)
            .filter((d) => {
              if (!(d.status === 2 || d.status === 3)) return false;
              return !!d.confidential;
            })
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
          investors: uniq(this.historic_investors
            .filter((d) => d.status === 1 && d.created_at == d.modified_at)
          ),
        },
        {
          name: "Investors updated",
          investors: uniq(this.historic_investors
            .filter((d) => {
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
          investors: uniqByKeepLatest(this.historic_investors)
            .filter((d) => d.draft_status === null && (d.status === 2 || d.status === 3))
        },
        {
          name: "Investors pending",
          investors: uniqByKeepLatest(this.historic_investors)
            .filter((d) => d.draft_status !== null)
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
      this.updateStats("region");
    },
    updateCountry(country) {
      this.selectedCountry = country;
      this.updateStats("country");
    },
    triggerUserRegion() {
      if (this.user.userregionalinfo) {
        let uri = this.user.userregionalinfo;
        if (uri.region) {
          this.selectedRegion = uri.region[0];
          this.updateStats();
        }
        if (uri.country) {
          this.selectedCountry = uri.country[0];
          this.updateStats();
        }
      }
    },
    updateDateRange() {
      this.daterange = {
        start: dayjs().subtract(this.selectedDateOption, "day").toDate(),
        end: new Date(),
      };
      this.updateStats();
    },

    updateStats(triggerfield) {
      if (triggerfield === "country") this.selectedRegion = null;
      if (triggerfield === "region") this.selectedCountry = null;

      if (!this.user) return;
      if (this.loading) return;
      this.loading = true;

      let dr_start = dayjs(this.daterange.start).format("YYYY-MM-DD");
      let dr_end = dayjs(this.daterange.end).format("YYYY-MM-DD");

      let filterByDealLocation = '';
      let filterByEditorLocation = '';
      if (this.selectedCountry) {
        filterByDealLocation = `country_id:${this.selectedCountry.id}`;
        filterByEditorLocation =
          `{
              field:"revision.user.userregionalinfo.country.id",
              operation:EQ,
              value:"${this.selectedCountry.id}"
           },`
      }
      if (this.selectedRegion && this.selectedRegion.id != -1) {
        filterByDealLocation = `region_id:${this.selectedRegion.id}`;
        filterByEditorLocation =
          `{
              field:"revision.user.userregionalinfo.region.id",
              operation:EQ,
              value:"${this.selectedRegion.id}"
           },`
      }
      let filterByDealLocationBracketed = '';
      if (filterByDealLocation) filterByDealLocationBracketed = `(${filterByDealLocation})`;

      const query = `query {
        deals: dealversions(filters:[
            {field:"revision.date_created",operation:GE,value:"${dr_start}"},
            {field:"revision.date_created",operation:LE,value:"${dr_end}"},
          ]
          ${filterByDealLocation}
        )
        {
          deal  {
            id
            deal_size
            fully_updated
            fully_updated_at
            status
            draft_status
            confidential
            country_id
            datasources_count
            cached_has_no_known_investor
            created_at
            modified_at
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
            id
            name
            country { id name }
            status
            draft_status
            created_at
            modified_at
          }
        }
        statistics${filterByDealLocationBracketed} {
          deals_public_count
          deals_public_multi_ds_count
          deals_public_high_geo_accuracy
          deals_public_polygons
        }
      }`;


      axios
        .post("/graphql/", {query})
        .then((response) => {
          // this.historic_deals_added = response.data.data.deals_added || [];
          // this.historic_deals_updated = response.data.data.deals_updated || [];
          // this.historic_deals_fully_updated = response.data.data.deals_fully_updated || [];
          // this.historic_investors_added = response.data.data.investors_added || [];
          // this.historic_investors_updated = response.data.data.investors_updated || [];
          this.historic_deals = response.data.data.deals.map((v) => v.deal) || [];
          this.historic_investors = response.data.data.investors.map((v) => v.investor) || [];
          this.goal_statistics = response.data.data.statistics || {};
        })
        .finally(() => (this.loading = false));
    },
    percentRatio(partialValue, totalValue) {
      if (totalValue) {
        let ratio = ((100 * partialValue) / totalValue).toFixed(1);
        return `${ratio} %`;
      }
      return '';
    }
  },
  beforeRouteEnter(to, from, next) {
    next();
  },
};

//   parseTopInvestors(deal) {
//   if (!deal.top_investors) return "";
//   return deal.top_investors
//     .map((inv) => {
//       return inv.name;
//     })
//     .join("<br>");
// },
// parseIntentionOfInvestment(deal) {
//   if (!deal.intention_of_investment) return "";
//   return deal.intention_of_investment
//     .map((int) => {
//       let intention = int.value;
//       console.log(int);
//       let slug = intention; //slugify(intention, { lower: true });
//       return `<a href="/data/by-intention/${intention}/"
//                 class="toggle-tooltip intention-icon ${slug}" title=""
//                 data-original-title="${intention}"><span>${intention}</span></a>`;
//     })
//     .sort();
// },
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

.scroll-container {
  overflow: scroll;
}

.nav-tabs {
  h2, h3 {
    margin-top: 0;
    margin-bottom: 0;
  }
}

table.goals {
  th, td {
    padding: 0.3em;
  }

  th {
    text-align: center;
    white-space: nowrap;

    &.label {
      text-align: left;
    }
  }

  td {
    text-align: right;
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
