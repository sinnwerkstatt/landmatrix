<script lang="ts">
  import { gql, request } from "graphql-request";
  import Pie from "svelte-chartjs/src/Pie.svelte";
  import { _ } from "svelte-i18n";
  import { afterNavigate } from "$app/navigation";
  import { GQLEndpoint } from "$lib";
  import { defaultFilterValues, filters, NegotiationStatus } from "$lib/filters";
  import { getCountryOrRegion } from "$lib/helpers";
  import { user } from "$lib/stores";
  import type { BlogPage, ObservatoryPage } from "$lib/types/wagtail";
  import LoadingPulse from "$components/LoadingPulse.svelte";
  import QuasiStaticMap from "$components/Map/QuasiStaticMap.svelte";
  import MapDataCharts from "$components/MapDataCharts.svelte";
  import PageTitle from "$components/PageTitle.svelte";
  import Streamfield from "$components/Streamfield.svelte";
  import ArticleList from "$components/Wagtail/ArticleList.svelte";
  import Twitter from "$components/Wagtail/Twitter.svelte";

  export let page: ObservatoryPage;

  let readMore = false;
  let articles: BlogPage[] = [];
  let totalSize = "";
  let totalCount = "";
  let chartDatSize;
  let chartDatCount;
  let filteredCountryProfiles;
  let filteredNewsPubs;

  $: regionID = page.region ? page.region.id : undefined;
  $: countryID = page.country ? page.country.id : undefined;
  $: roc = regionID
    ? getCountryOrRegion(regionID, true)
    : getCountryOrRegion(countryID);
  $: slug = roc?.slug ?? "";

  async function getAggregations() {
    const q = gql`
      query DealAggregations($fields: [String]!, $subset: Subset, $filters: [Filter]) {
        deal_aggregations(fields: $fields, subset: $subset, filters: $filters) {
          current_negotiation_status {
            value
            size
            count
          }
        }
      }
    `;

    let filters = defaultFilterValues();
    filters.negotiation_status = [];
    filters.region_id = regionID;
    filters.country_id = countryID;

    const variables = {
      fields: ["current_negotiation_status"],
      filters: filters.toGQLFilterArray(),
      subset: $user?.is_authenticated ? "ACTIVE" : "PUBLIC",
    };
    const result = await request(GQLEndpoint, q, variables);
    const curNegStat = result.deal_aggregations.current_negotiation_status;
    // const curNegStat = page.current_negotiation_status_metrics
    totalCount = curNegStat
      .map((ns) => ns.count)
      .reduce((a, b) => +a + +b, 0)
      .toLocaleString("fr");

    totalSize = curNegStat
      .map((ns) => ns.size)
      .reduce((a, b) => +a + +b, 0)
      .toLocaleString("fr");

    let negStatBuckets = [
      { color: "rgba(252,148,31,0.4)", label: "Intended", count: 0, size: 0 },
      { color: "rgba(252,148,31,1)", label: "Concluded", count: 0, size: 0 },
      { color: "rgba(125,74,15,1)", label: "Failed", count: 0, size: 0 },
      { color: "rgb(59,36,8)", label: "Change of ownership", count: 0, size: 0 },
      { color: "rgb(44,28,5)", label: "Contract expired", count: 0, size: 0 },
    ];

    for (let agg of curNegStat) {
      switch (agg.value) {
        case NegotiationStatus.EXPRESSION_OF_INTEREST:
        case NegotiationStatus.UNDER_NEGOTIATION:
        case NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING:
          negStatBuckets[0].count += agg.count;
          negStatBuckets[0].size += +agg.size;
          break;
        case NegotiationStatus.ORAL_AGREEMENT:
        case NegotiationStatus.CONTRACT_SIGNED:
          negStatBuckets[1].count += agg.count;
          negStatBuckets[1].size += +agg.size;
          break;

        case NegotiationStatus.NEGOTIATIONS_FAILED:
        case NegotiationStatus.CONTRACT_CANCELED:
          negStatBuckets[2].count += agg.count;
          negStatBuckets[2].size += +agg.size;
          break;
        case NegotiationStatus.CHANGE_OF_OWNERSHIP:
          negStatBuckets[4].count += agg.count;
          negStatBuckets[4].size += +agg.size;
          break;
        case NegotiationStatus.CONTRACT_EXPIRED:
          negStatBuckets[4].count += agg.count;
          negStatBuckets[4].size += +agg.size;
          break;
        default:
          console.warn({ agg });
      }
    }
    chartDatSize = {
      labels: negStatBuckets.map((n) => n.label),
      datasets: [
        {
          data: negStatBuckets.map((n) => n["size"]),
          backgroundColor: negStatBuckets.map((n) => n.color),
        },
      ],
    };
    chartDatCount = {
      labels: negStatBuckets.map((n) => n.label),
      datasets: [
        {
          data: negStatBuckets.map((n) => n["count"]),
          backgroundColor: negStatBuckets.map((n) => n.color),
        },
      ],
    };
  }

  afterNavigate(() => {
    readMore = false;
    getAggregations();
  });
  filteredCountryProfiles = page.related_blogpages.filter((p) =>
    p.categories.find((c) => c.slug && c.slug === "country-profile")
  );
  filteredNewsPubs = page.related_blogpages.filter((p) =>
    p.categories.find((c) => c.slug && (c.slug === "news" || c.slug === "publications"))
  );

  const setGlobalLocationFilter = () => {
    if (page.region) {
      filters.set({ filter: "region_id", value: regionID });
      filters.set({ filter: "country_id", value: null });
    } else if (page.country) {
      filters.set({ filter: "country_id", value: countryID });
      filters.set({ filter: "region_id", value: null });
    }
  };
</script>

<PageTitle>{$_(page.title)}</PageTitle>

<div class="mx-auto w-[clamp(20rem,75%,56rem)]">
  <QuasiStaticMap {countryID} {regionID} />

  {#if page.introduction_text}
    <div class="pt-6 pb-3">
      <div class="intro">
        {page.introduction_text}
      </div>
      {#if !readMore}
        <div class="mt-6">
          <button on:click|preventDefault={() => (readMore = true)} class="text-orange">
            {$_("Read more")}
          </button>
        </div>
      {:else}
        <div class="mx-auto max-w-[65ch]">
          <Streamfield content={page.body} />
        </div>
      {/if}
    </div>
  {/if}
</div>

<div class="charts bg-lm-light mt-0 mb-8 p-0 pb-6">
  <div class="mx-auto w-[clamp(20rem,75%,56rem)] min-h-[300px]">
    {#if totalSize === ""}
      <LoadingPulse class="h-[300px]" />
    {:else}
      <h3>{$_("We currently have information about:")}</h3>
      <div class="grid md:grid-cols-2 font-bold">
        <div class="text-center">
          <div class="text-orange">{$_("Size")}</div>
          <div class=" mb-2">{totalSize} ha</div>
          <div class="mx-auto max-w-[80%]">
            <Pie data={chartDatSize} options={{ responsive: true, aspectRatio: 1 }} />
            <!-- <StatusPieChart unit="ha" />-->
          </div>
        </div>
        <div class="text-center">
          <div class="text-orange">{$_("Number of deals")}</div>
          <div class="  mb-2">{totalCount}</div>
          <div class="mx-auto max-w-[80%]">
            <Pie data={chartDatCount} options={{ responsive: true, aspectRatio: 1 }} />
            <!-- <StatusPieChart />-->
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>

<div class="mx-auto w-[clamp(20rem,75%,56rem)]">
  <MapDataCharts on:click={setGlobalLocationFilter} />
</div>

<ArticleList articles={filteredCountryProfiles} articlesLabel={$_("Country profiles")}>
  <div class="description">
    <p>
      {$_(
        "Country profiles present national-level data of large-scale land acquisitions and transactions including who the investors are, what the aim of the investment is, who the former owner was and what the land was previously used for, and what the potential benefits and impacts of the land deals are."
      )}
    </p>
    <p>
      {$_(
        "By making this information available, the Land Matrix hopes to enhance broad engagement and data exchange, facilitating the continuous improvement of the data. Find out how to get involved"
      )}
      <a href="/contribute">{$_("here")}</a>
      .
    </p>
    <h4>{$_("Download country profiles for")}:</h4>
  </div>
</ArticleList>
<ArticleList articles={filteredNewsPubs} articlesLabel={$_("News & publications")} />

{#if page.twitter_feed}
  <div class="mx-auto container w-[clamp(20rem,75%,56rem)] mb-8">
    <h3>{$_("Latest tweets")}</h3>
    <Twitter twitterFeed={page.twitter_feed} />
  </div>
{/if}
