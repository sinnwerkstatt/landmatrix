import { _, t } from "svelte-i18n";
import { get } from "svelte/store";
import { ImplementationStatus, NegotiationStatusGroupMap } from "$lib/filters";
import type { Deal } from "$lib/types/deal";
import { formfields } from "../../lib/stores";

export function calcNegotiationStatusChart(deals: Deal[], displayDealsCount: boolean) {
  const $_ = get(t);

  const negStatBuckets = {
    INTENDED: { count: 0, size: 0 },
    CONCLUDED: { count: 0, size: 0 },
    FAILED: { count: 0, size: 0 },
    CHANGE_OF_OWNERSHIP: { count: 0, size: 0 },
    CONTRACT_EXPIRED: { count: 0, size: 0 },
  };
  for (const d of deals ?? []) {
    const group = NegotiationStatusGroupMap[d.current_negotiation_status];
    const buck = negStatBuckets[group];
    if (buck) {
      buck.count += 1;
      buck.size += d.deal_size;
    }
  }
  return {
    labels: [
      $_("Intended"),
      $_("Concluded"),
      $_("Failed"),
      $_("Change of ownership"),
      $_("Contract expired"),
    ],
    datasets: [
      {
        data: Object.values(negStatBuckets).map((n) =>
          displayDealsCount ? n["count"] : n["size"]
        ),
        backgroundColor: [
          "rgba(252,148,31,0.4)",
          "rgba(252,148,31,1)",
          "rgba(125,74,15,1)",
          "rgb(59,36,8)",
          "rgb(44,28,5)",
        ],
      },
    ],
  };
}

export function calcImplementationStatusChart(
  deals: Deal[],
  displayDealsCount: boolean
) {
  const $_ = get(t);
  const impStatBuckets = {
    PROJECT_NOT_STARTED: { count: 0, size: 0 },
    STARTUP_PHASE: { count: 0, size: 0 },
    IN_OPERATION: { count: 0, size: 0 },
    PROJECT_ABANDONED: { count: 0, size: 0 },
  };
  for (const d of deals ?? []) {
    const buck = impStatBuckets[d.current_implementation_status];
    if (buck) {
      buck.count += 1;
      buck.size += d.deal_size;
    }
  }
  return {
    labels: [
      $_("Project not started"),
      $_("Start-up phase (no production)"),
      $_("In operation (production)"),
      $_("Project abandoned"),
    ],
    datasets: [
      {
        data: Object.values(impStatBuckets).map((n) =>
          displayDealsCount ? n["count"] : n["size"]
        ),
        backgroundColor: [
          "rgba(252,148,31,0.4)",
          "rgba(252,148,31,0.7)",
          "rgba(252,148,31,1)",
          "#7D4A0F",
        ],
      },
    ],
  };
}

export function calcProduceChart(deals: Deal[], displayDealsCount: boolean) {
  const $_ = get(t);

  const produceLabelMap = {
    ...get(formfields).deal.crops.choices,
    ...get(formfields).deal.animals.choices,
    ...get(formfields).deal.mineral_resources.choices,
  };
  const data: unknown[] = [];
  const fields = ["crops", "animals", "mineral_resources"];
  // if (produceLabelMap && this.dealsWithProduceInfo.length) {
  //   const counts = {};
  //   for (const deal of this.dealsWithProduceInfo) {
  //     for (const field of fields) {
  //       counts[field] = counts[field] || [];
  //       if (deal["current_" + field]) {
  //         for (const key of deal["current_" + field]) {
  //           counts[field][key] = counts[field][key] + 1 || 1;
  //         }
  //       }
  //     }
  //   }
  //   for (const field of fields) {
  //     for (const [key, count] of Object.entries(counts[field])) {
  //       if (count > 1) {
  //         data.push({
  //           label: key,
  //           color: colors[fields.indexOf(field)],
  //           value: count,
  //         });
  //       }
  //     }
  //   }
  //   data.sort((a, b) => {
  //     return b.value - a.value;
  //   });
  //   const totalCount = sum(data, "value");
  //   const cutOffIndex = Math.min(15, data.length);
  //   const other = data.slice(cutOffIndex, data.length);
  //   data = data.slice(0, cutOffIndex);
  //   for (const d of data) {
  //     if (d.label in this.produceLabelMap) {
  //       d.label = this.produceLabelMap[d.label];
  //     }
  //     d.value = (d.value / totalCount) * 100;
  //     d.unit = "%";
  //     d.precision = 1;
  //   }
  //   if (other.length) {
  //     const otherCount = sum(other, "value");
  //     data.push({
  //       label: "Other",
  //       color: "rgba(252,148,31,0.4)",
  //       value: (otherCount / totalCount) * 100,
  //       unit: "%",
  //       precision: 1,
  //     });
  //   }
  // }
  return {
    labels: [$_("Crops"), $_("Livestock"), $_("Mineral resources")],
    datasets: [{ data, backgroundColor: ["#FC941F", "#7D4A0F", "#000000"] }],
  };
}
