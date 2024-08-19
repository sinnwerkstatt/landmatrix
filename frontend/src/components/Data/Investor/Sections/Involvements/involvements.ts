import { InvolvementRole, type Involvement } from "$lib/types/data"
import { isEmptySubmodel } from "$lib/utils/dataProcessing"

const INVOLVEMENT_IGNORE_KEYS = [
  "role",
  "child_investor_id",
] satisfies (keyof Involvement)[]

export const createInvolvement =
  (isTertiary: boolean, djangoId: number) =>
  (nid: string): Involvement => ({
    id: null!,
    nid,
    parent_investor_id: null!,
    child_investor_id: djangoId,
    role: isTertiary ? InvolvementRole.LENDER : InvolvementRole.PARENT,
    loans_currency_id: null,
    investment_type: [],
    percentage: null,
    loans_amount: null,
    loans_date: null,
    parent_relation: null,
    comment: "",
  })

export const isEmptyInvolvement = (involvement: Involvement) =>
  isEmptySubmodel(involvement, INVOLVEMENT_IGNORE_KEYS)
