<template>
  <div class="observatory">
    <PageTitle>{{ $t(page.title) }}</PageTitle>

    <div class="clamp-20-75p-56">
      <QuasiStaticMap :country-id="country_id" :region-id="region_id" />

      <div v-if="page.introduction_text" class="intro-text">
        <div class="intro">
          {{ page.introduction_text }}
        </div>
        <div v-if="!readMore" class="readmore">
          <p>
            <a href="" @click.prevent="readMore = true">{{ $t("Read more") }}</a>
          </p>
        </div>
        <div class="row">
          <Streamfield v-if="readMore" :content="content" />
        </div>
      </div>
    </div>

    <div class="charts">
      <div class="clamp-20-75p-56">
        <div class="row">
          <div class="col-12">
            <h3>{{ $t("We currently have information about:") }}</h3>
            <div class="row">
              <div class="col-6 text-center">
                <label>Size</label>
                <div class="total">{{ totalSize }} ha</div>
                <StatusPieChart
                  v-if="negotiationStatusBuckets"
                  :deal-data="negotiationStatusBuckets"
                  :aspect-ratio="1"
                  :container-style="{ maxWidth: '70%' }"
                  unit="ha"
                  value-field="size"
                />
              </div>
              <div class="col-6 text-center">
                <label>{{ $t("Number of deals") }}</label>
                <div class="total">
                  {{ totalCount }}
                </div>
                <StatusPieChart
                  v-if="negotiationStatusBuckets"
                  :deal-data="negotiationStatusBuckets"
                  :aspect-ratio="1"
                  :container-style="{ maxWidth: '70%' }"
                  value-field="count"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="clamp-20-75p-56">
      <MapDataCharts @click.native="setGlobalLocationFilter" />
    </div>

    <ArticleList
      :articles="filteredCountryProfiles"
      :articles-label="$t('Country profiles')"
    >
      <div class="description">
        <p>
          {{
            $t(
              "Country profiles present national-level data of large-scale land acquisitions and transactions including who the investors are, what the aim of the investment is, who the former owner was and what the land was previously used for, and what the potential benefits and impacts of the land deals are."
            )
          }}
        </p>
        <p>
          {{
            $t(
              "By making this information available, the Land Matrix hopes to enhance broad engagement and data exchange, facilitating the continuous improvement of the data. Find out how to get involved"
            )
          }}
          <router-link to="/contribute">{{ $t("here") }}</router-link>
          .
        </p>
        <h4>{{ $t("Download country profiles for") }}:</h4>
      </div>
    </ArticleList>
    <ArticleList
      :articles="filteredNewsPubs"
      :articles-label="$t('News & publications')"
    />
    <div v-if="page.twitter_feed" class="clamp-20-75p-56 tweets">
      <h3>{{ $t("Latest tweets") }}</h3>
      <Twitter :value="page.twitter_feed" />
    </div>
  </div>
</template>

<script lang="ts">
  import gql from "graphql-tag";
  import Vue from "vue";
  import StatusPieChart from "$components/Charts/StatusPieChart.vue";
  import PageTitle from "$components/PageTitle.vue";
  import QuasiStaticMap from "$components/QuasiStaticMap.vue";
  import Streamfield from "$components/Streamfield.vue";
  import ArticleList from "$components/Wagtail/ArticleList.vue";
  import MapDataCharts from "$components/Wagtail/MapDataCharts.vue";
  import Twitter from "$components/Wagtail/Twitter.vue";
  import type { BlogPage, ObservatoryPage, WagtailStreamfield } from "$types/wagtail";
  import type { DealAggregations } from "$types/deal";
  import type { GQLFilter } from "$types/filters";

  export default Vue.extend({
    name: "ObservatoryPage",
    components: {
      PageTitle,
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
        deal_aggregations: {} as DealAggregations,
        articles: [] as BlogPage[],
      };
    },
    apollo: {
      deal_aggregations: {
        query: gql`
          query DealAggregations(
            $fields: [String]!
            $subset: Subset
            $filters: [Filter]
          ) {
            deal_aggregations(fields: $fields, subset: $subset, filters: $filters) {
              current_negotiation_status {
                value
                size
                count
              }
            }
          }
        `,
        variables() {
          let extra_filter: GQLFilter[] = {
            region_id: this.page.region ? this.page.region.id : null,
            country_id: this.page.country ? this.page.country.id : null,
            negotiation_status: [],
          };
          return {
            fields: ["current_negotiation_status"],
            filters: this.$store.getters.defaultFiltersForGQL(extra_filter),
            subset: this.$store.getters.userAuthenticated ? "ACTIVE" : "PUBLIC",
          };
        },
      },
      articles: {
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
              url
            }
          }
        `,
      },
    },
    computed: {
      page(): ObservatoryPage {
        return this.$store.state.wagtailPage;
      },
      region_id(): number | null {
        return this.page.region ? this.page.region.id : null;
      },
      country_id(): number | null {
        return this.page.country ? this.page.country.id : null;
      },
      slug(): string {
        let ret;
        if (this.page.region) {
          ret = this.$store.getters.getCountryOrRegion({
            type: "region",
            id: this.page.region.id,
          });
        } else if (this.page.country) {
          ret = this.$store.getters.getCountryOrRegion({
            type: "country",
            id: this.page.country.id,
          });
        }
        return ret ? ret.slug : "";
      },
      content(): WagtailStreamfield {
        return this.page ? this.page.body : [];
      },
      totalCount(): string {
        if (!this.deal_aggregations.current_negotiation_status) return "";
        return this.deal_aggregations.current_negotiation_status
          .map((ns) => ns.count)
          .reduce((a, b) => +a + +b, 0)
          .toLocaleString("fr");
      },
      totalSize(): string {
        if (!this.deal_aggregations?.current_negotiation_status) return "";
        return this.deal_aggregations.current_negotiation_status
          .map((ns) => ns.size)
          .reduce((a, b) => +a + +b, 0)
          .toLocaleString("fr");
      },
      negotiationStatusBuckets(): unknown {
        if (!this.deal_aggregations.current_negotiation_status) return;
        let retval = [
          { color: "rgba(252,148,31,0.4)", label: "Intended", count: 0, size: 0 },
          { color: "rgba(252,148,31,1)", label: "Concluded", count: 0, size: 0 },
          { color: "rgba(125,74,15,1)", label: "Failed", count: 0, size: 0 },
          {
            color: "rgb(59,36,8)",
            label: "Change of ownership",
            count: 0,
            size: 0,
          },
          { color: "rgb(44,28,5)", label: "Contract expired", count: 0, size: 0 },
        ];
        for (let agg of this.deal_aggregations.current_negotiation_status) {
          switch (agg.value) {
            case "EXPRESSION_OF_INTEREST":
            case "UNDER_NEGOTIATION":
            case "MEMORANDUM_OF_UNDERSTANDING":
              retval[0].count += agg.count;
              retval[0].size += +agg.size;
              break;
            case "ORAL_AGREEMENT":
            case "CONTRACT_SIGNED":
              retval[1].count += agg.count;
              retval[1].size += +agg.size;
              break;

            case "NEGOTIATIONS_FAILED":
            case "CONTRACT_CANCELED":
              retval[2].count += agg.count;
              retval[2].size += +agg.size;
              break;
            case "CHANGE_OF_OWNERSHIP":
              retval[4].count += agg.count;
              retval[4].size += +agg.size;
              break;
            case "CONTRACT_EXPIRED":
              retval[4].count += agg.count;
              retval[4].size += +agg.size;
              break;
            default:
              console.warn({ agg });
          }
        }
        return retval;
      },

      filteredCountryProfiles(): BlogPage[] {
        if (!this.slug) return [];
        return this.articles
          .filter(
            (a) =>
              a.tags.find((t) => t.slug === this.slug) &&
              a.categories.find((c) => c.slug === "country-profile")
          )
          .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
      },
      filteredNewsPubs(): BlogPage[] {
        if (!this.slug) return [];
        return this.articles
          .filter((a) => {
            return (
              a.tags.find((t) => t.slug === this.slug) &&
              a.categories.find(
                (c) => c.slug && ["news", "publications"].includes(c.slug)
              )
            );
          })
          .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
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
    methods: {
      setGlobalLocationFilter() {
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
  });
</script>

<style lang="scss" scoped>
  .observatory {
    margin-bottom: 5em;

    h3 {
      font-size: 1.5rem;
    }

    .intro-text {
      padding-top: 1.5em;
      padding-bottom: 0.8em;

      .readmore {
        margin-top: 1.5em;
      }
    }

    .charts {
      background-color: var(--color-lm-light);
      padding: 0 0 1.5em;
      margin-top: 0;
      margin-bottom: 2rem;

      label {
        color: var(--color-lm-orange);
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
