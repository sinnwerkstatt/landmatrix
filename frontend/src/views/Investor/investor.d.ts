enum role {
  PARENT,
  LENDER,
}

export type Involvement = {
  id: number;
  role: role;
  investment_type: [string];
  percentage: number;
  loans_amount: number;
  loans_currency: object;
  loans_date: string;
  parent_relation: string;
  comment: string;
  involvement_type: string;
};
