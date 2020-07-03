<template>
  <div class="container">
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
                @input="selectedCountry = null"
              />
            </div>
            <div class="multiselect-div">
              <multiselect
                v-model="selectedCountry"
                :options="countries"
                label="name"
                placeholder="Country"
                @input="selectedRegion = null"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="number-of-deals">
      <div class="loadingscreen" v-if="loading">
        <div class="loader"></div>
      </div>
      <b-tabs>
        <b-tab>
          <template v-slot:title>
            <h2 v-if="filtered_deals.length">{{ filtered_deals.length }} Deals</h2>
            <h2 v-else>Deals</h2>
          </template>

          <b-tabs pills card vertical>
            <b-tab v-for="(stats, i) in deal_statistics" :key="i">
              <template v-slot:title>
                <strong>{{ stats.deals.length }}</strong> {{ stats.name }}<br />
              </template>
              <b-card-text>
                <DealTable
                  :deals="prepareDeals(stats.deals)"
                  :fields="dealFields"
                  :pageSize="10"
                />
              </b-card-text>
            </b-tab>
          </b-tabs>
        </b-tab>
      </b-tabs>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import dayjs from "dayjs";
  import DealTable from "@/components/Deal/DealTable";
  import { mapState } from "vuex";
  import InvestorTable from "@/components/Investor/InvestorTable";

  export default {
    components: { InvestorTable, DealTable },
    data: function () {
      return {
        loading: true,
        today: dayjs().format("YYYY/MM/DD"),
        daterange: {
          start: dayjs().subtract(30, "day").toDate(),
          end: new Date(),
        },
        selectedCountry: null,
        selectedRegion: null,

        deals: [],
        dealFields: [
          "deal_size",
          "status",
          "draft_status",
          "confidential",
          "country",
          "operating_company",
          "timestamp",
        ],
        investorFields: ["name", "status"],
        investors: [],

        selectedDateOption: 30,
        date_pre_options: [
          { name: "Last 30 days", value: 30 },
          { name: "Last 60 days", value: 60 },
          { name: "Last 180 days", value: 180 },
          { name: "Last 365 days", value: 365 },
        ],
      };
    },
    computed: {
      ...mapState({
        regions: (state) => state.page.regions,
        countries: (state) => state.page.countries,
        user: (state) => state.page.user,
      }),
      filtered_deals() {
        if (this.selectedCountry)
          return this.deals.filter((d) => {
            return d.country && d.country.id === this.selectedCountry.id;
          });
        if (this.selectedRegion)
          return this.deals.filter((d) => {
            return d.country && d.country.region.id === this.selectedRegion.id;
          });
        return this.deals;
      },
      deal_statistics() {
        return [
          {
            name: "Deals added",
            deals: this.filtered_deals.filter((d) => d.status === 2),
          },
          {
            name: "Deals updated",
            deals: this.filtered_deals.filter((d) => d.status === 3),
          },
          {
            name: "Deals published",
            deals: this.filtered_deals.filter((d) => d.status === 2 || d.status === 3),
          },
          {
            name: "Deals pending",
            deals: this.filtered_deals.filter((d) => d.draft_status !== null),
          },
          {
            name: "Deals rejected",
            deals: this.filtered_deals.filter((d) => d.status === 5),
          },
          {
            name: "Deals pending deletion",
            deals: this.filtered_deals.filter((d) => d.status === 6),
          },
          {
            name: "Deals active, not public",
            deals: this.filtered_deals.filter((d) => {
              // only consider deals that are "live/updated"
              if (!(d.status === 2 || d.status === 3)) return false;

              if (d.confidential) return true;
              if (!d.country || d.country.high_income) return true;
              if (!d.datasources) return true;
              if (!d.operating_company || d.operating_company.name === "") return true;
              // TODO: The parent company unknown filter is still missing here;
              return false;
            }),
          },
          {
            name: "Deals active, not-public flag",
            deals: this.filtered_deals.filter((d) => {
              // only consider deals that are "live/updated"
              if (!(d.status === 2 || d.status === 3)) return false;
              return !!d.confidential;
            }),
          },
        ];
      },
      filtered_investors() {
        if (this.selectedCountry)
          return this.investors.filter((d) => {
            return d.country && d.country.id === this.selectedCountry.id;
          });
        if (this.selectedRegion)
          return this.investors.filter((d) => {
            return d.country && d.country.region.id === this.selectedRegion.id;
          });
        return this.investors;
      },
      investor_statistics() {
        return [
          {
            name: "Investors added",
            investors: this.filtered_investors.filter((d) => d.status === 1),
          },
          {
            name: "Investors updated",
            investors: this.filtered_investors.filter((d) => d.status === 3),
          },
          {
            name: "Investors published",
            investors: this.filtered_investors.filter(
              (d) => d.status === 2 || d.status === 3
            ),
          },
          {
            name: "Investors pending",
            investors: this.filtered_investors.filter((d) => d.draft_status !== null),
          },
        ];
      },
    },
    watch: {
      user() {
        this.triggerUserRegion();
      },
      regions() {
        this.triggerUserRegion();
      },
      countries() {
        this.triggerUserRegion();
      },
    },
    methods: {
      triggerUserRegion() {
        if (!this.countries) return;
        if (!this.regions) return;
        if (!this.user) return;
        if (this.user.userregionalinfo) {
          let uri = this.user.userregionalinfo;
          if (uri.region) {
            this.selectedRegion = uri.region[0];
            this.updateStats("region");
          }
          if (uri.country) {
            this.selectedCountry = uri.country[0];
            this.updateStats("country");
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
        this.loading = true;

        let query = `query Stats($filters: [Filter]) {
          deals(limit: 0, filters: $filters) {
           id
           deal_size
           fully_updated
           status
           draft_status
           confidential
           country { id name high_income region {id} }
           datasources { id }
           operating_company {name}
           timestamp
          }
          investors(limit: 0, filters: $filters) {
           id
           name
           timestamp
           status
           draft_status
           country { id name high_income region { id } }
          }
        }`;
        let variables = {
          filters: [
            {
              field: "timestamp",
              operation: "GE",
              value: dayjs(this.daterange.start).format("YYYY-MM-DD"),
            },
            {
              field: "timestamp",
              operation: "LE",
              value: dayjs(this.daterange.end).format("YYYY-MM-DD"),
            },
          ],
        };
        axios.post("/graphql/", { query, variables }).then((response) => {
          this.deals = response.data.data.deals;
          this.investors = response.data.data.investors;
          this.loading = false;
        });
      },
      prepareDeals(deals) {
        return deals.map((deal) => {
          let country = deal.country ? deal.country.name : "";
          let operating_company = deal.operating_company
            ? deal.operating_company.name
            : "";
          let timestamp = dayjs(deal.timestamp).format("YYYY-MM-DD");
          let confidential = deal.confidential ? "fa-check" : "fa-times";
          return {
            ...deal,
            timestamp,
            confidential: `<i class="fa ${confidential}" aria-hidden="true"></i>`,
            country,
            operating_company,
          };
        });
      },
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
  .number-of-deals {
    position: relative;

    .loadingscreen {
      z-index: 10;
      position: absolute;
      width: 100%;
      height: 100%;
      background: rgba(128, 128, 128, 0.8);
      /*background: rgba( darken($primary, 30%), 0.7 );*/
    }
  }

  .loader,
  .loader:before,
  .loader:after {
    background: #ffffff;
    -webkit-animation: load1 1s infinite ease-in-out;
    animation: load1 1s infinite ease-in-out;
    width: 1em;
    height: 4em;
  }
  .loader {
    color: #ffffff;
    text-indent: -9999em;
    margin: 88px auto;
    position: relative;
    font-size: 11px;
    -webkit-transform: translateZ(0);
    -ms-transform: translateZ(0);
    transform: translateZ(0);
    -webkit-animation-delay: -0.16s;
    animation-delay: -0.16s;
  }
  .loader:before,
  .loader:after {
    position: absolute;
    top: 0;
    content: "";
  }
  .loader:before {
    left: -1.5em;
    -webkit-animation-delay: -0.32s;
    animation-delay: -0.32s;
  }
  .loader:after {
    left: 1.5em;
  }
  @-webkit-keyframes load1 {
    0%,
    80%,
    100% {
      box-shadow: 0 0;
      height: 4em;
    }
    40% {
      box-shadow: 0 -2em;
      height: 5em;
    }
  }
  @keyframes load1 {
    0%,
    80%,
    100% {
      box-shadow: 0 0;
      height: 4em;
    }
    40% {
      box-shadow: 0 -2em;
      height: 5em;
    }
  }
</style>

<style lang="scss">
  @import "../../scss/colors";

  .nav-link.active.teal-background {
    background: $lm_investor !important;
  }
</style>
