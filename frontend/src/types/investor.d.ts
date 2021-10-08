import { User } from "$types/user";
import type { Obj, ObjVersion, WorkflowInfo } from "$types/generics";

enum role {
  PARENT,
  LENDER,
}

interface Investor extends Obj {
  versions: InvestorVersion[];
  workflowinfos: InvestorWorkflowInfo[];
}

interface InvestorVersion extends ObjVersion {
  investor: Investor;
}

export type Involvement = {
  id: number;
  role: role;
  investment_type: [string];
  percentage: number;
  loans_amount: number;
  loans_currency: unknown;
  loans_date: string;
  parent_relation: string;
  comment: string;
  involvement_type: string;
};

interface InvestorWorkflowInfo extends WorkflowInfo {
  investor: Investor;
}
