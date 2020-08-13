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
                  <div class="form-group">
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
                  <div class="form-group">
                    <label>Country/Region</label>
                    <div class="input-group">
                      <div class="multiselect-div">
                        <multiselect
                          v-model="selectedRegion"
                          :options="regions"
                          label="name"
                          placeholder="Region"
                          @input="updateStats('region')"
                        />
                      </div>
                      <div class="multiselect-div">
                        <multiselect
                          v-model="selectedCountry"
                          :options="countries"
                          label="name"
                          placeholder="Country"
                          @input="updateStats('country')"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="actions">
                <DownloadJsonCSV v-if="formFilled" :data="allStatsCsv" :name="allStatsCsvFileName">
                  <a class="btn btn-outline-primary">Download all indicators as CSV</a>
                </DownloadJsonCSV>
              </div>
              <div class="number-of-deals">
                <b-tabs>
                  <b-tab>
                    <template v-slot:title>
                      <h3>Deals</h3>
                    </template>

                    <b-tabs pills card vertical nav-wrapper-class="col-lg-3 col-md-12" content-class="col-lg-9 col-md-12">
                      <b-tab v-for="(stats, i) in deal_statistics" :key="i">
                        <template v-slot:title>
                          <strong>{{ stats.value }}</strong> {{ stats.name }}<br/>
                        </template>
                        <b-card-text>
                          <div class="actions">
                            <DownloadJsonCSV v-if="prepareDealsCsv(stats.deals).length" :data="prepareDealsCsv(stats.deals)"
                                             :name="`Indicator-List_${stats.name}.csv`">
                              <a class="btn btn-outline-primary">Download deals as CSV</a>
                            </DownloadJsonCSV>
                          </div>
                          <div class="scroll-container">
                            <DealTable
                              :deals="prepareDeals(stats.deals)"
                              :fields="dealFields"
                              :pageSize="10"
                            />
                          </div>
                        </b-card-text>
                      </b-tab>
                    </b-tabs>
                  </b-tab>
                  <b-tab>
                    <template v-slot:title>
                      <h3>Investors</h3>
                    </template>

                    <b-tabs pills card vertical nav-wrapper-class="col-lg-3 col-md-12" content-class="col-lg-9 col-md-12">
                      <b-tab v-for="(stats, i) in investor_statistics" :key="i">
                        <template v-slot:title>
                          <strong>{{ stats.value }}</strong> {{ stats.name }}<br/>
                        </template>
                        <b-card-text>
                          <div class="actions">
                            <DownloadJsonCSV v-if="prepareInvestors(stats.investors).length" :data="prepareInvestors(stats.investors)"
                              :name="`Indicator-List_${stats.name}.csv`">
                              <a class="btn btn-outline-primary">Download investors as CSV</a>
                            </DownloadJsonCSV>
                          </div>
                          <div class="scroll-container">
                            <InvestorTable
                              :investors="prepareInvestors(stats.investors)"
                              :fields="investorFields"
                              :pageSize="10"
                            />
                          </div>
                        </b-card-text>
                      </b-tab>
                    </b-tabs>
                  </b-tab>
                </b-tabs>
              </div>
            </b-card-text>
          </b-tab>
          <b-tab>
            <template v-slot:title>
              <h2>Goals</h2>
            </template>
            <b-card-text>
              <div class="row my-5">
                <div class="col-md-6">
                  <div class="form-group">
                    <label>Country/Region</label>
                    <div class="input-group">
                      <div class="multiselect-div">
                        <multiselect
                          v-model="selectedRegion"
                          :options="regions"
                          label="name"
                          placeholder="Region"
                          @input="selectedCountry=null"
                        />
                      </div>
                      <div class="multiselect-div">
                        <multiselect
                          v-model="selectedCountry"
                          :options="countries"
                          label="name"
                          placeholder="Country"
                          @input="selectedRegion=null"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <ul>
                <li><b>{{ goal_statistics.deals_public_count }}</b> # publicly visible deals (published, public filter ok, 'not public' not set)</li>
                <li># publicly visible deals, with default filter</li>
                <li><b>{{ goal_statistics.deals_public_multi_ds_count }}</b># deals with with multiple data sources</li>
                <li># deals with with multiple data sources, with default filter</li>
                <li><b>{{ goal_statistics.deals_public_high_geo_accuracy }}</b># deals georeferenced with high accuracy*</li>
                <li># deals georeferenced with high accuracy, with default filter</li>
                <li><b>{{ goal_statistics.deals_public_polygons }}</b># deals with polygon data</li>
                <li># deals with polygon data, with default filter</li>
              </ul>
              <p>* Deals with at least one location with either accuracy level 'Coordinates' or 'Exact location' or at least one polygon.</p>
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
import DealTable from "/components/Deal/DealTable";
import {mapState} from "vuex";
import InvestorTable from "/components/Investor/InvestorTable";
import DownloadJsonCSV from 'vue-json-csv';

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
  if (!deal.datasources.length) return false;
  // if (!deal.operating_company || deal.operating_company.is_actually_unknown) return false;
  // TODO: The parent company unknown filter is still missing here;
  return true;
}

export default {
  name: "CaseStatistics",
  components: {InvestorTable, DealTable, DownloadJsonCSV},
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

      deals: [],
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
      investors: [],
      investorFields: [
        "name",
        "country",
        "status",
        "created_at",
        "modified_at"
      ],

      selectedDateOption: 30,
      date_pre_options: [
        {name: "Last 30 days", value: 30},
        {name: "Last 60 days", value: 60},
        {name: "Last 180 days", value: 180},
        {name: "Last 365 days", value: 365},
      ],
      goal_statistics: {
        deals_public_count: 0,
        deals_public_multi_ds_count: 0,
      },
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
    formFilled() {
      return this.selectedCountry || this.selectedRegion;
    },
    filtered_deals() {
      if (this.selectedCountry)
        return this.deals.filter((d) => {
          return d.country && d.country.id === this.selectedCountry.id;
        });
      if (this.selectedRegion && this.selectedRegion.id != -1)
        return this.deals.filter((d) => {
          return d.country && d.country.region.id === this.selectedRegion.id;
        });
      return this.deals;
    },
    public_deals() {

    },
    deal_statistics() {
      let stats = [
        {
          name: "Deals added",
          deals: uniq(this.filtered_deals
            .filter((d) => d.status === 1 && d.created_at == d.modified_at)
          ),
        },
        {
          name: "Deals updated",
          deals: uniq(this.filtered_deals
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
          deals: uniqByKeepLatest(this.filtered_deals)
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
          deals: uniqByKeepLatest(this.filtered_deals)
            .filter((d) => d.draft_status === null && (d.status === 2 || d.status === 3))
        },
        {
          name: "Deals pending",
          deals: uniqByKeepLatest(this.filtered_deals)
            .filter((d) => d.draft_status !== null)
        },
        {
          name: "Deals rejected",
          deals: uniqByKeepLatest(this.filtered_deals)
            .filter((d) => d.status === 5)
        },
        {
          name: "Deals pending deletion",
          deals: uniqByKeepLatest(this.filtered_deals)
            .filter((d) => d.status === 6)
        },
        {
          name: "Deals active, but not public",
          deals: uniqByKeepLatest(this.filtered_deals)
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
          deals: uniqByKeepLatest(this.filtered_deals)
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
    investor_statistics() {
      let stats = [
        {
          name: "Investors added",
          investors: uniq(this.investors
            .filter((d) => d.status === 1 && d.created_at == d.modified_at)
          ),
        },
        {
          name: "Investors updated",
          investors: uniq(this.investors
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
          investors: uniqByKeepLatest(this.investors)
            .filter((d) => d.draft_status === null && (d.status === 2 || d.status === 3))
        },
        {
          name: "Investors pending",
          investors: uniqByKeepLatest(this.investors)
            .filter((d) => d.draft_status !== null)
        },
      ];
      for (let stat of stats) {
        stat.value = stat.investors.length;
      }
      return stats;
    },
    allStatsCsv() {
      let allStats = {};
      for (var stats of this.deal_statistics) {
        allStats[stats.name] = stats.value;
      }
      for (var stats of this.investor_statistics) {
        allStats[stats.name] = stats.value;
      }
      return [allStats];
    },
    allStatsCsvFileName() {
      let filename = "Indicators_";
      filename += dayjs(this.daterange.start).format('DD-MM-YYYY');
      filename += "_" + dayjs(this.daterange.end).format('DD-MM-YYYY');
      if (this.selectedCountry) {
        filename += "_" + this.selectedCountry.slug;
      } else {
        filename += "_" + this.selectedRegion.slug;
      }
      filename += ".csv";
      return filename;
    }
  },
  watch: {
    user() {
      this.triggerUserRegion();
    },
  },
  methods: {
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

      let filterByEditorLocation = '';
      if (this.selectedCountry) {
        filterByEditorLocation =
          `{
              field:"revision.user.userregionalinfo.country_id",
              operation:EQ,
              value:"${this.selectedCountry.id}"
           },`
      }
      if (this.selectedRegion && this.selectedRegion.id != -1) {
        filterByEditorLocation =
          `{
              field:"revision.user.userregionalinfo.region.id",
              operation:EQ,
              value:"${this.selectedRegion.id}"
           },`
      }

      const query = `query {
        deals: dealversions(filters:[
          {field:"revision.date_created",operation:GE,value:"${dr_start}"},
          {field:"revision.date_created",operation:LE,value:"${dr_end}"},
        ])
        {
          deal  {
            id
            deal_size
            fully_updated
            fully_updated_at
            status
            draft_status
            confidential
            country { id name high_income region {id} }
            datasources { id type name }
            created_at
            modified_at
          }
        }
        investors: investorversions(filters:[
          {field:"revision.date_created",operation:GE,value:"${dr_start}"},
          {field:"revision.date_created",operation:LE,value:"${dr_end}"},
          ${filterByEditorLocation}
        ])
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
        statistics {
          deals_public_count
          deals_public_multi_ds_count
          deals_public_high_geo_accuracy
          deals_public_polygons
        }
      }`;


      axios
        .post("/graphql/", {query})
        .then((response) => {
          // this.deals_added = response.data.data.deals_added || [];
          // this.deals_updated = response.data.data.deals_updated || [];
          // this.deals_fully_updated = response.data.data.deals_fully_updated || [];
          // this.investors_added = response.data.data.investors_added || [];
          // this.investors_updated = response.data.data.investors_updated || [];
          this.deals = response.data.data.deals.map((v) => v.deal) || [];
          this.investors = response.data.data.investors.map((v) => v.investor) || [];
          this.goal_statistics = response.data.data.statistics || {};
        })
        .finally(() => (this.loading = false));
    },
    prepareDeals(deals) {
      return deals.map((deal) => {
        let country = deal.country ? deal.country.name : "";
        let operating_company = deal.operating_company
          ? deal.operating_company.name
          : "";
        let confidential = deal.confidential ? "fa-check" : "fa-times";
        return {
          ...deal,
          created_at: dayjs(deal.created_at).format("YYYY-MM-DD"),
          modified_at: dayjs(deal.modified_at).format("YYYY-MM-DD"),
          confidential: `<i class="fa ${confidential}" aria-hidden="true"></i>`,
          country,
          operating_company,
        };
      });
    },
    prepareDealsCsv(deals) {
      return this.prepareDeals(deals).map((deal) => {
        delete deal.confidential;
        delete deal.datasources;
        return {
          ...deal,
        };
      })
    },
    prepareInvestors(investors) {
      return investors.map((investor) => {
        let country = investor.country ? investor.country.name : "";
        return {
          ...investor,
          country,
          created_at: dayjs(investor.created_at).format("YYYY-MM-DD"),
          modified_at: dayjs(investor.modified_at).format("YYYY-MM-DD"),
        };
      });
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
