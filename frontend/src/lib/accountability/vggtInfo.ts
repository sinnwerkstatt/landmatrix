export const scoreLabels = {
  NO_DATA: "No data",
  SEVERE_VIOLATIONS: "Severe violations",
  PARTIAL_VIOLATIONS: "Violations",
  NO_VIOLATIONS: "No violations",
}

export const vggtInfo = {
  1: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS:
        "Indigenous people traditional / customary rights / community rights not recognized",
      PARTIAL_VIOLATIONS:
        "Indigenous people traditional / customary rights / community rights recognized BUT not enforced in practice",
      NO_VIOLATIONS:
        "Indigenous people traditional / customary rights / community rights recognized",
    },
    score_help: [],
  },
  2: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS: "Displacement without compensation",
      PARTIAL_VIOLATIONS:
        "Displacement, with inadequate consultation (no FPIC) and/or compensation",
      NO_VIOLATIONS:
        "No displacement or displacement with FPIC with adequate compensation.",
    },
    score_help: [
      "Only take into account compensation refering to the displacement",
      "'Dealt with' means that the company addressed the issues created by the displacement. Compensation and Resettlement that do not address the issue created by displacement such as nnot providing any new livelihood opportunities or creating even more conflict should be rated as not adequately dealt with.",
      "If displacement is recorded and no information is provided on 'is dealt with' then assume it is not dealt with.",
    ],
  },
  3: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS: "Not consulted",
      PARTIAL_VIOLATIONS: "Limited consultation",
      NO_VIOLATIONS: "Free Prior and Informed Consent (FPIC)",
    },
    score_help: [],
  },
  4: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS: "Land conflicts reported",
      PARTIAL_VIOLATIONS: "Land conflicts reported, but only partly dealt with",
      NO_VIOLATIONS: "No land conflicts reported or fully dealt with",
    },
    score_help: [],
  },
  5: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS: "No benefits materialised",
      PARTIAL_VIOLATIONS:
        "Unspecific benefits materialised or benefits that are not deemed to foster social and economic growth and sustainable human development focusing on smallholders",
      NO_VIOLATIONS:
        "Specific benefits materialised that foster social and economic growth and sustainable human development focusing on smallholders",
    },
    score_help: [
      "If the project is not implemented, we don't expect any materialised benefits. This score only applies to deals in Startup phase and In operation. In other cases, the score keeps the status No data.",
      "In case the extent of promised benefits is unknown, but benefits materialised were reported, we have to assume that all promised benefits were materialised.",
    ],
  },
  6: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS:
        "Negative impacts related to environmental degradation reported and not addressed by the investor",
      PARTIAL_VIOLATIONS:
        "Negative impacts related to environmental degradation reported, but addressed by the investor",
      NO_VIOLATIONS:
        "No negative impacts related to environmental degradation reported",
    },
    score_help: [
      "The category cultural loss does not count as negative impact as article 12.12 only relates to food insecurity and environmental degradation.",
      "The category other (and comment related to the category) to be assessed individually and only scored as it relates to food insecurity and environmental degradation.",
      "Where there are no negative impacts recorded, make a note as such in the comment field.",
      "Deals rated as having no VGGTs violation have either only cultural loss reported as negative impact or have an explicit reference in the comment with respect to no impact",
      "Any type of negative impact reported that is linked to food security/environmental degradation should be considered.",
    ],
  },
  7: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS:
        "No compensation received or largely unsatisfactory and source of tensions within the community",
      PARTIAL_VIOLATIONS:
        "Compensation received but incomplete, severely delayed or unsatisfactory",
      NO_VIOLATIONS: "Compensation received",
    },
    score_help: [
      "If the project is not implemented, we don't expect any received compensation. This score only applies to deals in Startup phase and In operation. In other cases, the score keeps the status No data.",
      "If only some community members received compensation, it is considered incomplete.",
      "Only use additional information (community reaction and land conflicts related) if it relates to financial compensation.",
    ],
  },
  8: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS: "Women not included in consultation",
      PARTIAL_VIOLATIONS: "Insufficient inclusion of women in consultation",
      NO_VIOLATIONS: "Women included at representative level in consultation",
    },
    score_help: [
      "Employment information related to women must not be scored even if this data is pulled through from the LMI platform. We focus on community consultation only for this variable.",
    ],
  },
  9: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS: "Purchase price or leasing fee not known",
      PARTIAL_VIOLATIONS:
        "Purchase price or leasing fee published by non-formal source",
      NO_VIOLATIONS:
        "Purchase price or leasing fee publicly available through formal sources",
    },
    score_help: [
      "If the information comes from a media report and nothing else, this is an informal source.",
      "It's not to judge if the price was enough but on the transparency around the final amount agreed.",
      "If no purchase price or leasing fees are registered, it means that they weren't publicly available which consists in a VGGTs violation. This also means that this variable cannot have the 'no data' status.",
      "Formal sources are government sources and contract publicly available on the investor's website.",
      "Informal sources are sources for which you can't find the link to the original source, organisation's sites, etc.",
    ],
  },
  10: {
    score_meaning: {
      NO_DATA: "Insufficient data available to score this variable",
      SEVERE_VIOLATIONS:
        "No or insufficient legal assistance provided, with little means of resolving disputes",
      PARTIAL_VIOLATIONS:
        "Some effective legal assistance,  and access to and means of resolving disputes available",
      NO_VIOLATIONS:
        "Legal assistance fully provided, and access to and means of resolving disputes available",
    },
    score_help: ["Legal assistance can come from the State or civil society."],
  },
}
