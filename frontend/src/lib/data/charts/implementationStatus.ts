import type { BucketMap } from "$lib/data/buckets"
import { createBucketMapReducer } from "$lib/data/buckets"
import { COLORS } from "$lib/data/createChartData"
import type { DealVersion2, ImplementationStatus } from "$lib/types/data"

export const IMPLEMENTATION_STATUS_COLORS: { [key in ImplementationStatus]: string } = {
  PROJECT_NOT_STARTED: COLORS.ORANGE_LIGHTER,
  STARTUP_PHASE: COLORS.ORANGE_LIGHT,
  IN_OPERATION: COLORS.ORANGE,
  PROJECT_ABANDONED: COLORS.ORANGE_DARK,
}

export const getImplementationStatusColor = (status: ImplementationStatus) =>
  IMPLEMENTATION_STATUS_COLORS[status]

export const implementationStatusReducer = (
  bucketMap: BucketMap<ImplementationStatus>,
  deal: DealVersion2,
): BucketMap<ImplementationStatus> => {
  const implementationStatus = deal.current_implementation_status
  const bucketMapReducer = createBucketMapReducer<ImplementationStatus>(
    deal.deal_size ?? 0,
  )
  return implementationStatus
    ? bucketMapReducer(bucketMap, implementationStatus)
    : bucketMap
}
