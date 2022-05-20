import type { Obj, ObjVersion, WorkflowInfo } from "$lib/types/generics";
import { DataSource } from "./deal";

enum Role {
  PARENT,
  LENDER,
}
const enum Classification {
  GOVERNMENT,
  GOVERNMENT_INSTITUTION,
  STATE_OWNED_COMPANY,
  SEMI_STATE_OWNED_COMPANY,
  ASSET_MANAGEMENT_FIRM,
  BILATERAL_DEVELOPMENT_BANK,
  STOCK_EXCHANGE_LISTED_COMPANY,
  COMMERCIAL_BANK,
  INSURANCE_FIRM,
  INVESTMENT_BANK,
  INVESTMENT_FUND,
  MULTILATERAL_DEVELOPMENT_BANK,
  PRIVATE_COMPANY,
  PRIVATE_EQUITY_FIRM,
  INDIVIDUAL_ENTREPRENEUR,
  NON_PROFIT,
  OTHER,
}

interface Investor extends Obj {
  name: string;
  classification: Classification;
  homepage: string;
  opencorporates: string;
  datasources: DataSource[];
  comment: string;
  involvements: Involvement[];
  versions: InvestorVersion[];
  workflowinfos: InvestorWorkflowInfo[];
}

interface InvestorVersion extends ObjVersion {
  investor: Investor;
}

export type Involvement = {
  id: number;
  role: Role;
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
