enum role {
  PARENT,
  LENDER,
}

export type Investor = {
  id: number;
  status: number;
  draft_status: number;
  versions: InvestorVersion[];
};

export type InvestorVersion = {
  id: number;
  investor: Investor;
  created_at: Date;
  created_by: User;
  object_id: Int;
};

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
