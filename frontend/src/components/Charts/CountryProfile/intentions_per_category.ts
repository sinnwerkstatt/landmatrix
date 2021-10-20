/**
 * https://gist.github.com/d3noob/31665aced416f27abca4fa46f5f4b568
 * https://observablehq.com/@d3/sankey-diagram
 * https://observablehq.com/@d3/brexit-voting?collection=@d3/d3-sankey
 */
import { drag, select } from "d3";
import { sankey, SankeyGraph, sankeyLinkHorizontal } from "d3-sankey";

export class LamaSankey {
  private readonly width = 700;
  private readonly height = 700;

  do_the_sank(
    selector: string,
    data: SankeyGraph<
      { [key: string]: string | number | boolean },
      { [key: string]: string | number }
    >
  ): void {
    const svg = select(selector)
      // there is a little extra padding at the bottom (+ 10)
      .attr("viewBox", `0 0 ${this.width + 20} ${this.height + 20 + 10}`)
      .attr("height", "100%")
      .attr("width", "100%")
      .style("background-color", "white")
      .append("g")
      .attr("transform", "translate(10,10)");
    svg.selectAll("*").remove();
    if (data.nodes.length === 0) return;
    const d3sankey = sankey()
      .nodeId((d) => d.id)
      .nodeWidth(10)
      .nodePadding(15)
      .size([this.width, this.height]);
    const graph = d3sankey(data);

    const stroke_colors: { [key: string]: string } = {
      PROJECT_NOT_STARTED: "#4BBB87",
      STARTUP_PHASE: "#B9D635",
      IN_OPERATION: "#fc941f",
      PROJECT_ABANDONED: "#7C9A61",
      S_UNKNOWN: "rgb(185,185,185)",
    };

    const links = svg
      .append("g")
      .selectAll(".link")
      .data(graph.links)
      .enter()
      .append("path")
      .attr("class", "link")
      .attr("d", sankeyLinkHorizontal())
      .attr("stroke", (d) => stroke_colors[d.source.id])
      .attr("stroke-width", (d) => d.width)
      .attr("stroke-opacity", 0.6)
      .attr("fill", "none");

    // add the link titles
    links
      .append("title")
      .text((d) => `${d.source.name} → ${d.target.name}\n${d.value} deals`);

    // add in the nodes
    const node = svg
      .append("g")
      .selectAll(".node")
      .data(graph.nodes)
      .enter()
      .append("g")
      .attr("class", "node")
      .call(
        drag()
          .subject((d) => d)
          .on("drag", dragmove)
      );

    // add the rectangles for the nodes
    node
      .append("rect")
      .attr("x", (d) => d.x0 + 2)
      .attr("y", (d) => d.y0)
      .attr("height", (d) => d.y1 - d.y0)
      .attr("width", 6)
      .attr("shape-rendering", "crispEdges")
      .style("fill", "#111")
      .style("stroke", null)
      .style("stroke-width", 0)
      .style("cursor", "move")
      .append("title")
      .text((d) => d.name + "\n" + d.value);

    // add in the title for the nodes
    node
      .append("text")
      .attr("x", (d) => d.x0 - 6)
      .attr("y", (d) => (d.y1 + d.y0) / 2)
      .attr("dy", "0.35em")
      .attr("text-anchor", "end")
      .text((d) =>
        d.istatus ? `${d.name} - ${d.deal_count}` : `${d.name} - ${d.value}`
      )
      .filter((d) => d.x0 < this.width / 2)
      .attr("x", (d) => d.x1 + 6)
      .attr("text-anchor", "start")
      .style("cursor", "move")
      .style("text-shadow", "0 1px 0 #fff");

    function dragmove(event, d) {
      const curRect = select(this).select("rect");
      // d.x1 = d.x1 + event.dx;
      // d.x0 = d.x0 + event.dx;
      // let xTranslate = d.x0 - curRect.attr("X");
      d.y0 = d.y0 + event.dy;
      const yTranslate = d.y0 - curRect.attr("y");
      select(this).attr("transform", `translate(0,${yTranslate})`);
      d3sankey.update(graph);
      links.attr("d", sankeyLinkHorizontal());
    }
  }
}

type SankeyLink = {
  source: string;
  target: string;
  value: number;
};

export function sankey_links_to_csv_cross(json: SankeyLink[]): string {
  const x = new Set() as Set<string>;
  const y = new Set() as Set<string>;
  const cross: { [key: string]: { [key: string]: number } } = {};
  json.forEach((entry) => {
    x.add(entry.source);
    y.add(entry.target);
    if (!cross[entry.source]) cross[entry.source] = {};
    cross[entry.source][entry.target] = entry.value;
  });
  const y_list = [...y];
  let ret = "," + y_list.join(",") + "\n";
  [...x].forEach((source) => {
    ret += `${source},`;
    const line: Array<string | number> = [];
    y_list.forEach((target) => {
      line.push(cross[source][target] || "");
    });
    ret += line.join(",") + "\n";
  });
  return ret;
}
