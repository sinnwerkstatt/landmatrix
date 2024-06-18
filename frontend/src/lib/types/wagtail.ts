import type { components } from "$lib/openAPI"

import type { BlockKey } from "$components/Wagtail/blocks"

export type WagtailStreamfieldBlock = {
  type: BlockKey
  value: never
  id: string
}
export type WagtailStreamfield = WagtailStreamfieldBlock[]

export type WagtailPageMeta = {
  type: string
  detail_url: string
  html_url: string
  slug: string
  show_in_menus: boolean
  seo_title: string
  search_description: string
  first_published_at: Date
  locale: string
}

export interface CountryOrRegion {
  id: number
  name: string
  // slug?: string
  observatory_page_id: number | null
  // observatory_page?: ObservatoryPage
  point_lat_min: number
  point_lat_max: number
  point_lon_min: number
  point_lon_max: number
}

export interface WagtailPage {
  id: number
  title: string
  meta: WagtailPageMeta
  body: WagtailStreamfield
}

export interface TwitterFeed {
  username: string
  timeline: {
    name: string
    screen_name: string
    created_at: Date
    deep_link: string
    text: string
  }[]
}

export interface Marker {
  region_id?: number
  country_id?: number
  count?: number
  coordinates: [number, number]
}

export interface ObservatoryPage extends WagtailPage {
  short_description: string
  introduction_text: string
  twitter_feed: TwitterFeed
  region?: components["schemas"]["Region"]
  country?: components["schemas"]["Country"]
  related_blogpages?: BlogPage[]
  markers: Marker[]
}

export interface BlogPage extends WagtailPage {
  header_image: string
  slug: string
  url: string
  date: Date
  excerpt: string
  categories: BlogCategory[]
  categories_names: string[]
  tags: BlogTag[]
  documents: {
    id: string
    type: "text" | "document"
    value: {
      title: string
      file: string
      created_at: string
    }
  }[]
}

export interface BlogCategory {
  id: number
  name: string
  slug: string | null
}

export interface BlogTag {
  id: number
  name: string
  slug: string | null
}

export interface Partner {
  id: string
  name: string
  logo: string
  role: "PARTNER" | "DONOR"
  homepage: string
}

export interface BlockImage {
  image?: { url: string }
  url: string
  caption?: string
  external?: boolean
  lightbox?: boolean
}
