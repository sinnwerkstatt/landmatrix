import cytoscape from "cytoscape";
import coseBilkent from "cytoscape-cose-bilkent";
import popper from "cytoscape-popper";
import type { Deal } from "$lib/types/deal";
import type { Investor, Involvement } from "$lib/types/investor";

cytoscape.use(coseBilkent);
cytoscape.use(popper);

const cy = null;

const cyconfig = {
  minZoom: 0.3,
  maxZoom: 5,
  layout: {
    name: "cose-bilkent",
    quality: "proof",
    nodeDimensionsIncludeLabels: true,
    animate: "end",
  },
  style: [
    {
      selector: "node",
      style: {
        "background-color": (obj) => {
          return obj.data("bgcolor") || "#bee7e7";
        },
        label: (obj) => {
          return obj.data("name");
        },
        "text-valign": "center",
        "font-size": "9pt",
        "text-wrap": "wrap",
        "text-max-width": "120px",
        // "shape": "ellipse",
      },
    },
    {
      selector: "edge",
      style: {
        width: 1,
        "line-color": "data(edge_color)",
        "target-arrow-color": "data(edge_color)",
        "target-arrow-shape": (obj) => {
          return obj.data("target_arrow_shape") || "none  ";
        },
        "curve-style": "bezier",
      },
    },
  ],
};

export function calculateGraph(
  investor: Investor,
  elements,
  showDeals: boolean,
  depth: number
) {
  if (depth <= 0) return;

  if (!elements) {
    elements = [
      {
        data: {
          id: investor.id,
          name: investor.name,
          comment: investor.comment,
          country: investor.country,
          classification: investor.classification,
          homepage: investor.homepage,
          bgcolor: "#44b7b6",
          rootNode: true,
        },
      },
    ];
  }

  if (showDeals) {
    investor.deals?.forEach((deal: Deal) => {
      const deal_node = {
        data: {
          ...deal,
          _id: deal.id,
          id: "D" + deal.id,
          name: "#" + deal.id,
          bgcolor: "#fc941f",
          dealNode: true,
        },
      };
      const deal_edge = {
        data: {
          id: `${investor.id}_D${deal.id}`,
          source: investor.id,
          target: "D" + deal.id,
          edge_color: "#fc941f",
        },
      };

      elements.push(deal_node);
      elements.push(deal_edge);
    });
  }
  if (!investor.involvements || !investor.involvements.length) return;
  investor.involvements.forEach((involvement: Involvement) => {
    const investor_node = {
      data: {
        id: involvement.investor.id,
        name: involvement.investor.name,
        comment: involvement.investor.comment,
        country: involvement.investor.country,
        classification: involvement.investor.classification,
        homepage: involvement.investor.homepage,
        involvement: {
          role: involvement.role,
          investment_type: involvement.investment_type,
          involvement_type: involvement.involvement_type,
          percentage: involvement.percentage,
          loans_amount: involvement.loans_amount,
          loans_currency: involvement.loans_currency,
          loans_date: involvement.loans_date,
          parent_relation: involvement.parent_relation,
          comment: involvement.comment,
        },
      },
    };
    const investor_edge = {
      data: {
        id: `${investor.id}_${involvement.investor.id}`,
        edge_color: involvement.role === "PARENT" ? "#72B0FD" : "#F78E8F",
        ...(involvement.involvement_type === "VENTURE"
          ? { source: investor.id, target: involvement.investor.id }
          : { source: involvement.investor.id, target: investor.id }),
        target_arrow_shape: "triangle",
      },
    };

    elements.push(investor_node);
    elements.push(investor_edge);

    calculateGraph(involvement.investor, elements, showDeals, depth - 1);
  });
}
