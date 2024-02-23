export interface Counts {
  deals_public_count?: number
  deals_public_multi_ds_count?: number
  deals_public_high_geo_accuracy?: number
  deals_public_polygons?: number
  investors_public_count?: number
  investors_public_known?: number
}

interface CaseStatisticsObj {
  id: number
  status: string | null
  active_version_id: number | null
  draft_version_id: number | null
  draft_version__status: string

  country_id: number | null
  region_id: number | null

  created_at: string
  modified_at: string | null
}

export interface CaseStatisticsDeal extends CaseStatisticsObj {
  fully_updated_at: string | null
  confidential: boolean
  deal_size: number | null
  active_version__is_public: boolean
  active_version__fully_updated: boolean
}
export interface CaseStatisticsInvestor extends CaseStatisticsObj {
  name: string
}
