import type { Contract } from "$lib/types/data"
import { isEmptySubmodel } from "$lib/utils/dataProcessing"

const CONTRACT_IGNORE_KEYS = ["dealversion"] satisfies (keyof Contract)[]

// explicitly set fields to null!
export const createContract = (nid: string): Contract => ({
  id: null!,
  nid,
  number: "",
  date: null,
  expiration_date: null,
  agreement_duration: null,
  comment: "",
  dealversion: null!,
})

export const isEmptyContract = (contract: Contract) =>
  isEmptySubmodel(contract, CONTRACT_IGNORE_KEYS)
