export interface BlockImage {
  image?: { url: string };
  url: string;
  caption?: string;
  external?: boolean;
}

export interface CountryOrRegion {
  id?: number;
  name: string;
  slug?: string;
  observatory_page_id?: number;
}
export type Region = CountryOrRegion;

export interface Country extends CountryOrRegion {
  code_alpha2: string;
}
