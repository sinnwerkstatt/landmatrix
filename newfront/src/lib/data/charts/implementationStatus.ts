import { implementation_status_choices } from "$lib/choices"
import type { BucketMap } from "$lib/data/buckets"
import { createBucketMapReducer } from "$lib/data/buckets"
import { COLORS, createChartData } from "$lib/data/createChartData"
import { ImplementationStatus } from "$lib/types/deal"
import type { Deal } from "$lib/types/deal"

const IMPLEMENTATION_STATUS_COLORS: { [key in ImplementationStatus]: string } = {
  [ImplementationStatus.PROJECT_NOT_STARTED]: COLORS.ORANGE_LIGHTER,
  [ImplementationStatus.STARTUP_PHASE]: COLORS.ORANGE_LIGHT,
  [ImplementationStatus.IN_OPERATION]: COLORS.ORANGE,
  [ImplementationStatus.PROJECT_ABANDONED]: COLORS.ORANGE_DARK,
}

const getImplementationStatusLabel = (status: ImplementationStatus) =>
  implementation_status_choices[status]

const getImplementationStatusColor = (status: ImplementationStatus) =>
  IMPLEMENTATION_STATUS_COLORS[status]

export const implementationStatusReducer = (
  bucketMap: BucketMap<ImplementationStatus>,
  deal: Deal,
): BucketMap<ImplementationStatus> => {
  const implementationStatus = deal.current_implementation_status
  const bucketMapReducer = createBucketMapReducer<ImplementationStatus>(deal.deal_size)
  return implementationStatus
    ? bucketMapReducer(bucketMap, implementationStatus)
    : bucketMap
}

export const createImplementationStatusChartData =
  createChartData<ImplementationStatus>(
    implementationStatusReducer,
    Object.values(ImplementationStatus),
    getImplementationStatusLabel,
    getImplementationStatusColor,
  )
