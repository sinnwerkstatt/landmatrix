export const INVESTOR_SECTIONS = [
  "general",
  "involvements",
  "network-graph",
  "data-sources",
  "history",
] as const

export type InvestorSection = (typeof INVESTOR_SECTIONS)[number]

export const INVESTOR_EDIT_SECTIONS = [
  "general",
  "parent-companies",
  "tertiary-investors",
  "data-sources",
] as const

export type InvestorEditSection = (typeof INVESTOR_EDIT_SECTIONS)[number]
