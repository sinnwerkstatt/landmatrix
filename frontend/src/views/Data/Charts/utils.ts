export function addMarkers(
  svg: Selection<BaseType, unknown, HTMLElement, unknown>
): void {
  const defs = svg.append("defs");
  const marker_factory = (name) =>
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
      .attr("d", "M0,-5L10,0L0,5");
  marker_factory("incoming-marker");
  marker_factory("outgoing-marker");
}
