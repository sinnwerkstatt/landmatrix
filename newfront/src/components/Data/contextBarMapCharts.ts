import { t } from "svelte-i18n";
import { get } from "svelte/store";
import { NegotiationStatusGroup, NegotiationStatusGroupMap } from "$lib/filters";
import { formfields } from "$lib/stores";
import type { Deal } from "$lib/types/deal";

export function calcNegotiationStatusChart(deals: Deal[], displayDealsCount: boolean) {
  const $_ = get(t);

  const negStatBuckets = {
    [NegotiationStatusGroup.INTENDED]: { count: 0, size: 0 },
    [NegotiationStatusGroup.CONCLUDED]: { count: 0, size: 0 },
    [NegotiationStatusGroup.FAILED]: { count: 0, size: 0 },
    [NegotiationStatusGroup.CONTRACT_EXPIRED]: { count: 0, size: 0 },
  };
  for (const d of deals ?? []) {
    if (!d.current_negotiation_status || !d.deal_size) {
      continue;
    }
    const group = NegotiationStatusGroupMap[d.current_negotiation_status];
    const buck = negStatBuckets[group];
    if (buck) {
      buck.count += 1;
      buck.size += d.deal_size;
    }
  }
  return {
    labels: [$_("Intended"), $_("Concluded"), $_("Failed"), $_("Contract expired")],
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
    if (!d.current_implementation_status || !d.deal_size) {
      continue;
    }
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

enum ProduceFields {
  CROPS = "current_crops",
  ANIMALS = "current_animals",
  MINERAL_RESOURCES = "current_mineral_resources",
}

const ProduceLabels = {
  [ProduceFields.CROPS]: "Crops",
  [ProduceFields.ANIMALS]: "Livestock",
  [ProduceFields.MINERAL_RESOURCES]: "Mineral resources",
};

const ProduceColors = {
  [ProduceFields.CROPS]: "#FC941F",
  [ProduceFields.ANIMALS]: "#7D4A0F",
  [ProduceFields.MINERAL_RESOURCES]: "#000000",
};

export function calcProduceChart(deals: Deal[]) {
  const $_ = get(t);

  const dealsWithProduceInfo =
    deals?.filter((deal) =>
      Object.values(ProduceFields).some((field) => deal[field])
    ) ?? [];

  const buckets = {
    [ProduceFields.CROPS]: 0,
    [ProduceFields.ANIMALS]: 0,
    [ProduceFields.MINERAL_RESOURCES]: 0,
  };

  for (const deal of dealsWithProduceInfo) {
    for (const field of Object.values(ProduceFields)) {
      if (deal[field]) {
        buckets[field] += 1;
      }
    }
  }

  const total = Object.values(buckets).reduce((acc, current) => acc + current);
  const sortedEntries = Object.entries(buckets).sort((a, b) => a[1] - b[1]) as [
    ProduceFields,
    number
  ][];

  return {
    labels: sortedEntries.map(([key, _]) => $_(ProduceLabels[key])),
    datasets: [
      {
        data: sortedEntries.map(([_, value]) => (value / total) * 100),
        backgroundColor: sortedEntries.map(([key, _]) => ProduceColors[key]),
      },
    ],
  };
}
