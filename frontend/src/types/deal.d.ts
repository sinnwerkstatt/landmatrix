import type { Obj, ObjVersion, WorkflowInfo } from "$types/generics";
import type { Investor } from "$types/investor";

interface Location {
  id: number;
}

interface Contract {
  id: number;
}
interface DataSource {
  id: number;
}
interface Deal extends Obj {
  locations: Location[];
  contracts: Contract[];
  datasources: DataSource[];
  versions: DealVersion[];
  workflowinfos: DealWorkflowInfo[];
  current_intention_of_investment: string[];
  current_negotiation_status: string;
  current_implementation_status: string;
  fully_updated_at: Date;
  top_investors: Investor[];
  deal_size: number;
  current_contract_size: number;
  operating_company?: Investor;
  confidential: boolean;
  is_public: boolean;
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
