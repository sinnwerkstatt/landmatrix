import type { FeatureCollection, Geometry } from "geojson";
import { Feature } from "geojson";
import { ImplementationStatus, NegotiationStatus } from "$lib/filters";
import type { Obj, ObjVersion, WorkflowInfo } from "$lib/types/generics";
import type { Investor } from "$lib/types/investor";

enum ACCURACY_LEVEL {
  "",
  COUNTRY,
  ADMINISTRATIVE_REGION,
  APPROXIMATE_LOCATION,
  EXACT_LOCATION,
  COORDINATES,
}

type AreaType = "production_area" | "contract_area" | "intended_area";

interface FeatureProps {
  // these are the location id and name -> not unique for feature
  id?: string;
  name?: string;
  type?: AreaType;
  date?: string;
  current?: boolean;
}

type AreaFeature = Feature<Geometry, FeatureProps>;
type AreaFeatureCollection = FeatureCollection<Geometry, FeatureProps>;

interface Location {
  id: string;
  name?: string;
  description?: string;
  point?: {
    lat: number;
    lng: number;
  };
  facility_name?: string;
  level_of_accuracy?: ACCURACY_LEVEL;
  comment?: string;
  areas?: AreaFeatureCollection;
}

interface Contract {
  id: string;
}
interface DataSource {
  id: string;
  type: string;
  url: string;
  file: string;
  file_not_public: string;
  publication_title: string;
  date: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  includes_in_country_verified_information: string;
  open_land_contracts_id: string;
  comment: string;
  old_group_id: number;
}
interface Deal extends Obj {
  locations: Location[];
  contracts: Contract[];
  datasources: DataSource[];
  versions: DealVersion[];
  workflowinfos?: DealWorkflowInfo[];
  current_intention_of_investment?: string[];
  current_negotiation_status?: NegotiationStatus;
  current_implementation_status?: ImplementationStatus;
  fully_updated_at?: Date;
  fully_updated?: boolean;
  top_investors?: Investor[];
  deal_size?: number;
  current_contract_size?: number;
  intended_size?: number;
  operating_company?: Investor;
  confidential?: boolean;
  is_public?: boolean;
  [key: string]: unknown;
}

interface DealVersion extends ObjVersion {
  deal: Deal;
}

interface DealWorkflowInfo extends WorkflowInfo {
  deal: Deal;
}

interface DealAggregation {
  value: string;
  count: number;
  size: number;
}
interface DealAggregations {
  [key: string]: DealAggregation[];
}
