export const general_info = [
  {
    name: "Land area",
    fields: [
      {
        name: "intended_size",
        component: "TextField",
        label: "Intended size (in ha)",
        placeholder: "Size",
        unit: "ha",
      },
      {
        name: "contract_size",
        component: "ValueDateField",
        label: "Size under contract (leased or purchased area, in ha)",
        placeholder: "Size",
        unit: "ha",
      },
      {
        name: "operating_size",
        component: "ValueDateField",
        label: "Size in operation (production, in ha)",
        placeholder: "Size",
        unit: "ha",
      },
      {
        name: "land_area_comment",
        component: "TextField",
        label: "Comment on land area",
        multiline: true,
      },
      {
        name: "negotiation_status",
        component: "ValueDateField",
        label: "Negotiation status",
        placeholder: "Negotiation status",
        multiselect: {
          multiple: false,
          options: [10, 11, 12, 20, 21, 30, 31, 32, 40],
          labels: {
            10: "Expression of interest",
            11: "Under negotiation",
            12: "Memorandum of understanding",
            20: "Oral agreement",
            21: "Contract signed",
            30: "Negotiations failed",
            31: "Contract canceled",
            32: "Contract expired",
            40: "Change of ownership",
          },
        },
      },
    ],
  },
  {
    name: "Intention of investment",
    fields: [
      {
        name: "intention_of_investment",
        component: "ValueDateField",
        label: "Intention of investment",
        placeholder: "Intention",
        multiselect: {
          multiple: true,
          with_categories: true,
          labels: {
            10: "Biofuels",
            11: "Food crops",
            12: "Fodder",
            13: "Livestock",
            14: "Non-food agricultural commodities",
            15: "Agriculture unspecified",
            20: "Timber plantation",
            21: "Forest logging / management",
            22: "For carbon sequestration/REDD",
            23: "Forestry unspecified",
            30: "Mining",
            31: "Oil / Gas extraction",
            32: "Tourism",
            33: "Industry",
            34: "Conservation",
            35: "Land speculation",
            36: "Renewable Energy",
            99: "Other",
          },
          options: [
            {
              category: "Agriculture",
              options: [10, 11, 12, 13, 14, 15],
            },
            {
              category: "Forestry",
              options: [20, 21, 22, 23],
            },
            {
              category: "Other",
              options: [30, 31, 32, 33, 34, 35, 36, 99],
            },
          ],
        },
      },
      {
        name: "intention_of_investment_comment",
        component: "TextField",
        label: "Comment on intention of investment",
        multiline: true,
      },
    ],
  },
  {
    name: "Nature of the deal",
    fields: [
      {
        name: "nature_of_deal",
        component: "CheckboxField",
        label: "Nature of the deal",
        options: {
          OUTRIGHT_PURCHASE: "Outright Purchase",
          LEASE: "Lease",
          CONCESSION: "Concession",
          EXPLOITATION_PERMIT:
            "Exploitation permit / license / concession (for mineral resources)",
          PURE_CONTRACT_FARMING: "Pure contract farming",
        },
      },
      {
        name: "nature_of_deal_comment",
        component: "TextField",
        label: "Comment on the nature of the deal",
        multiline: true,
      },
    ],
  },
];
