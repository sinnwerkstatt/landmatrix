<script lang="ts">
  // import { implementation_status_choices } from "$utils/choices";
  //  import { prepareNegotianStatusData, sum } from "$utils/data_processing";
  // import { data_deal_produce_query, data_deal_query } from "$views/Data/query";
  import Pie from "svelte-chartjs/src/Pie.svelte";
  import { _ } from "svelte-i18n";
  import { deals } from "$lib/data";
  import { filters } from "$lib/filters";
  import { countries, formfields, observatoryPages, regions } from "$lib/stores";
  import type { Deal } from "$lib/types/deal";
  import type { CountryOrRegion } from "$lib/types/wagtail";
  import { prepareNegotianStatusData, sum } from "$lib/utils/data_processing";
  import DealDisplayToggle from "$components/DealDisplayToggle.svelte";
  import { displayDealsCount } from "$components/Map/map_helper";
  import ContextBarContainer from "./ContextBarContainer.svelte";

  let dealsWithProduceInfo: Deal[] = [];

  let chartNegStat;
  let chartImpStat;
  let chartProd;

  let currentItem: CountryOrRegion;
  $: if (!$filters.region_id && !$filters.country_id) {
    currentItem = {
      name: "Global",
      observatory: $observatoryPages.find((o) => !o.country && !o.region),
    };
  } else {
    currentItem = $filters.region_id
      ? $regions.find((r) => r.id === $filters.region_id)
      : $countries.find((c) => c.id === $filters.country_id);
    currentItem.observatory = $observatoryPages.find(
      (o) => o.id === currentItem.observatory_page_id
    );
  }

  let negStatBuckets = [
    { color: "rgba(252,148,31,0.4)", label: "Intended", count: 0, size: 0 },
    { color: "rgba(252,148,31,1)", label: "Concluded", count: 0, size: 0 },
    { color: "rgb(44,28,5)", label: "Failed", count: 0, size: 0 },
    //{ color: "rgb(59,36,8)", label: "Change of ownership", count: 0, size: 0 },
    //{ color: "rgb(44,28,5)", label: "Contract expired", count: 0, size: 0 },
  ];

  chartNegStat = {
    labels: negStatBuckets.map((n) => n.label),
    datasets: [
      {
        data: negStatBuckets.map((n) => n["size"]),
        backgroundColor: negStatBuckets.map((n) => n.color),
      },
    ],
  };

  $: totalCount = $displayDealsCount
    ? `${Math.round($deals?.length).toLocaleString("fr")}`
    : `${Math.round(sum($deals, "deal_size")).toLocaleString("fr")} ha`;

  //$: dealsFilteredByNegStatus = prepareNegotianStatusData($deals);
  // $: negotiationStatusData = () => {
  //   if ($displayDealsCount) {
  //     return this.dealsFilteredByNegStatus.map((d) => {
  //       return { value: d.count, unit: "deals", ...d };
  //     });
  //   } else {
  //     return this.dealsFilteredByNegStatus.map((d) => {
  //       return { value: d.size, unit: "ha", ...d };
  //     });
  //   }
  // };
  // $: implementationStatusData = () => {
  //   let data = [];
  //   if (this.deals.length) {
  //     let i = 0;
  //     let colors = [
  //       "rgba(252,148,31,0.4)",
  //       "rgba(252,148,31,0.7)",
  //       "rgba(252,148,31,1)",
  //       "#7D4A0F",
  //     ];
  //     for (const [key, label] of Object.entries(implementation_status_choices)) {
  //       let filteredDeals = $deals.filter((d) => {
  //         return d.current_implementation_status === key;
  //       });
  //       data.push({
  //         label: label,
  //         color: colors[i],
  //         value: $displayDealsCount
  //           ? filteredDeals.length
  //           : sum(filteredDeals, "deal_size"),
  //         unit: $displayDealsCount ? "deals" : "ha",
  //       });
  //       i++;
  //     }
  //   }
  //   return data;
  // };
  // $: produceData = () => {
  //   let data = [];
  //   let fields = ["crops", "animals", "mineral_resources"];
  //   let colors = ["#FC941F", "#7D4A0F", "black"];
  //   if (this.produceLabelMap && this.dealsWithProduceInfo.length) {
  //     let counts = {};
  //     for (let deal of this.dealsWithProduceInfo) {
  //       for (let field of fields) {
  //         counts[field] = counts[field] || [];
  //         if (deal["current_" + field]) {
  //           for (let key of deal["current_" + field]) {
  //             counts[field][key] = counts[field][key] + 1 || 1;
  //           }
  //         }
  //       }
  //     }
  //     for (let field of fields) {
  //       for (const [key, count] of Object.entries(counts[field])) {
  //         if (count > 1) {
  //           data.push({
  //             label: key,
  //             color: colors[fields.indexOf(field)],
  //             value: count,
  //           });
  //         }
  //       }
  //     }
  //     data.sort((a, b) => {
  //       return b.value - a.value;
  //     });
  //     let totalCount = sum(data, "value");
  //     let cutOffIndex = Math.min(15, data.length);
  //     let other = data.slice(cutOffIndex, data.length);
  //     data = data.slice(0, cutOffIndex);
  //     for (let d of data) {
  //       if (d.label in this.produceLabelMap) {
  //         d.label = this.produceLabelMap[d.label];
  //       }
  //       d.value = (d.value / totalCount) * 100;
  //       d.unit = "%";
  //       d.precision = 1;
  //     }
  //     if (other.length) {
  //       let otherCount = sum(other, "value");
  //       data.push({
  //         label: "Other",
  //         color: "rgba(252,148,31,0.4)",
  //         value: (otherCount / totalCount) * 100,
  //         unit: "%",
  //         precision: 1,
  //       });
  //     }
  //   }
  //   return data;
  // };

  const produceLabelMap = {
    ...$formfields.deal.crops.choices,
    ...$formfields.deal.animals.choices,
    ...$formfields.deal.mineral_resources.choices,
  };
  const produceDataLegendItems = [
    {
      label: $_("Crops"),
      color: "#FC941F",
    },
    {
      label: $_("Livestock"),
      color: "#7D4A0F",
    },
    {
      label: $_("Mineral resources"),
      color: "black",
    },
  ];

  console.log(produceLabelMap);
</script>

<ContextBarContainer>
  {#if currentItem}
    <h2 class="font-bold text-lg my-3 leading-5">{currentItem.name}</h2>
    {#if currentItem?.observatory}
      <p class="mb-1">
        {currentItem.observatory.short_description}
        <br />
        <a href="/observatory/{currentItem.observatory.meta.slug}/">
          {$_("Read more")}
        </a>
      </p>
    {/if}
  {/if}
  {#if $deals?.length}
    <div>
      <DealDisplayToggle />
      <div class="w-full text-center font-bold my-3">
        {totalCount}
      </div>
      <div class="w-full mb-3">
        <h5 class="text-left text-lg mt-4">{$_("Negotiation status")}</h5>
        <Pie data={chartNegStat} options={{ responsive: true, aspectRatio: 1 }} />
        <!--        <p class="hint-box">The negotiation status is filtered at the moment.</p>-->
        <!--        <StatusPieChart-->
        <!--          :deal-data="dealsFilteredByNegStatus"-->
        <!--          :value-field="$displayDealsCount ? 'count' : 'size'"-->
        <!--          :unit="$displayDealsCount ? 'deals' : 'ha'"-->
        <!--        />-->
      </div>
      <div class="w-full mb-3">
        <h5 class="text-left text-lg mt-4">{$_("Implementation status")}</h5>
        <Pie data={chartImpStat} options={{ responsive: true, aspectRatio: 1 }} />

        <!--        <StatusPieChart-->
        <!--          :deal-data="implementationStatusData"-->
        <!--          value-field="value"-->
        <!--          :unit="$displayDealsCount ? 'deals' : 'ha'"-->
        <!--        />-->
      </div>
      <div class="w-full mb-3">
        <h5 class="text-left text-lg mt-4">{$_("Produce")}</h5>
        <Pie data={chartProd} options={{ responsive: true, aspectRatio: 1 }} />

        <!--        <StatusPieChart-->
        <!--          :deal-data="produceData"-->
        <!--          :legends="produceDataLegendItems"-->
        <!--          unit="%"-->
        <!--        />-->
      </div>
    </div>
  {/if}
</ContextBarContainer>
