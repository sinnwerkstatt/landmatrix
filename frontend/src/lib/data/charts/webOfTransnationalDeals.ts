// source https://observablehq.com/@d3/hierarchical-edge-bundling
import {
  ascending,
  cluster,
  curveBundle,
  hierarchy,
  lineRadial,
  select,
  selectAll,
} from "d3"
import type { BaseType, Selection, HierarchyNode } from "d3"

export interface EdgeBundlingData {
  id?: number
  imports?: string[]
  name: string
  children: EdgeBundlingData[]
}

export interface MyHierarchyNode extends HierarchyNode<EdgeBundlingData> {
  incoming: { 0: MyHierarchyNode; 1: MyHierarchyNode; path: SVGPathElement }[]
  outgoing: { 0: MyHierarchyNode; 1: MyHierarchyNode; path: SVGPathElement }[]
  text: SVGTextElement
  x: number
  y: number
}

const width = 1000
const radius = width / 2
const tree = cluster().size([2 * Math.PI, radius - 150])

const line = lineRadial<MyHierarchyNode>()
  .curve(curveBundle.beta(0.85))
  .radius(d => d.y)
  .angle(d => d.x)

function id(node: MyHierarchyNode): string {
  return `${node.parent ? id(node.parent) + "." : ""}${node.data.name}`
}

function bilink(root: MyHierarchyNode): MyHierarchyNode {
  const map = new Map(root.leaves().map(d => [id(d), d]))
  for (const d of root.leaves()) {
    d.incoming = []
    d.outgoing =
      d.data.imports?.map(i => {
        const node = map.get(i) as MyHierarchyNode
        return [d, node]
      }) ?? []
  }

  for (const d of root.leaves())
    for (const o of d.outgoing) {
      o[1].incoming.push(o)
    }
  return root
}

function addMarkers(
  svg: Selection<SVGElement, MyHierarchyNode, null, undefined>,
): void {
  const defs = svg.append("defs")
  const marker_factory = (name: string) =>
    defs
      .append("marker")
      .attr("id", name)
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 0)
      .attr("refY", 0)
      .attr("markerWidth", 10)
      .attr("markerHeight", 10)
      .attr("orient", "auto-start-reverse")
      .attr("markerUnits", "userSpaceOnUse")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
  marker_factory("incoming-marker")
  marker_factory("outgoing-marker")
}

export function LandMatrixRadialSpider(
  svgElement: SVGElement,
  data_hierarchical: EdgeBundlingData,
  selectedCountry: number | undefined,
  updateCountryFn: (country: number | undefined) => void,
) {
  select(svgElement).selectAll("g").remove()
  select(svgElement).selectAll("defs").remove()

  const svg = select<SVGElement, MyHierarchyNode>(svgElement)
    .attr("viewBox", [-width / 2, -width / 2, width, width])
    .attr("height", "100%")
    .attr("width", "100%")

  if (!data_hierarchical || data_hierarchical.children.length === 0) return

  const root = tree(
    bilink(
      hierarchy(data_hierarchical).sort(
        (a, b) => ascending(a.height, b.height) || ascending(a.data.name, b.data.name),
      ) as MyHierarchyNode,
    ),
  ) as unknown as MyHierarchyNode

  addMarkers(svg)

  const link = svg
    .append("g")
    .attr("stroke", "#ccc")
    .attr("fill", "none")
    .selectAll("path")
    .data(root.leaves().flatMap(leaf => leaf.outgoing))
    .join("path")
    .style("mix-blend-mode", "multiply")
    .attr("d", d => line(d[0].path(d[1])))
    .each(function (d) {
      d.path = this
    })

  function selectCountry(target: string, highlight_class = "highlighted") {
    const selection = select<BaseType, MyHierarchyNode>(target)
    if (selection.size() === 0) return
    const d = selection.datum()

    const incoming_paths = selectAll(d.incoming.map(d => d.path))
    incoming_paths.classed(`incoming-${highlight_class}`, true)
    incoming_paths.raise()

    const outgoing_paths = selectAll(d.outgoing.map(d => d.path))
    outgoing_paths.classed(`outgoing-${highlight_class}`, true)
    outgoing_paths.raise()

    const incoming_texts = selectAll(d.incoming.map(d => d[0].text))
    incoming_texts.classed(`incoming-${highlight_class}`, true)

    const outgoing_texts = selectAll(d.outgoing.map(d => d[1].text))
    outgoing_texts.classed(`outgoing-${highlight_class}`, true)

    link.style("mix-blend-mode", null)
    selection.attr("font-weight", "bold")
    selection.attr("fill", "black")
  }

  function mouseout_event(target: HTMLElement) {
    const selection = select<BaseType, MyHierarchyNode>(target)
    if (selection.size() === 0) return
    link.style("mix-blend-mode", "multiply")
    selection.attr("font-weight", null)
    const d = selection.datum()

    selectAll(d.incoming.map(d => d.path)).classed("incoming-highlighted", false)
    selectAll(d.incoming.map(d => d[0].text)).classed("incoming-highlighted", false)
    selectAll(d.outgoing.map(d => d.path)).classed("outgoing-highlighted", false)
    selectAll(d.outgoing.map(d => d[1].text)).classed("outgoing-highlighted", false)

    selectCountry("#text_" + selectedCountry, "permahighlight")
  }

  svg
    .append("g")
    .selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr("transform", d => `rotate(${(d.x * 180) / Math.PI - 90}) translate(${d.y},0)`)
    .append("text")
    .attr("dy", "0.31em")
    .attr("data-id", d => d.data.id ?? "")
    .attr("id", d => `text_${d.data.id}`)
    .attr("x", d => (d.x < Math.PI ? 6 : -6))
    .attr("text-anchor", d => (d.x < Math.PI ? "start" : "end"))
    .attr("transform", d => (d.x >= Math.PI ? "rotate(180)" : null))
    .text(d => d.data.name)
    .each(function (d) {
      d.text = this
    })
    .on("mouseover", event => selectCountry(event.currentTarget))
    .on("mouseout", event => mouseout_event(event.currentTarget))
    .on("mousedown", d => {
      selectedCountry =
        selectedCountry !== d.target.dataset.id ? d.target.dataset.id : null
      updateCountryFn(selectedCountry)
    })
    .call(text =>
      text.append("title").text(
        d => `${d.data.name}
      ${d.outgoing.length} investing countries
      investing in ${d.incoming.length} countries`,
      ),
    )

  selectCountry("#text_" + selectedCountry, "permahighlight")
}
