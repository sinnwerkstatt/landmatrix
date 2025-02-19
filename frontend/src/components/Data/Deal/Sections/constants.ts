// These are the section slugs
export const DEAL_SECTIONS = [
  "locations",
  "general",
  "contracts",
  "employment",
  "investor-info",
  "local-communities",
  "former-use",
  "produce-info",
  "water",
  "gender-related-info",
  "overall-comment",
  "data-sources",
  "history",
] as const

export type DealSection = (typeof DEAL_SECTIONS)[number]
