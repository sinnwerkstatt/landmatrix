<template>
  <div class="container">
    <div class="loadingscreen" v-if="loading">
      <div class="loader"></div>
    </div>
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
        <a class="btn btn-outline-primary">Download Indicators</a>
      </DownloadJsonCSV>
    </div>
    <div class="number-of-deals">
      <b-tabs>
        <b-tab>
          <template v-slot:title>
            <h2>Deals</h2>
          </template>

          <b-tabs pills card vertical nav-wrapper-class="col-lg-3 col-md-12" content-class="col-lg-9 col-md-12">
            <b-tab v-for="(stats, i) in deal_statistics" :key="i">
              <template v-slot:title>
                <strong>{{ stats.deals.length }}</strong> {{ stats.name }}<br/>
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
            <h2>Investors</h2>
          </template>

          <b-tabs pills card vertical nav-wrapper-class="col-lg-3 col-md-12" content-class="col-lg-9 col-md-12">
            <b-tab v-for="(stats, i) in investor_statistics" :key="i">
              <template v-slot:title>
                <strong>{{ stats.investors.length }}</strong> {{ stats.name }}<br/>
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
  </div>
</template>

<script>
import axios from "axios";
import dayjs from "dayjs";
import DealTable from "/components/Deal/DealTable";
import {mapState} from "vuex";
import InvestorTable from "/components/Investor/InvestorTable";
import DownloadJsonCSV from 'vue-json-csv';

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

      deals_added: [],
      deals_updated: [],
      deals_fully_updated: [],
      dealFields: [
        "country",
        "deal_size",
        "status",
        "draft_status",
        "confidential",
        "operating_company",
        "created_at",
        "modified_at",
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
    };
  },
  computed: {
    ...mapState({
      regions: (state) => state.page.regions,
      countries: (state) => state.page.countries,
      user: (state) => state.page.user,
    }),
    formFilled() {
      return this.selectedCountry || this.selectedRegion;
    },
    deal_statistics() {
      return [
        {
          name: "Deals added",
          deals: this.deals_added,
        },
        {
          name: "Deals updated",
          deals: this.deals_updated,
        },
        {
          name: "Deals Fully Updated",
          deals: this.deals_fully_updated,
        },
        {
          name: "Deals published",
          deals: this.deals_updated.filter((d) => d.status === 2 || d.status === 3),
        },
        {
          name: "Deals pending",
          deals: this.deals_updated.filter((d) => d.draft_status !== null),
        },
        {
          name: "Deals rejected",
          deals: this.deals_updated.filter((d) => d.status === 5),
        },
        {
          name: "Deals pending deletion",
          deals: this.deals_updated.filter((d) => d.status === 6),
        },
        {
          name: "Deals active, not public",
          deals: this.deals_updated.filter((d) => {
            // only consider deals that are "live/updated"
            if (!(d.status === 2 || d.status === 3)) return false;

            if (d.confidential) return true;
            if (!d.country || d.country.high_income) return true;
            if (!d.datasources) return true;
            if (!d.operating_company || d.operating_company.is_actually_unknown)
              return true;
            // TODO: The parent company unknown filter is still missing here;
            return false;
          }),
        },
        {
          name: "Deals active, not-public flag",
          deals: this.deals_updated.filter((d) => {
            // only consider deals that are "live/updated"
            if (!(d.status === 2 || d.status === 3)) return false;
            return !!d.confidential;
          }),
        },
      ];
    },
    investor_statistics() {
      return [
        {
          name: "Investors added",
          investors: this.investors.filter((d) => d.status === 1),
        },
        {
          name: "Investors updated",
          investors: this.investors.filter((d) => d.status === 3),
        },
        {
          name: "Investors published",
          investors: this.investors.filter(
            (d) => d.status === 2 || d.status === 3
          ),
        },
        {
          name: "Investors pending",
          investors: this.investors.filter((d) => d.draft_status !== null),
        },
      ];
    },
    allStatsCsv() {
      let allStats = {};
      for (var stats of this.deal_statistics) {
        allStats[stats.name] = stats.deals.length;
      }
      for (var stats of this.investor_statistics) {
        allStats[stats.name] = stats.investors.length;
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
      const deal_gql_fields = `{
           id
           deal_size
           fully_updated
           status
           draft_status
           confidential
           country { id name high_income region {id} }
           datasources { id }
           operating_company {name is_actually_unknown}
           created_at
           modified_at
        }`;
      const investor_gql_fields = `{
          id
          name
          created_at
          modified_at
          status
          draft_status
          country { id name high_income region { id } }
        }`;
      let dr_start = dayjs(this.daterange.start).format("YYYY-MM-DD");
      let dr_end = dayjs(this.daterange.end).format("YYYY-MM-DD");
      let reg_con = "", reg_con_inv = "";
      if (this.selectedCountry) {
        reg_con = `{field:"country.id",operation:EQ,value:"${this.selectedCountry.id}"}`;
      }
      if (this.selectedRegion) {
        reg_con = `{field:"country.fk_region_id",operation:EQ,value:"${this.selectedRegion.id}"}`;
      }

      const query = `query {
          deals_added: deals(limit: 0, filters: [
            {field:"created_at",operation:GE,value:"${dr_start}"},
            {field:"created_at",operation:LE,value:"${dr_end}"},
            {field:"status",operation:IN,value:["1","2","3"]},
            ${reg_con}
            ]) ${deal_gql_fields}
          deals_updated: deals(limit: 0, filters: [
            {field:"modified_at",operation:GE,value:"${dr_start}"},
            {field:"modified_at",operation:LE,value:"${dr_end}"},
            {field:"status",operation:IN,value:["1","2","3"]},
            ${reg_con}
            ]) ${deal_gql_fields}
          deals_fully_updated: deals(limit: 0, filters: [
            {field:"fully_updated_at",operation:GE,value:"${dr_start}"},
            {field:"fully_updated_at",operation:LE,value:"${dr_end}"},
            ${reg_con}
            ]) ${deal_gql_fields}
          investors_data: investors(limit: 0, filters:[
            ${reg_con}
            ]) ${investor_gql_fields}
        }`;

      axios
        .post("/graphql/", {query})
        .then((response) => {
          this.deals_added = response.data.data.deals_added || [];
          this.deals_updated = response.data.data.deals_updated || [];
          this.deals_fully_updated = response.data.data.deals_fully_updated || [];
          this.investors = response.data.data.investors_data;
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
}

.scroll-container {
  overflow: scroll;
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
