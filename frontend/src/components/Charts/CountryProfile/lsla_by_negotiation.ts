/**
 *
 */
import { axisLeft, max, range, scaleBand, scaleLinear, select } from "d3";

export type LSLAData = {
  name: string;
  amount: number;
  size: number;
  meta?: boolean;
};

export class LSLAByNegotiation {
  private readonly width = 920;
  private readonly height = 500;
  private readonly margin = { top: 30, right: 0, bottom: 10, left: 300 };

  do_the_graph(selector: string, data: LSLAData[]): void {
    const elem = document.querySelector(selector);
    if (elem) elem.innerHTML = "";

    const svg = select(selector)
      // there is a little extra padding at the bottom (+ 10)
      .attr("viewBox", `0 0 ${this.width + 20} ${this.height + 20 + 10}`)
      .attr("height", "100%")
      .attr("width", "100%")
      .style("background-color", "white");

    // svg
    //   .append("line")
    //   .attr("x1", 608)
    //   .attr("x2", 608)
    //   .attr("y1", 0)
    //   .attr("y2", 700)
    //   .attr("stroke", "black")
    //   .attr("stroke-width", "2");
    //

    const y = scaleBand()
      .domain(range(data.length))
      .rangeRound([0, this.height])
      .padding(0.1);

    const format = (val: number) => `${Math.round(val).toLocaleString("fr")} ha`;

    const x1 = scaleLinear()
      .domain([0, max(data, (d) => d.amount)])
      .range([300, 600]);
    const x2 = scaleLinear()
      .domain([0, max(data, (d) => d.size)])
      .range([610, 910]);

    // const svg_data = svg.selectAll("g").data(data).enter();
    const bar_amount = svg
      .append("g")
      .attr("id", "amountstuff")
      .selectAll("g")
      .data(data)
      .enter()
      .append("g");

    // shadow boxes
    bar_amount
      .append("rect")
      .attr("fill", "#f6f7f7")
      .attr("x", x1(0))
      .attr("y", (d, i) => y(i))
      .attr("width", 300)
      .attr("height", y.bandwidth());

    bar_amount
      .append("rect")
      .attr("fill", (d) => (d.meta ? "#812819" : "#d3b7ac"))
      .attr("x", x1(0))
      .attr("y", (d, i) => y(i))
      .attr("width", (d) => x1(d.amount) - x1(0))
      .attr("height", y.bandwidth());

    bar_amount
      .append("text")
      .attr("x", (d) => x1(d.amount))
      .attr("y", (d, i) => y(i) + y.bandwidth() / 2)
      .text((d) => d.amount)
      .attr("dy", "0.35em")
      .attr("dx", function (d) {
        const barWidth = x1(d.amount) - x1(0);
        const textWidth = Math.ceil(Math.max(0, this.getBBox().width));
        if (textWidth + 10 > barWidth) return 5;
        return -textWidth - 5;
      })
      .attr("fill", (d, idx, z) =>
        +(z[idx].getAttribute("dx") || 1) > 0 ? "black" : "white"
      );

    const bar_size = svg
      .append("g")
      .attr("id", "sizestuff")
      .selectAll("g")
      .data(data)
      .enter()
      .append("g");

    // shadow boxes
    bar_size
      .append("rect")
      .attr("fill", "#f6f7f7")
      .attr("x", x2(0))
      .attr("y", (d, i) => y(i))
      .attr("width", 300)
      .attr("height", y.bandwidth());
    bar_size
      .attr("fill", (d) => (d.meta ? "#f68d1f" : "#f8d6ab"))
      .append("rect")
      .attr("x", x2(0))
      .attr("y", (d, i) => y(i))
      .attr("width", (d) => x2(d.size) - x2(0))
      .attr("height", y.bandwidth());

    bar_size
      .append("text")
      .attr("x", (d) => x2(d.size))
      .attr("y", (d, i) => y(i) + y.bandwidth() / 2)
      .text((d) => format(d.size))
      .attr("dy", "0.35em")
      .attr("dx", function (d) {
        const barWidth = x2(d.size) - x2(0);
        const textWidth = Math.ceil(Math.max(0, this.getBBox().width));
        if (textWidth + 10 > barWidth) return 5;
        return -textWidth - 5;
      })
      .attr("fill", (d, idx, z) =>
        +(z[idx].getAttribute("dx") || 1) > 0 ? "black" : "white"
      );

    svg
      .append("g")
      .attr("transform", `translate(${this.margin.left},0)`)
      .call(
        axisLeft(y)
          .tickFormat((i) => data[i].name)
          .tickSizeOuter(0)
      )
      .attr("font-size", "1rem");
  }
}
