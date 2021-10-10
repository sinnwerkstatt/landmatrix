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

export interface Region {
  id: number;
  name: string;
  slug: string;
}

export interface Country {
  id: number;
  name: string;
  slug: string;
}

export interface WagtailPage {
  id: number;
  title: string;
  meta: WagtailPageMeta;
  body: WagtailStreamfield;
}

export interface ObservatoryPage extends WagtailPage {
  short_description: string;
  introduction_text: string;
  twitter_feed: unknown;
  region?: Region;
  country?: Country;
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
