<template>
  <div class="observatory">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-sm-12 col-md-10 col-lg-8 col-xl-6">
          <h1>{{ page.title }}</h1>
          <div v-if="page.introduction_text">
            <p>{{ page.introduction_text }}</p>
            <p v-if="!readMore"><a href="" @click.prevent="readMore=true">Read more</a></p>
          </div>
          <div v-if="readMore" class="row">
            <Streamfield :content="content"/>
          </div>
        </div>
      </div>
    </div>
    <div class="jumbotron jumbotron-fluid charts">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-sm-12 col-md-10 col-lg-8 col-xl-6">
            <div class="row">
              <div class="col-12">
                <h3>We currently have information about:</h3>
                <div class="row">
                  <div class="col-6 text-center">
                    <label>Size</label>
                    <div class="total">{{ totalSize }}</div>
                    <StatusPieChart :deal-data="negotiationStatusDataSizes" :displayLegend="true" :aspect-ratio="1"></StatusPieChart>
                  </div>
                  <div class="col-6 text-center">
                    <label>Number of deals</label>
                    <div class="total">{{ totalCount }}</div>
                    <StatusPieChart :deal-data="negotiationStatusDataCounts" :displayLegend="true" :aspect-ratio="1"></StatusPieChart>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-sm-12 col-md-11 col-lg-9 col-xl-7">
          <MapDataCharts></MapDataCharts>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import numeral from "numeral";
import gql from "graphql-tag";
import {prepareNegotianStatusData, sum} from "../../utils/data_processing";
import Streamfield from "/components/Streamfield";
import StatusPieChart from "../../components/Charts/StatusPieChart";
import MapDataCharts from "../../components/Wagtail/MapDataCharts";

export default {
  components: {StatusPieChart, Streamfield, MapDataCharts},
  data() {
    return {
      readMore: false,
      deals: [],
    }
  },
  apollo: {
    deals: {
      $skipAll() {
        return this.locationFilter.length == 0;
      },
      query: gql`
        query Deals($limit: Int!, $filters: [Filter]) {
          deals(limit: $limit, filters: $filters) {
            id
            deal_size
            country {
              id
              fk_region {
                id
              }
            }
            # top_investors { id name }
            intention_of_investment
            current_negotiation_status
            current_implementation_status
            locations {
              id
              point
              level_of_accuracy
            }
          }
        }
      `,
      variables() {
        return {
          limit: 0,
          filters: this.locationFilter,
        };
      },
    },
  },
  computed: {
    page() {
      return this.$store.state.page.wagtailPage;
    },
    content() {
      return this.page ? this.page.body : [];
    },
    locationFilter() {
      if (this.page.region) {
        return [{field: "country.fk_region_id", value: this.page.region.id.toString()}];
      } else if (this.page.country) {
        return [{filter: "country_id", value: this.page.country.id.toString()}];
      }
    },
    totalCount() {
      return numeral(this.deals.length).format("0,0");
    },
    totalSize() {
      return `${numeral(sum(this.deals, 'deal_size')).format('0,0')} ha`;
    },
    dealsFilteredByNegStatus() {
      return prepareNegotianStatusData(this.deals);
    },
    negotiationStatusDataCounts() {
      return this.dealsFilteredByNegStatus.map(d => {
        return {value: d.count, unit: "deals", ...d}
      });
    },
    negotiationStatusDataSizes() {
      return this.dealsFilteredByNegStatus.map(d => {
        return {value: d.size, unit: "ha", ...d}
      });
    },
  },
  watch: {
    page: {
      immediate: true,
      handler() {
        this.readMore = !this.page.introduction_text;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../../scss/colors";

.observatory {
  h1 {
    font-size: 48px;
    font-weight: normal !important;
    color: black;
    text-align: left;
    text-transform: none;

    &:before {
      content: none;
    }
  }

  .charts {
    background-color: #F9F9F9;
    padding: 0;
    padding-bottom: 0.3rem;

    label {
      color: $lm_orange;
      font-weight: bold;
    }
    .total {
      font-weight: bold;
      margin-bottom: 1em;
    }
  }
}
</style>
<style lang="scss">
.observatory {
  h3 {
    font-size: 24px;
  }
  .charts {
    .legend {
      text-align: center;
      margin-top: 1em;
      .legend-item {
        .colored-area {
          width: 0.8em;
          height: 0.8em;
        }
      }
    }
  }
}
</style>
