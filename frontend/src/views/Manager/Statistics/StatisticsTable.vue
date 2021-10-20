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
                    v-if="prepareDealsCsv(stats.objs).length"
                    :data="prepareDealsCsv(stats.objs)"
                    :name="`Indicator-List_${stats.name}.csv`"
                  >
                    <a class="btn btn-outline-primary">Download deals as CSV</a>
                  </DownloadJsonCSV>
                </div>
                <div class="scroll-container">
                  <DealTable :deals="stats.objs" :fields="dealFields" :page-size="10" />
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
                    v-if="stats.objs.length > 0"
                    :data="stats.objs"
                    :name="`Indicator-List_${stats.name}.csv`"
                  >
                    <a class="btn btn-outline-primary">Download investors as CSV</a>
                  </DownloadJsonCSV>
                </div>
                <div class="scroll-container">
                  <InvestorTable
                    :fields="investorFields"
                    :investors="stats.objs"
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
  import Vue, { PropType } from "vue";
  import dayjs from "dayjs";
  import DealTable from "$components/Deal/DealTable.vue";
  import InvestorTable from "$components/Investor/InvestorTable.vue";
  import type { Country, Region } from "$types/wagtail";
  // @ts-ignore
  import DownloadJsonCSV from "vue-json-csv";
  import type { Stat } from "$views/Manager/CaseStatistics.vue";
  import type { Deal } from "$types/deal";
  import type { Investor } from "$types/investor";

  export default Vue.extend({
    name: "StatisticsTable",
    components: { InvestorTable, DealTable, DownloadJsonCSV },
    props: {
      dealStatistics: { type: Array as PropType<Stat<Deal>[]>, required: true },
      investorStatistics: { type: Array as PropType<Stat<Investor>[]>, required: true },
      countries: { type: Array as PropType<Country[]>, default: null },
      selectedRegion: { type: Object as PropType<Region>, default: null },
      selectedCountry: { type: Object as PropType<Country>, default: null },
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
      formFilled(): boolean {
        return !!(this.selectedRegion || this.selectedCountry);
      },
      allStatsCsv(): { [key: string]: number }[] {
        let allStats: { [key: string]: number } = {};
        for (let stats of this.dealStatistics) {
          allStats[stats.name] = stats.value;
        }
        for (let stats of this.investorStatistics) {
          allStats[stats.name] = stats.value;
        }
        return [allStats];
      },
      allStatsCsvFileName(): string {
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
      prepareDealsCsv(deals: Deal[]) {
        return deals.map((deal) => {
          // confidential: `<i class="fa ${confidential}" aria-hidden="true"></i>`,

          delete deal.confidential;
          let country = this.countries.find((c) => c.id == deal.country_id);

          return {
            ...deal,
            created_at: dayjs(deal.created_at).format("YYYY-MM-DD"),
            modified_at: dayjs(deal.modified_at).format("YYYY-MM-DD"),
            fully_updated_at: dayjs(deal.fully_updated_at).format("YYYY-MM-DD"),
            country: country ? country.name : "",
            operating_company: deal.operating_company?.name || "",
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
