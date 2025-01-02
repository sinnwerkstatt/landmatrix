import { get } from "svelte/store"

import { dealChoices } from "$lib/fieldChoices"
import type { components } from "$lib/openAPI"

export function getNegotiationBuckets(
  deals: components["schemas"]["DealVersion"][],
  bySize = false,
) {
  const vBuckets = get(dealChoices).negotiation_status_group.map(x => ({
    name: x.label,
    count: 0,
    size: 0,
    className: {
      INTENDED: "text-green-300",
      CONCLUDED: "text-green-500",
      FAILED: "text-red-500",
      CONTRACT_EXPIRED: "text-gray-300",
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
        label: `<strong>${n.name}</strong>: ${n.size.toLocaleString("fr").replace(",", ".")} ha`,
        className: n.className,
      }))
  } else {
    return vBuckets
      .filter(n => n.count > 0)
      .map(n => ({
        name: n.name,
        value: ((n.count / totalCount) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.count.toFixed()} deals`,
        className: n.className,
      }))
  }
}

export function getImplementationBuckets(
  deals: components["schemas"]["DealVersion"][],
  bySize = false,
) {
  const vBuckets = get(dealChoices).implementation_status.map(x => ({
    name: x.label,
    count: 0,
    size: 0,
    className: {
      PROJECT_NOT_STARTED: "text-green-200",
      STARTUP_PHASE: "text-green-300",
      IN_OPERATION: "text-green-500",
      PROJECT_ABANDONED: "text-gray-300",
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
        label: `<strong>${n.name}</strong>: ${n.size.toLocaleString("fr").replace(",", ".")} ha`,
        className: n.className,
      }))
  } else {
    return vBuckets
      .filter(n => n.count > 0)
      .map(n => ({
        name: n.name,
        value: ((n.count / totalCount) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.count.toFixed()} deals`,
        className: n.className,
      }))
  }
}

export function getProduce(
  deals: components["schemas"]["DealVersion"][],
  bySize = false,
) {
  const vBuckets = [
    {
      name: "Crops",
      count: 0,
      size: 0,
      className: "text-purple-400",
    },
    {
      name: "Livestock",
      count: 0,
      size: 0,
      className: "text-red-400",
    },
    {
      name: "Mineral Resources",
      count: 0,
      size: 0,
      className: "text-violet-400",
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
        label: `<strong>${n.name}</strong>: ${n.size.toLocaleString("fr").replace(",", ".")} ha`,
        className: n.className,
      }))
  } else {
    return vBuckets
      .filter(n => n.count > 0)
      .map(n => ({
        name: n.name,
        value: ((n.count / totalCount) * 100).toFixed(),
        label: `<strong>${n.name}</strong>: ${n.count.toFixed()} deals`,
        className: n.className,
      }))
  }
}
