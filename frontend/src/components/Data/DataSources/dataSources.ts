import type { DataSource, DealDataSource, InvestorDataSource } from "$lib/types/data"
import { isEmptySubmodel } from "$lib/utils/dataProcessing"

const DATA_SOURCE_IGNORE_KEYS = [
  "dealversion",
  "investorversion",
  "file_not_public",
] satisfies (keyof DealDataSource | keyof InvestorDataSource)[]

// explicitly set fields to null!
export const createDataSource = (nid: string): DataSource => ({
  id: null!,
  nid,
  type: "" as never,
  url: "",
  file: null!,
  file_not_public: false,
  publication_title: "",
  date: null,
  name: "",
  company: "",
  email: "",
  phone: "",
  includes_in_country_verified_information: null,
  open_land_contracts_id: "",
  comment: "",
  dealversion: null!,
  investorversion: null!,
})

export const isEmptyDataSource = (dataSource: DataSource) =>
  isEmptySubmodel(dataSource, DATA_SOURCE_IGNORE_KEYS)
