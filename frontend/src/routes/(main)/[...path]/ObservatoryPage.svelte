<script lang="ts">
  import { _ } from "svelte-i18n"
  import { slide } from "svelte/transition"

  import { afterNavigate } from "$app/navigation"

  import { dealChoices } from "$lib/fieldChoices"
  import { filters, FilterValues } from "$lib/filters"
  import { NegotiationStatusGroup, type NegotiationStatus } from "$lib/types/data"
  import type { BlogPage, ObservatoryPage } from "$lib/types/wagtail"

  import LoadingPulse from "$components/LoadingPulse.svelte"
  import QuasiStaticMap from "$components/Map/QuasiStaticMap.svelte"
  import MapDataCharts from "$components/MapDataCharts.svelte"
  import NewFooter from "$components/NewFooter.svelte"
  import PageTitle from "$components/PageTitle.svelte"
  import StatusBarChart, { type DataType } from "$components/StatusBarChart.svelte"
  import Streamfield from "$components/Streamfield.svelte"
  import ArticleList from "$components/Wagtail/ArticleList.svelte"
  import Twitter from "$components/Wagtail/Twitter.svelte"

  interface Props {
    page: ObservatoryPage
  }

  let { page }: Props = $props()

  let readMore = $state(false)

  let filteredCountryProfiles: BlogPage[] = $derived(
    (page.related_blogpages ?? []).filter(p =>
      p.categories.find(c => c.slug && c.slug === "country-profile"),
    ),
  )
  let filteredNewsPubs: BlogPage[] = $derived(
    (page.related_blogpages ?? []).filter(p =>
      p.categories.find(
        c => c.slug && (c.slug === "news" || c.slug === "publications"),
      ),
    ),
  )

  let regionID = $derived(page.region?.id)
  let countryID = $derived(page.country?.id)

  const colorsMap: { [key in NegotiationStatusGroup]: string } = {
    // TODO use HSL
    INTENDED: "hsl(93, 55%, 75%)", //"text-green-300",
    CONCLUDED: "hsl(94, 56%, 65%)", //"text-green-500",
    FAILED: "hsl(0, 73%, 66%)", //"text-red-500",
    CONTRACT_EXPIRED: "hsl(0, 0%, 60%)", //"text-gray-300",
  }

  let currentNegStatus: { value: NegotiationStatus; count: number; size: number }[] =
    $state([])
  const _fetchCurrentNegStatus = async (rgnID?: number, cntryID?: number) => {
    let filters = new FilterValues().default()
    filters.negotiation_status = []
    filters.region_id = rgnID
    filters.country_id = cntryID

    const ret = await fetch(
      `/api/charts/deal_aggregations/?${filters.toRESTFilterArray()}`,
    )
    const retJson = await ret.json()
    currentNegStatus = retJson.current_negotiation_status
  }
  $effect(() => {
    _fetchCurrentNegStatus(regionID, countryID)
  })

  let totalSize = $derived(
    currentNegStatus.map(ns => ns.size).reduce((a, b) => +a + +b, 0),
  )
  let totalCount = $derived(
    currentNegStatus.map(ns => ns.count).reduce((a, b) => +a + +b, 0),
  )

  let negStatBuckets = $derived.by(() => {
    let _negStatBuckets = $dealChoices.negotiation_status_group.map(x => ({
      // TODO: Try to type fieldChoices (or create a generic interface) to avoid casting explicitly
      fillColor: colorsMap[x.value as NegotiationStatusGroup],
      name: x.label,
      count: 0,
      size: 0,
    }))
    for (let agg of currentNegStatus) {
      switch (agg.value) {
        case "EXPRESSION_OF_INTEREST":
        case "UNDER_NEGOTIATION":
        case "MEMORANDUM_OF_UNDERSTANDING":
          _negStatBuckets[0].count += agg.count
          _negStatBuckets[0].size += +agg.size
          break
        case "ORAL_AGREEMENT":
        case "CONTRACT_SIGNED":
        case "CHANGE_OF_OWNERSHIP":
          _negStatBuckets[1].count += agg.count
          _negStatBuckets[1].size += +agg.size
          break
        case "NEGOTIATIONS_FAILED":
        case "CONTRACT_CANCELED":
          _negStatBuckets[2].count += agg.count
          _negStatBuckets[2].size += +agg.size
          break
        case "CONTRACT_EXPIRED":
          _negStatBuckets[3].count += agg.count
          _negStatBuckets[3].size += +agg.size
          break
        default:
          console.warn({ agg })
      }
    }
    return _negStatBuckets
  })
  const chartDatSize: DataType[] = $derived(
    negStatBuckets.map(n => ({
      name: n.name,
      value: ((n.size / totalSize) * 100).toFixed(),
      label: `<strong>${n.name}</strong>: ${n.size.toLocaleString("fr").replace(",", ".")} ${$_("ha")}`,
      fillColor: n.fillColor,
    })),
  )
  const chartDatCount: DataType[] = $derived(
    negStatBuckets.map(n => ({
      name: n.name,
      value: ((n.count / totalCount) * 100).toFixed(),
      label: `<strong>${n.name}</strong>: ${n.count.toFixed()} ${$_("deals")}`,
      fillColor: n.fillColor,
    })),
  )

  // QUESTION: Wouldn't it make sense to keep navigation stuff in +page.svelte ?
  afterNavigate(() => {
    readMore = false
  })

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

<PageTitle>{page.title}</PageTitle>

<div class="mx-auto w-[clamp(20rem,75%,56rem)]">
  {#key page.id}
    <QuasiStaticMap {countryID} markers={page.markers} {regionID} />
  {/key}

  {#if page.introduction_text}
    <div class="pb-3 pt-6">
      <div class="intro">
        {page.introduction_text}
      </div>
      {#if !readMore}
        <div class="mt-6">
          <button onclick={() => (readMore = true)} class="text-orange" type="button">
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
  <div class="mx-auto min-h-[240px] w-[clamp(20rem,75%,56rem)]">
    {#if totalSize === -1}
      <LoadingPulse class="h-[300px]" />
    {:else}
      <h3 class="pb-2">{$_("We currently have information about:")}</h3>
      <div class="grid gap-8 font-bold last:mb-8 lg:grid-cols-2 lg:last:mb-4">
        <div class="text-center">
          <div class="text-orange">{$_("Size")}</div>
          <div class="mb-2">{totalSize.toLocaleString("fr").replace(",", ".")} ha</div>
          <div class="mx-auto max-w-[80%]">
            {#key chartDatSize}
              <div class="p-4">
                <StatusBarChart data={chartDatSize} width={400} />
              </div>
            {/key}
          </div>
        </div>
        <div class="text-center">
          <div class="text-orange">{$_("Number of deals")}</div>
          <div class="mb-2">{totalCount.toLocaleString("fr").replace(",", ".")}</div>
          <div class="mx-auto max-w-[80%]">
            {#key chartDatCount}
              <div class="p-4">
                <StatusBarChart data={chartDatCount} width={400} />
              </div>
            {/key}
          </div>
        </div>
      </div>
    {/if}
  </div>
</div>

<div class="mx-auto w-[clamp(20rem,75%,56rem)]">
  <MapDataCharts onclick={setGlobalLocationFilter} />
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
