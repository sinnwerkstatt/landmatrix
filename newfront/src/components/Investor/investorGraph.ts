import cytoscape from "cytoscape"
import type { Core as Graph } from "cytoscape"
import type { CytoscapeOptions, ElementDefinition, NodeSingular } from "cytoscape"
import cyCoseBilkent from "cytoscape-cose-bilkent"
import type { LayoutOptions } from "cytoscape-cose-bilkent"
import cyPopper from "cytoscape-popper"
import tippy from "tippy.js"
import type { Instance as TippyInstance } from "tippy.js"

import { classification_choices } from "$lib/choices"
import type { Deal } from "$lib/types/deal"
import type { Investor, Involvement } from "$lib/types/investor"
import type { Classification } from "$lib/types/investor"

cytoscape.use(cyCoseBilkent)
cytoscape.use(cyPopper)

export const CY_OPTIONS: CytoscapeOptions = {
  minZoom: 0.3,
  maxZoom: 5,
  layout: {
    name: "cose-bilkent",
    quality: "proof",
    nodeDimensionsIncludeLabels: true,
    animate: "end",
  } as LayoutOptions,
  style: [
    {
      selector: "node",
      style: {
        "background-color": el => {
          return el.data("bgColor")
        },
        label: (el: NodeSingular) => {
          return el.data("name")
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
        "target-arrow-shape": el => {
          return el.data("target_arrow_shape") || "none"
        },
        "curve-style": "bezier",
      },
    },
  ],
}

export const createGraph = (elements: ElementDefinition[]) =>
  cytoscape({
    container: document.getElementById("investor-network"),
    elements: elements,
    ...CY_OPTIONS,
  })

const makePopper = (ele: NodeSingular & { tippy?: TippyInstance }) => {
  const ref = ele.popperRef() // used only for positioning
  if (ref) {
    // unfortunately, a dummy element must be passed as tippy only accepts a dom element as the target
    // https://github.com/atomiks/tippyjs/issues/661
    const dummyDomEle = document.createElement("div")

    ele.tippy = tippy(dummyDomEle, {
      trigger: "manual", // call show() and hide() yourself
      getReferenceClientRect: ref.getBoundingClientRect,
      animation: false,
      content: () => {
        const tipEl = document.createElement("div")
        tipEl.classList.add("g-tooltip")
        if (ele.data().dealNode) {
          // tooltip content of deal node
          tipEl.classList.add("deal")
          tipEl.innerHTML = `Deal ${ele.data().name}`
        } else {
          // tooltip content of investor node
          tipEl.classList.add("investor")
          let content = `<span class="name">${ele.data().name} (#${
            ele.data().id
          })</span>`
          if ("country" in ele.data() && ele.data().country)
            content += ` ${ele.data().country.name}, `
          if (
            "classification" in ele.data() &&
            classification_choices[ele.data().classification as Classification]
          )
            content +=
              classification_choices[ele.data().classification as Classification]
          tipEl.innerHTML = content
        }
        return tipEl
      },
    })
  }
}
export const registerTippy = (cyGraph: Graph) => {
  cyGraph.ready(() => {
    cyGraph.nodes().forEach(function (ele) {
      makePopper(ele)
    })
    cyGraph.nodes().unbind("mouseover")
    cyGraph.nodes().bind("mouseover", event => event.target.tippy.show())
    cyGraph.nodes().unbind("mouseout")
    cyGraph.nodes().bind("mouseout", event => event.target.tippy.hide())
  })
}

export const createGraphElements = (
  investor: Investor,
  elements: ElementDefinition[],
  showDeals: boolean,
  depth: number,
) => {
  if (depth <= 0) return elements

  if (elements.length === 0) {
    elements.push({
      data: {
        id: `${investor.id}`,
        name: investor.name,
        comment: investor.comment,
        country: investor.country,
        classification: investor.classification,
        homepage: investor.homepage,
        bgColor: "#44b7b6",
        rootNode: true,
      },
    })
  }

  if (showDeals) {
    investor.deals?.forEach((deal: Deal) => {
      const deal_node = {
        data: {
          ...deal,
          _id: deal.id,
          id: "D" + deal.id,
          name: "#" + deal.id,
          bgColor: "#fc941f",
          dealNode: true,
        },
      }
      const deal_edge = {
        data: {
          id: `${investor.id}_D${deal.id}`,
          source: investor.id,
          target: "D" + deal.id,
          edge_color: "#fc941f",
        },
      }

      elements.push(deal_node)
      elements.push(deal_edge)
    })
  }
  if (investor.involvements && investor.involvements.length) {
    investor.involvements.forEach((involvement: Involvement) => {
      const investor_node = {
        data: {
          id: `${involvement.investor.id}`,
          name: involvement.investor.name,
          comment: involvement.investor.comment,
          country: involvement.investor.country,
          classification: involvement.investor.classification,
          homepage: involvement.investor.homepage,
          bgColor: "#bee7e7",
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
      }
      const investor_edge = {
        data: {
          id: `${investor.id}_${involvement.investor.id}`,
          edge_color: involvement.role === "PARENT" ? "#72B0FD" : "#F78E8F",
          ...(involvement.involvement_type === "VENTURE"
            ? { source: investor.id, target: involvement.investor.id }
            : { source: involvement.investor.id, target: investor.id }),
          target_arrow_shape: "triangle",
        },
      }

      elements.push(investor_node)
      elements.push(investor_edge)

      createGraphElements(involvement.investor, elements, showDeals, depth - 1)
    })
  }

  return elements
}
