import type { Obj, ObjVersion, WorkflowInfo } from "$types/generics";

interface Deal extends Obj {
  versions: DealVersion[];
  workflowinfos: DealWorkflowInfo[];
  current_intention_of_investment: string[];
  current_implementation_status: string;
}

interface DealVersion extends ObjVersion {
  deal: Deal;
}

interface DealWorkflowInfo extends WorkflowInfo {
  deal: Deal;
}
