import type {
  CytoscapeOptions,
  ElementDefinition,
  Core as Graph,
  NodeSingular,
} from "cytoscape"
import cytoscape from "cytoscape"
import type { LayoutOptions } from "cytoscape-cose-bilkent"
import cyCoseBilkent from "cytoscape-cose-bilkent"
import cyPopper from "cytoscape-popper"
import { get } from "svelte/store"
import type { Content } from "tippy.js"
import tippy from "tippy.js"

import { browser } from "$app/environment"
import { page } from "$app/stores"

import { classificationMap } from "$lib/stores/maps"
import { Classification } from "$lib/types/investor"

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const tippyFactory = (ref: any, content: Content) => {
  // Since tippy constructor requires DOM element/elements, create a placeholder
  const dummyDomEle = document.createElement("div")

  return tippy(dummyDomEle, {
    getReferenceClientRect: ref.getBoundingClientRect,
    trigger: "manual",
    content: content,

    animation: false,
    // arrow: true,
    // placement: "bottom",
    // hideOnClick: false,
    // sticky: "reference",

    interactive: true,
    appendTo: document.body,
  })
}

cytoscape.use(cyCoseBilkent)
cytoscape.use(cyPopper(tippyFactory))

let textColor = "black"
if (browser && sessionStorage.theme === "dark") {
  textColor = "white"
}
export const LAYOUT_OPTIONS = {
  name: "cose-bilkent",
  quality: "proof",
  nodeDimensionsIncludeLabels: true,
  animate: "end",
} as LayoutOptions
export const CY_OPTIONS: CytoscapeOptions = {
  minZoom: 0.3,
  maxZoom: 5,
  // wheelSensitivity: 0.2,
  layout: LAYOUT_OPTIONS,

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
        "font-size": "9px",
        "text-wrap": "wrap",
        "text-max-width": "120px",
        color: textColor,
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

export const createGraph = (
  containerElement: HTMLDivElement,
  elements: ElementDefinition[],
) =>
  cytoscape({
    container: containerElement,
    elements: elements,
    ...CY_OPTIONS,
  })

const makeContent = (ele: NodeSingular) => {
  const tipEl = document.createElement("div")
  tipEl.classList.add("g-tooltip")
  if (ele.data().dealNode) {
    // tooltip content of deal node
    tipEl.classList.add("deal")
    tipEl.classList.add("bg-orange")
    tipEl.innerHTML = `Deal ${ele.data().name}`
  } else {
    // tooltip content of investor node
    tipEl.classList.add("investor")
    tipEl.classList.add("bg-pelorous")
    let content = `<div class="font-bold">${ele.data().active_version__name} (#${
      ele.data().id
    })</div>`

    if ("active_version__country_id" in ele.data()) {
      const cntr = get(page).data.countries.find(
        c => c.id === ele.data().active_version__country_id,
      )
      if (cntr) content += `${cntr.name}`
    }

    if ("active_version__classification" in ele.data()) {
      // Todo: make reflexive, e.g., make tooltip a svelte component
      const choice =
        get(classificationMap)[
          ele.data().active_version__classification as Classification
        ]
      if (choice) content += ", " + choice
    }

    tipEl.innerHTML = content
  }
  return tipEl
}

export const registerTippy = (cyGraph: Graph) => {
  cyGraph.ready(() => {
    cyGraph.nodes().forEach(ele => {
      // @ts-expect-error tippy is custom property
      ele.tippy = ele.popper({
        content: makeContent(ele),
      })
    })
    cyGraph.nodes().unbind("mouseover")
    cyGraph.nodes().bind("mouseover", event => event.target.tippy.show())
    cyGraph.nodes().unbind("mouseout")
    cyGraph.nodes().bind("mouseout", event => event.target.tippy.hide())
  })
}
