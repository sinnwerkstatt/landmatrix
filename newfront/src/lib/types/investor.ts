import type { Obj, ObjVersion, WorkflowInfo } from "$lib/types/generics";
import type { DataSource, Deal } from "./deal";

export enum Role {
  PARENT = "PARENT",
  LENDER = "LENDER",
}
export enum Classification {
  GOVERNMENT = "GOVERNMENT",
  GOVERNMENT_INSTITUTION = "GOVERNMENT_INSTITUTION",
  STATE_OWNED_COMPANY = "STATE_OWNED_COMPANY",
  SEMI_STATE_OWNED_COMPANY = "SEMI_STATE_OWNED_COMPANY",
  ASSET_MANAGEMENT_FIRM = "ASSET_MANAGEMENT_FIRM",
  BILATERAL_DEVELOPMENT_BANK = "BILATERAL_DEVELOPMENT_BANK",
  STOCK_EXCHANGE_LISTED_COMPANY = "STOCK_EXCHANGE_LISTED_COMPANY",
  COMMERCIAL_BANK = "COMMERCIAL_BANK",
  INSURANCE_FIRM = "INSURANCE_FIRM",
  INVESTMENT_BANK = "INVESTMENT_BANK",
  INVESTMENT_FUND = "INVESTMENT_FUND",
  MULTILATERAL_DEVELOPMENT_BANK = "MULTILATERAL_DEVELOPMENT_BANK",
  PRIVATE_COMPANY = "PRIVATE_COMPANY",
  PRIVATE_EQUITY_FIRM = "PRIVATE_EQUITY_FIRM",
  INDIVIDUAL_ENTREPRENEUR = "INDIVIDUAL_ENTREPRENEUR",
  NON_PROFIT = "NON_PROFIT",
  OTHER = "OTHER",
}

export interface Investor extends Obj {
  name: string;
  classification: Classification;
  homepage: string;
  opencorporates: string;
  datasources: DataSource[];
  comment: string;
  involvements: Involvement[];
  investors: Involvement[];
  ventures: Involvement[];
  versions: InvestorVersion[];
  workflowinfos: InvestorWorkflowInfo[];
  deals: Deal[];
  [key: string]: unknown;
}

export interface InvestorVersion extends ObjVersion {
  investor: Investor;
}

export type Involvement = {
  id: number;
  role: Role;
  investment_type?: [string];
  investor: Investor;
  venture?: Investor;
  percentage?: number;
  loans_amount?: number;
  loans_currency?: unknown;
  loans_date?: string;
  parent_relation?: string;
  comment?: string;
  involvement_type?: string;
};

export interface InvestorWorkflowInfo extends WorkflowInfo {
  investor: Investor;
}
