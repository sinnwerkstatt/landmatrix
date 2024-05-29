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
import type { Instance as TippyInstance } from "tippy.js"
import tippy from "tippy.js"

import { browser } from "$app/environment"
import { page } from "$app/stores"

import { Classification, classificationChoices } from "$lib/choices"

cytoscape.use(cyCoseBilkent)
cytoscape.use(cyPopper)

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
            if (cntr) content += `${cntr.name}, `
          }

          if ("active_version__classification" in ele.data()) {
            const choice =
              classificationChoices[
                ele.data().active_version__classification as Classification
              ]
            if (choice) content += choice
          }

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
