<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { afterNavigate } from "$app/navigation"

  import { filters, FilterValues } from "$lib/filters"
  import { NegotiationStatus } from "$lib/types/deal"
  import type { ObservatoryPage } from "$lib/types/wagtail"

  import LoadingPulse from "$components/LoadingPulse.svelte"
  import QuasiStaticMap from "$components/Map/QuasiStaticMap.svelte"
  import MapDataCharts from "$components/MapDataCharts.svelte"
  import NewFooter from "$components/NewFooter.svelte"
  import PageTitle from "$components/PageTitle.svelte"
  import StatusPieChart from "$components/StatusPieChart.svelte"
  import Streamfield from "$components/Streamfield.svelte"
  import ArticleList from "$components/Wagtail/ArticleList.svelte"
  import Twitter from "$components/Wagtail/Twitter.svelte"

  export let page: ObservatoryPage

  let readMore = false
  let totalSize = ""
  let totalCount = ""
  let chartDatSize
  let chartDatCount
  let filteredCountryProfiles
  let filteredNewsPubs

  $: regionID = page.region?.id
  $: countryID = page.country?.id

  async function getAggregations() {
    let filters = new FilterValues().default()
    filters.negotiation_status = []
    filters.region_id = regionID
    filters.country_id = countryID

    const ret = await fetch(
      `/api/charts/deal_aggregations/?${filters.toRESTFilterArray()}`,
    )
    const retJson = await ret.json()
    const curNegStat = retJson.current_negotiation_status

    totalCount = curNegStat
      .map(ns => ns.count)
      .reduce((a, b) => +a + +b, 0)
      .toLocaleString("fr")

    totalSize = curNegStat
      .map(ns => ns.size)
      .reduce((a, b) => +a + +b, 0)
      .toLocaleString("fr")

    let negStatBuckets = [
      { color: "rgba(252,148,31,0.4)", label: $_("Intended"), count: 0, size: 0 },
      { color: "rgba(252,148,31,1)", label: $_("Concluded"), count: 0, size: 0 },
      { color: "rgba(125,74,15,1)", label: $_("Failed"), count: 0, size: 0 },
      { color: "rgb(44,28,5)", label: $_("Contract expired"), count: 0, size: 0 },
    ]

    for (let agg of curNegStat) {
      switch (agg.value) {
        case NegotiationStatus.EXPRESSION_OF_INTEREST:
        case NegotiationStatus.UNDER_NEGOTIATION:
        case NegotiationStatus.MEMORANDUM_OF_UNDERSTANDING:
          negStatBuckets[0].count += agg.count
          negStatBuckets[0].size += +agg.size
          break
        case NegotiationStatus.ORAL_AGREEMENT:
        case NegotiationStatus.CONTRACT_SIGNED:
        case NegotiationStatus.CHANGE_OF_OWNERSHIP:
          negStatBuckets[1].count += agg.count
          negStatBuckets[1].size += +agg.size
          break
        case NegotiationStatus.NEGOTIATIONS_FAILED:
        case NegotiationStatus.CONTRACT_CANCELED:
          negStatBuckets[2].count += agg.count
          negStatBuckets[2].size += +agg.size
          break
        case NegotiationStatus.CONTRACT_EXPIRED:
          negStatBuckets[3].count += agg.count
          negStatBuckets[3].size += +agg.size
          break
        default:
          console.warn({ agg })
      }
    }
    chartDatSize = {
      labels: negStatBuckets.map(n => n.label),
      datasets: [
        {
          data: negStatBuckets.map(n => n["size"]),
          backgroundColor: negStatBuckets.map(n => n.color),
        },
      ],
    }
    chartDatCount = {
      labels: negStatBuckets.map(n => n.label),
      datasets: [
        {
          data: negStatBuckets.map(n => n["count"]),
          backgroundColor: negStatBuckets.map(n => n.color),
        },
      ],
    }
  }

  afterNavigate(() => {
    readMore = false
    getAggregations()
  })
  $: filteredCountryProfiles = page.related_blogpages.filter(p =>
    p.categories.find(c => c.slug && c.slug === "country-profile"),
  )
  $: filteredNewsPubs = page.related_blogpages.filter(p =>
    p.categories.find(c => c.slug && (c.slug === "news" || c.slug === "publications")),
  )

  const setGlobalLocationFilter = () => {
    if (page.region) {
      $filters.region_id = regionID
      $filters.country_id = undefined
    } else if (page.country) {
      $filters.region_id = undefined
      $filters.country_id = countryID
    }
  }
</script>

<PageTitle>{$_(page.title)}</PageTitle>

<div class="mx-auto w-[clamp(20rem,75%,56rem)]">
  <QuasiStaticMap {countryID} markers={page.markers} {regionID} />

  {#if page.introduction_text}
    <div class="pb-3 pt-6">
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
        <div transition:slide>
          <Streamfield content={page.body} class="px-0" />
        </div>
      {/if}
    </div>
  {/if}
</div>

<div class="mb-8 mt-2 bg-gray-50 py-6 dark:bg-gray-700">
  <div class="mx-auto min-h-[300px] w-[clamp(20rem,75%,56rem)]">
    {#if totalSize === ""}
      <LoadingPulse class="h-[300px]" />
    {:else}
      <h3 class="pb-2">{$_("We currently have information about:")}</h3>
      <div class="grid gap-8 font-bold last:mb-8 sm:grid-cols-2">
        <div class="text-center">
          <div class="text-orange">{$_("Size")}</div>
          <div class="mb-2">{totalSize} ha</div>
          <div class="mx-auto max-w-[80%]">
            <StatusPieChart data={chartDatSize} unit="ha" />
          </div>
        </div>
        <div class="text-center">
          <div class="text-orange">{$_("Number of deals")}</div>
          <div class="mb-2">{totalCount}</div>
          <div class="mx-auto max-w-[80%]">
            <StatusPieChart data={chartDatCount} />
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>

<div class="mx-auto w-[clamp(20rem,75%,56rem)]">
  <MapDataCharts on:click={setGlobalLocationFilter} />
</div>

<div class="container mx-auto my-8 w-[clamp(20rem,75%,56rem)]">
  <h3 class="heading4 mb-3">{$_("Country profiles")}</h3>
  <div>
    <p>
      {$_(
        "Country profiles present national-level data of large-scale land acquisitions and transactions including who the investors are, what the aim of the investment is, who the former owner was and what the land was previously used for, and what the potential benefits and impacts of the land deals are.",
      )}
    </p>
    <p>
      {$_(
        "By making this information available, the Land Matrix hopes to enhance broad engagement and data exchange, facilitating the continuous improvement of the data. Find out how to get involved",
      )}
      <a href="/contribute">{$_("here")}</a>
      .
    </p>
    <h4 class="heading5">{$_("Download country profiles for")}:</h4>
  </div>
  <ArticleList articles={filteredCountryProfiles} />
</div>

<div class="container mx-auto my-8 w-[clamp(20rem,75%,56rem)]">
  <h3 class="heading4 mb-3">{$_("News & publications")}</h3>
  <ArticleList articles={filteredNewsPubs} />
</div>

{#if page.twitter_feed}
  <div class="container mx-auto mb-8 w-[clamp(20rem,75%,56rem)]">
    <h3>{$_("Latest tweets")}</h3>
    <Twitter twitterFeed={page.twitter_feed} />
  </div>
{/if}

<NewFooter />
