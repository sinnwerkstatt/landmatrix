import { t } from "svelte-i18n";
import { get } from "svelte/store";
import {
  ImplementationStatus,
  NegotiationStatusGroup,
  NegotiationStatusGroupMap,
  ProduceGroup,
} from "$lib/filters";
import type { Deal } from "$lib/types/deal";

const NegotiationStatusColors = {
  [NegotiationStatusGroup.INTENDED]: "rgba(252,148,31,0.4)",
  [NegotiationStatusGroup.CONCLUDED]: "rgba(252,148,31,1)",
  [NegotiationStatusGroup.FAILED]: "rgba(125,74,15,1)",
  [NegotiationStatusGroup.CONTRACT_EXPIRED]: "rgb(59,36,8)",
};

const NegotiationStatusLabels = {
  [NegotiationStatusGroup.INTENDED]: "Intended",
  [NegotiationStatusGroup.CONCLUDED]: "Concluded",
  [NegotiationStatusGroup.FAILED]: "Failed",
  [NegotiationStatusGroup.CONTRACT_EXPIRED]: "Contract expired",
};

const ImplementationStatusLabels = {
  [ImplementationStatus.PROJECT_NOT_STARTED]: "Project not started",
  [ImplementationStatus.STARTUP_PHASE]: "Start-up phase (no production)",
  [ImplementationStatus.IN_OPERATION]: "In operation (production)",
  [ImplementationStatus.PROJECT_ABANDONED]: "Project abandoned",
};

const ImplementationStatusColors = {
  [ImplementationStatus.PROJECT_NOT_STARTED]: "rgba(252,148,31,0.4)",
  [ImplementationStatus.STARTUP_PHASE]: "rgba(252,148,31,0.7)",
  [ImplementationStatus.IN_OPERATION]: "rgba(252,148,31,1)",
  [ImplementationStatus.PROJECT_ABANDONED]: "#7D4A0F",
};

const ProduceLabels = {
  [ProduceGroup.CROPS]: "Crops",
  [ProduceGroup.ANIMALS]: "Livestock",
  [ProduceGroup.MINERAL_RESOURCES]: "Mineral resources",
};

const ProduceColors = {
  [ProduceGroup.CROPS]: "#FC941F",
  [ProduceGroup.ANIMALS]: "#7D4A0F",
  [ProduceGroup.MINERAL_RESOURCES]: "#000000",
};

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
  const sortedEntries = Object.entries(negStatBuckets)
    .map(
      ([key, bucket]) =>
        [key, displayDealsCount ? bucket.count : bucket.size] as [
          NegotiationStatusGroup,
          number
        ]
    )
    .sort((a, b) => a[1] - b[1]);

  return {
    labels: sortedEntries.map(([key, _]) => $_(NegotiationStatusLabels[key])),
    datasets: [
      {
        data: sortedEntries.map(([_, value]) => value),
        backgroundColor: sortedEntries.map(([key, _]) => NegotiationStatusColors[key]),
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
    [ImplementationStatus.PROJECT_NOT_STARTED]: { count: 0, size: 0 },
    [ImplementationStatus.STARTUP_PHASE]: { count: 0, size: 0 },
    [ImplementationStatus.IN_OPERATION]: { count: 0, size: 0 },
    [ImplementationStatus.PROJECT_ABANDONED]: { count: 0, size: 0 },
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
  const sortedEntries = Object.entries(impStatBuckets)
    .map(
      ([key, bucket]) =>
        [key, displayDealsCount ? bucket.count : bucket.size] as [
          ImplementationStatus,
          number
        ]
    )
    .sort((a, b) => a[1] - b[1]);

  return {
    labels: sortedEntries.map(([key, _]) => $_(ImplementationStatusLabels[key])),
    datasets: [
      {
        data: sortedEntries.map(([_, value]) => value),
        backgroundColor: sortedEntries.map(
          ([key, _]) => ImplementationStatusColors[key]
        ),
      },
    ],
  };
}

export function calcProduceChart(deals: Deal[]) {
  const $_ = get(t);

  const ProduceFields = {
    [ProduceGroup.CROPS]: "current_crops",
    [ProduceGroup.ANIMALS]: "current_animals",
    [ProduceGroup.MINERAL_RESOURCES]: "current_mineral_resources",
  };
  const dealsWithProduceInfo =
    deals?.filter((deal) =>
      Object.values(ProduceFields).some((field) => deal[field])
    ) ?? [];

  const buckets = {
    [ProduceGroup.CROPS]: 0,
    [ProduceGroup.ANIMALS]: 0,
    [ProduceGroup.MINERAL_RESOURCES]: 0,
  };

  for (const deal of dealsWithProduceInfo) {
    Object.entries(ProduceFields).forEach(([field, fieldName]) => {
      if (deal[fieldName]) {
        buckets[field as unknown as ProduceGroup] += 1;
      }
    });
  }

  const total = Object.values(buckets).reduce((acc, current) => acc + current);
  const sortedEntries = Object.entries(buckets)
    .map(([key, val]) => [key, val] as unknown as [ProduceGroup, number])
    .sort((a, b) => a[1] - b[1]);

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
