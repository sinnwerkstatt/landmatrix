export type InvestorSection = {
  name: string;
  fields: string[];
};

export const investorSections: { [key: string]: InvestorSection[] } = {
  general_info: [
    {
      name: "General Info",
      fields: [
        "name",
        "country__name",
        "classification",
        "homepage",
        "opencorporates",
        "comment",
      ],
    },
  ],
};

export const investorSubsections = {
  parent_companies: [
    "investor",
    "investment_type",
    "percentage",
    "loans_amount",
    "loans_currency",
    "loans_date",
    "comment",
  ],
  tertiary_investors: [
    "investor",
    "investment_type",
    "ownership_share",
    "loan_amount",
    "loan_currency",
    "loan_date",
    "parent_relation",
    "comment",
  ],
};
