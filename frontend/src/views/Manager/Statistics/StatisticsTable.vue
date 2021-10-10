<template>
  <div class="statistics-table">
    <div class="actions">
      <DownloadJsonCSV
        v-if="formFilled"
        :data="allStatsCsv"
        :name="allStatsCsvFileName"
      >
        <a class="btn btn-outline-primary">Download all indicators as CSV</a>
      </DownloadJsonCSV>
    </div>
    <div class="number-of-deals">
      <b-tabs>
        <b-tab>
          <template #title>
            <h3>Deals</h3>
          </template>

          <b-tabs
            card
            content-class="col-lg-9 col-md-12"
            nav-wrapper-class="col-lg-3 col-md-12"
            pills
            vertical
          >
            <b-tab v-for="(stats, i) in dealStatistics" :key="i">
              <template #title>
                <strong>{{ stats.value }}</strong> {{ stats.name }}<br />
              </template>
              <b-card-text>
                <div class="actions">
                  <DownloadJsonCSV
                    v-if="prepareDealsCsv(stats.deals).length"
                    :data="prepareDealsCsv(stats.deals)"
                    :name="`Indicator-List_${stats.name}.csv`"
                  >
                    <a class="btn btn-outline-primary">Download deals as CSV</a>
                  </DownloadJsonCSV>
                </div>
                <div class="scroll-container">
                  <DealTable
                    :deals="prepareDeals(stats.deals)"
                    :fields="dealFields"
                    :page-size="10"
                  />
                </div>
              </b-card-text>
            </b-tab>
          </b-tabs>
        </b-tab>
        <b-tab>
          <template #title>
            <h3>Investors</h3>
          </template>

          <b-tabs
            card
            content-class="col-lg-9 col-md-12"
            nav-wrapper-class="col-lg-3 col-md-12"
            pills
            vertical
          >
            <b-tab v-for="(stats, i) in investorStatistics" :key="i">
              <template #title>
                <strong>{{ stats.value }}</strong> {{ stats.name }}<br />
              </template>
              <b-card-text>
                <div class="actions">
                  <DownloadJsonCSV
                    v-if="prepareInvestors(stats.investors).length"
                    :data="prepareInvestors(stats.investors)"
                    :name="`Indicator-List_${stats.name}.csv`"
                  >
                    <a class="btn btn-outline-primary">Download investors as CSV</a>
                  </DownloadJsonCSV>
                </div>
                <div class="scroll-container">
                  <InvestorTable
                    :fields="investorFields"
                    :investors="prepareInvestors(stats.investors)"
                    :page-size="10"
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

<script lang="ts">
  import DealTable from "$components/Deal/DealTable";
  import InvestorTable from "$components/Investor/InvestorTable";
  import dayjs from "dayjs";
  // noinspection TypeScriptCheckImport
  import DownloadJsonCSV from "vue-json-csv";
  import Vue, { PropType } from "vue";
  import type { Country, Region } from "$types/wagtail";

  export default Vue.extend({
    name: "StatisticsTable",
    components: { InvestorTable, DealTable, DownloadJsonCSV },
    props: {
      dealStatistics: { type: Object },
      investorStatistics: { type: Object },
      countries: { type: Object as PropType<Country[]>, default: null },
      selectedRegion: { type: Object as PropType<Region> },
      selectedCountry: { type: Object as PropType<Country> },
    },
    data: function () {
      return {
        dealFields: [
          "country",
          "deal_size",
          "status",
          "draft_status",
          "confidential",
          "created_at",
          "modified_at",
          "fully_updated_at",
        ],
        investorFields: [
          "name",
          "country",
          "status",
          "draft_status",
          "created_at",
          "modified_at",
        ],
      };
    },
    computed: {
      formFilled() {
        return this.selectedRegion || this.selectedCountry;
      },
      allStatsCsv() {
        let allStats = {};
        for (let stats of this.dealStatistics) {
          allStats[stats.name] = stats.value;
        }
        for (let stats of this.investorStatistics) {
          allStats[stats.name] = stats.value;
        }
        return [allStats];
      },
      allStatsCsvFileName() {
        let filename = "Indicators_";
        if (this.selectedCountry) {
          filename += "_" + this.selectedCountry.slug;
        } else {
          filename += "_" + this.selectedRegion.slug;
        }
        filename += ".csv";
        return filename;
      },
    },
    methods: {
      prepareDeals(deals) {
        return deals.map((deal) => {
          let country = this.countries.find((c) => c.id == deal.country_id);
          country = country ? country.name : "";
          let operating_company = deal.operating_company
            ? deal.operating_company.name
            : "";
          let confidential = deal.confidential ? "fa-check" : "fa-times";
          return {
            ...deal,
            created_at: dayjs(deal.created_at).format("YYYY-MM-DD"),
            modified_at: dayjs(deal.modified_at).format("YYYY-MM-DD"),
            fully_updated_at: dayjs(deal.modified_at).format("YYYY-MM-DD"),
            confidential: `<i class="fa ${confidential}" aria-hidden="true"></i>`,
            country,
            operating_company,
          };
        });
      },
      prepareDealsCsv(deals) {
        return this.prepareDeals(deals).map((deal) => {
          delete deal.confidential;
          return {
            ...deal,
          };
        });
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
      },
    },
  });
</script>

<style lang="scss" scoped>
  .actions {
    margin-bottom: -0.7em;
    text-align: right;

    > div {
      display: inline-block;
    }
  }

  .scroll-container {
    overflow: scroll;
  }

  .nav-tabs {
    h2,
    h3 {
      margin-top: 0;
      margin-bottom: 0;
    }
  }
</style>
