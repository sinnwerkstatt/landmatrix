import type { Deal } from "./deal";

type WagtailStreamfieldBlock = {
  type: string;
  value: string;
  id: string;
};
type WagtailStreamfield = WagtailStreamfieldBlock[];

type WagtailPageMeta = {
  type: string;
  detail_url: string;
  html_url: string;
  slug: string;
  show_in_menus: boolean;
  seo_title: string;
  search_description: string;
  first_published_at: Date;
  locale: string;
};

export interface CountryOrRegion {
  id?: number;
  name: string;
  slug?: string;
  observatory_page_id?: number;
}
export interface Region extends CountryOrRegion {
  point_lat_min: number;
  point_lat_max: number;
  point_lon_min: number;
  point_lon_max: number;
}

export interface Country extends CountryOrRegion {
  code_alpha2: string;
  high_income: boolean;
  point_lat: number;
  point_lon: number;
  deals: Deal[];
}

export interface WagtailPage {
  id: number;
  title: string;
  meta: WagtailPageMeta;
  body: WagtailStreamfield;
}

export interface TwitterFeed {
  username: string;
  timeline: {
    name: string;
    screen_name: string;
    created_at: Date;
    deep_link: URL;
    text: string;
  }[];
}

export interface Marker {
  region_id?: number;
  country_id?: number;
  count?: number;
  coordinates: [number, number];
}
export interface ObservatoryPage extends WagtailPage {
  short_description: string;
  introduction_text: string;
  twitter_feed: TwitterFeed;
  region?: Region;
  country?: Country;
  related_blogpages?: BlogPage[];
  markers: Marker[];
}

export interface BlogPage extends WagtailPage {
  header_image: string;
  slug: string;
  url: string;
  date: Date;
  excerpt: string;
  categories: BlogCategory[];
  tags: BlogTag[];
}

export interface BlogCategory {
  id: number;
  name: string;
  slug: string | null;
}

export interface BlogTag {
  id: number;
  name: string;
  slug: string | null;
}
