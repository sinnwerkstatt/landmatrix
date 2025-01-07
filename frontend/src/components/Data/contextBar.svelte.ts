import { _ } from "svelte-i18n"
import { get } from "svelte/store"

import { type ValueLabelEntry } from "$lib/fieldChoices"
import type { components } from "$lib/openAPI"

export function getNegotiationBuckets(
  deals: components["schemas"]["DealVersion"][],
  groups: ValueLabelEntry[],
  bySize = false,
) {
  const vBuckets = groups.map(x => ({
    name: x.label,
    count: 0,
    size: 0,
    fillColor: {
      INTENDED: "hsl(93, 55%, 75%)", // "text-green-300",
      CONCLUDED: "hsl(94, 56%, 65%)", // "text-green-500",
      FAILED: "hsl(0, 73%, 66%)", // "text-red-500",
      CONTRACT_EXPIRED: "hsl(0, 0%, 60%)", //"text-gray-300",
    }[x.value] as string,
  }))

  let totalCount = 0
  let totalSize = 0
  for (const deal of deals) {
    totalCount += 1
    totalSize += deal.deal_size ?? 0

    if (!deal.current_negotiation_status) continue
    switch (deal.current_negotiation_status) {
      case "EXPRESSION_OF_INTEREST":
      case "UNDER_NEGOTIATION":
      case "MEMORANDUM_OF_UNDERSTANDING":
        vBuckets[0].count += 1
        vBuckets[0].size += deal.deal_size ?? 0
        break
      case "ORAL_AGREEMENT":
      case "CONTRACT_SIGNED":
      case "CHANGE_OF_OWNERSHIP":
        vBuckets[1].count += 1
        vBuckets[1].size += deal.deal_size ?? 0
        break
      case "NEGOTIATIONS_FAILED":
      case "CONTRACT_CANCELED":
        vBuckets[2].count += 1
        vBuckets[2].size += deal.deal_size ?? 0
        break
      case "CONTRACT_EXPIRED":
        vBuckets[3].count += 1
        vBuckets[3].size += deal.deal_size ?? 0
        break
    }
  }

  if (bySize) {
    return vBuckets
      .filter(n => n.size > 0)
      .map(n => ({
        name: n.name,
        value: ((n.size / totalSize) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.size.toLocaleString("fr").replace(",", ".")} ${get(_)("ha")}`,
        fillColor: n.fillColor,
      }))
  } else {
    return vBuckets
      .filter(n => n.count > 0)
      .map(n => ({
        name: n.name,
        value: ((n.count / totalCount) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.count.toFixed()} ${get(_)("deals")}`,
        fillColor: n.fillColor,
      }))
  }
}

export function getImplementationBuckets(
  deals: components["schemas"]["DealVersion"][],
  groups: ValueLabelEntry[],
  bySize = false,
) {
  const vBuckets = groups.map(x => ({
    name: x.label,
    count: 0,
    size: 0,
    fillColor: {
      PROJECT_NOT_STARTED: "hsl(93, 55%, 83%)", // "text-green-200",
      STARTUP_PHASE: "hsl(93, 55%, 75%)", // "text-green-300",
      IN_OPERATION: "hsl(94, 56%, 65%)", // "text-green-500",
      PROJECT_ABANDONED: "hsl(0, 0%, 60%)", // "text-gray-300",
    }[x.value] as string,
  }))

  let totalCount = 0
  let totalSize = 0
  for (const deal of deals) {
    totalCount += 1
    totalSize += deal.deal_size ?? 0

    if (!deal.current_implementation_status) continue

    switch (deal.current_implementation_status) {
      case "PROJECT_NOT_STARTED":
        vBuckets[0].count += 1
        vBuckets[0].size += deal.deal_size ?? 0
        break
      case "STARTUP_PHASE":
        vBuckets[1].count += 1
        vBuckets[1].size += deal.deal_size ?? 0
        break
      case "IN_OPERATION":
        vBuckets[2].count += 1
        vBuckets[2].size += deal.deal_size ?? 0
        break
      case "PROJECT_ABANDONED":
        vBuckets[3].count += 1
        vBuckets[3].size += deal.deal_size ?? 0
        break
    }
  }

  if (bySize) {
    return vBuckets
      .filter(n => n.size > 0)
      .map(n => ({
        name: n.name,
        value: ((n.size / totalSize) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.size.toLocaleString("fr").replace(",", ".")} ${get(_)("ha")}`,
        fillColor: n.fillColor,
      }))
  } else {
    return vBuckets
      .filter(n => n.count > 0)
      .map(n => ({
        name: n.name,
        value: ((n.count / totalCount) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.count.toFixed()} ${get(_)("deals")}`,
        fillColor: n.fillColor,
      }))
  }
}

export function getProduce(
  deals: components["schemas"]["DealVersion"][],
  groups: ValueLabelEntry[],
  bySize = false,
) {
  const vBuckets = [
    {
      name: groups.find(g => g.value === "CROPS")!.label,
      count: 0,
      size: 0,
      fillColor: "hsl(233, 76%, 73%)", // "text-purple-400",
    },
    {
      name: groups.find(g => g.value === "ANIMALS")!.label,
      count: 0,
      size: 0,
      fillColor: "hsl(4, 73%, 70%)", // "text-red-400",
    },
    {
      name: groups.find(g => g.value === "MINERAL_RESOURCES")!.label,
      count: 0,
      size: 0,
      fillColor: "hsl(272, 61%, 69%)", // "text-violet-400",
    },
  ]
  let totalCount = 0
  let totalSize = 0
  for (const deal of deals) {
    totalCount += 1
    totalSize += deal.deal_size ?? 0

    if (deal.current_crops?.length) {
      vBuckets[0].count += 1
      vBuckets[0].size += deal.deal_size ?? 0
    }
    if (deal.current_animals?.length) {
      vBuckets[1].count += 1
      vBuckets[1].size += deal.deal_size ?? 0
    }
    if (deal.current_mineral_resources?.length) {
      vBuckets[2].count += 1
      vBuckets[2].size += deal.deal_size ?? 0
    }
  }

  if (bySize) {
    return vBuckets
      .filter(n => n.size > 0)
      .map(n => ({
        name: n.name,
        value: ((n.size / totalSize) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.size.toLocaleString("fr").replace(",", ".")} ${get(_)("ha")}`,
        fillColor: n.fillColor,
      }))
  } else {
    return vBuckets
      .filter(n => n.count > 0)
      .map(n => ({
        name: n.name,
        value: ((n.count / totalCount) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.count.toFixed()} ${get(_)("deals")}`,
        fillColor: n.fillColor,
      }))
  }
}
