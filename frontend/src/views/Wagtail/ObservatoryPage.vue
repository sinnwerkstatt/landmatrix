<template>
  <div class="observatory">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-sm-12 col-md-10 col-lg-8 col-xl-6">
          <h1>{{ page.title }}</h1>
          <QuasiStaticMap
            :deals="deals"
            :region_id="region_id"
            :country_id="country_id"
          />
        </div>
      </div>
      <div class="row justify-content-center">
        <div class="col-sm-12 col-md-10 col-lg-8 col-xl-6">
          <div class="intro-text" v-if="page.introduction_text">
            <div class="intro">{{ page.introduction_text }}</div>
            <div class="readmore" v-if="!readMore">
              <p><a href="" @click.prevent="readMore = true">Read more</a></p>
            </div>
            <Streamfield v-if="readMore" :content="content" />
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
                    <StatusPieChart
                      :deal-data="negotiationStatusDataSizes"
                      :displayLegend="true"
                      :aspect-ratio="1"
                    ></StatusPieChart>
                  </div>
                  <div class="col-6 text-center">
                    <label>Number of deals</label>
                    <div class="total">{{ totalCount }}</div>
                    <StatusPieChart
                      :deal-data="negotiationStatusDataCounts"
                      :displayLegend="true"
                      :aspect-ratio="1"
                    ></StatusPieChart>
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
          <MapDataCharts @click.native="setGlobalLocationFilter"></MapDataCharts>
        </div>
      </div>
    </div>
    <ArticleList
      :articlesLabel="'Country Profiles'"
      :articles="filteredCountryProfiles"
    >
      <div class="description">
        <p>
          Country profiles present national-level data of large-scale land acquisitions
          and transactions including who the investors are, what the aim of the
          investment is, who the former owner was and what the land was previously used
          for, and what the potential benefits and impacts of the land deals are.
        </p>
        <p>
          By making this information available, the Land Matrix hopes to enhance broad
          engagement and data exchange, facilitating the continuous improvement of the
          data. Find out how to get involved
          <router-link :to="`/get-involved/`">{{ $t("here") }} </router-link>
          .
        </p>
        <h4>Download country profiles for:</h4>
      </div>
    </ArticleList>
    <ArticleList
      :articlesLabel="'News & publications'"
      :articles="filteredNewsPubs"
    ></ArticleList>
    <div v-if="page.twitter_feed" class="container tweets">
      <div class="row justify-content-center">
        <div class="col-sm-12 col-md-10 col-lg-8 col-xl-6">
          <h3>Latest tweets</h3>
          <Twitter :value="page.twitter_feed"></Twitter>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import numeral from "numeral";
  import gql from "graphql-tag";
  import { prepareNegotianStatusData, sum } from "../../utils/data_processing";
  import Streamfield from "/components/Streamfield";
  import StatusPieChart from "../../components/Charts/StatusPieChart";
  import MapDataCharts from "../../components/Wagtail/MapDataCharts";
  import ArticleList from "../../components/Wagtail/ArticleList";
  import Twitter from "../../components/Wagtail/Twitter";
  import QuasiStaticMap from "../../components/QuasiStaticMap";
  import { data_deal_query_gql } from "../Data/query";

  export default {
    components: {
      QuasiStaticMap,
      StatusPieChart,
      Streamfield,
      MapDataCharts,
      ArticleList,
      Twitter,
    },
    data() {
      return {
        readMore: false,
        deals: [],
        articles: [],
      };
    },
    apollo: {
      deals: {
        query: data_deal_query_gql,
        variables() {
          let user = this.$store.state.page.user;
          return {
            limit: 0,
            filters: this.locationFilter,
            subset: user && user.is_authenticated ? "ACTIVE" : "PUBLIC",
          };
        },
      },
      articles: {
        skip() {
          return this.deals.length == 0;
        },
        query: gql`
          query {
            articles: blogpages {
              id
              title
              slug
              date
              header_image
              excerpt
              categories {
                slug
              }
              tags {
                slug
              }
            }
          }
        `,
      },
    },
    computed: {
      page() {
        return this.$store.state.page.wagtailPage;
      },
      region_id() {
        return this.page.region ? this.page.region.id : null;
      },
      country_id() {
        return this.page.country ? this.page.country.id : null;
      },
      locationItem() {
        if (this.page.region) {
          return this.$store.getters.getCountryOrRegion({
            type: "region",
            id: this.page.region.id,
          });
        } else if (this.page.country) {
          return this.$store.getters.getCountryOrRegion({
            type: "country",
            id: this.page.country.id,
          });
        }
      },
      slug() {
        return this.locationItem ? this.locationItem.slug : null;
      },
      content() {
        return this.page ? this.page.body : [];
      },
      locationFilter() {
        if (this.page.region) {
          return [
            { field: "country.fk_region_id", value: this.page.region.id.toString() },
          ];
        } else if (this.page.country) {
          return [{ field: "country_id", value: this.page.country.id.toString() }];
        } else {
          return [];
        }
      },
      totalCount() {
        return numeral(this.deals.length).format("0,0");
      },
      totalSize() {
        return `${numeral(sum(this.deals, "deal_size")).format("0,0")} ha`;
      },
      dealsFilteredByNegStatus() {
        return prepareNegotianStatusData(this.deals);
      },
      negotiationStatusDataCounts() {
        return this.dealsFilteredByNegStatus.map((d) => {
          return { value: d.count, unit: "deals", ...d };
        });
      },
      negotiationStatusDataSizes() {
        return this.dealsFilteredByNegStatus.map((d) => {
          return { value: d.size, unit: "ha", ...d };
        });
      },
      filteredCountryProfiles() {
        if (!this.slug) return [];
        return this.articles
          .filter((a) => {
            return (
              a.tags.find((t) => {
                return t.slug === this.slug;
              }) &&
              a.categories.find((c) => {
                return c.slug === "country-profile";
              })
            );
          })
          .sort((a, b) => a.date < b.date);
      },
      filteredNewsPubs() {
        if (!this.slug) return [];
        return this.articles
          .filter((a) => {
            return (
              a.tags.find((t) => {
                return t.slug === this.slug;
              }) &&
              a.categories.find((c) => {
                return ["news", "publications"].includes(c.slug);
              })
            );
          })
          .sort((a, b) => a.date < b.date);
      },
    },
    methods: {
      setGlobalLocationFilter(event) {
        if (this.page.region) {
          this.$store.dispatch("setFilter", {
            filter: "country_id",
            value: null,
          });
          this.$store.dispatch("setFilter", {
            filter: "region_id",
            value: this.page.region.id,
          });
        } else if (this.page.country) {
          this.$store.dispatch("setFilter", {
            filter: "region_id",
            value: null,
          });
          this.$store.dispatch("setFilter", {
            filter: "country_id",
            value: this.page.country.id,
          });
        }
      },
    },
    watch: {
      page: {
        immediate: true,
        handler() {
          this.readMore = !this.page.introduction_text;
        },
      },
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";

  .observatory {
    margin-bottom: 5em;
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

    .intro-text {
      padding-top: 1.5em;
      padding-bottom: 0.8em;
      .readmore {
        margin-top: 1.5em;
      }
    }

    .charts {
      background-color: #f9f9f9;
      padding: 0;
      padding-bottom: 1.5em;
      margin-top: 0;

      label {
        color: $lm_orange;
        font-weight: bold;
        font-size: 15px;
        margin-bottom: 0;
      }

      .total {
        font-weight: bold;
        font-size: 15px;
        margin-bottom: 0.5em;
      }
    }

    .tweets {
      margin-bottom: 2em;
    }
  }
</style>
<style lang="scss">
  .observatory {
    h3 {
      font-size: 24px;
    }

    .static-map {
      margin-top: 1.5em;
    }

    .streamfield {
      .container {
        padding-top: 1.5em;
        padding-bottom: 0;
      }
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
