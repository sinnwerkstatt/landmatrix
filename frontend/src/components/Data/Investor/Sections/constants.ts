export const INVESTOR_SECTIONS = [
  "general",
  "involvements",
  "network-graph",
  "data-sources",
  "history",
] as const

export type InvestorSection = (typeof INVESTOR_SECTIONS)[number]
