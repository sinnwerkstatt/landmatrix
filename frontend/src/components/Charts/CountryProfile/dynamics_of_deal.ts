/**
 *
 */
import { axisLeft, descending, max, range, scaleBand, scaleLinear, select } from "d3";
import numeral from "numeral/numeral";

export type DynamicsDataPoint = {
  name: string;
  value: number;
};
export class DynamicsOfDeal {
  private readonly width = 700;
  private readonly height = 500;
  private readonly margin = { top: 30, right: 0, bottom: 10, left: 10 };

  do_the_graph(selector: string, data: DynamicsDataPoint[]): void {
    const svg = select(selector)
      // there is a little extra padding at the bottom (+ 10)
      .attr("viewBox", `0 0 ${this.width + 20} ${this.height + 20 + 10}`)
      .attr("height", "100%")
      .attr("width", "100%")
      .style("background-color", "white")
      .append("g");
    // .attr("transform", "translate(10,10)");

    data = data.sort((a, b) => descending(a.value, b.value));

    const y = scaleBand()
      .domain(range(data.length))
      .rangeRound([this.margin.top, this.height - this.margin.bottom])
      .padding(0.1);

    const x = scaleLinear()
      .domain([0, max(data, (d) => d.value)])
      .range([this.margin.left, this.width - this.margin.right]);

    const format = (val: number) => `${numeral(val).format("0,0")} ha`;

    const bar = svg.selectAll("g").data(data).enter().append("g");
    // bar.attr("class", "bar")
    //         .attr("cx",0)
    //         .attr("transform", function(d, i) {
    //             return "translate(" + margin + "," + (i * (barHeight + barPadding) + barPadding) + ")";
    //         });
    bar
      .attr("fill", "#fc941f")
      .append("rect")
      .attr("x", x(0))
      .attr("y", (d, i) => y(i))
      .attr("width", (d) => x(d.value) - x(0))
      .attr("height", y.bandwidth());

    bar
      .append("text")
      .attr("x", (d) => x(d.value))
      .attr("y", (d, i) => y(i) + y.bandwidth() / 2)
      .text((d) => format(d.value))
      .attr("dy", "0.35em")
      .attr("dx", function (d) {
        const barWidth = x(d.value) - x(0);
        const textWidth = Math.ceil(Math.max(0, this.getBBox().width));
        if (textWidth > barWidth + 5) return 5;
        return -textWidth - 5;
      })
      .attr("fill", (d, idx, z) =>
        +(z[idx].getAttribute("dx") || 1) > 0 ? "black" : "white"
      );

    // svg
    //   .append("g")
    //   .attr("fill", "white")
    //   .attr("text-anchor", "end")
    //   .attr("font-family", "sans-serif")
    //   .attr("font-size", 12)
    //   .selectAll("text")
    //   .data(data)
    //   .join("text")
    //   .attr("x", (d) => x(d.value))
    //   .attr("y", (d, i) => y(i) + y.bandwidth() / 2)
    //   .attr("dy", "0.35em")
    //   .attr("dx", -4)
    //   .text((d) => format(d.value))
    //   .call((text) =>
    //     text
    //       .filter((d) => x(d.value) - x(0) < 20) // short bars
    //       .attr("dx", +4)
    //       .attr("fill", "black")
    //       .attr("text-anchor", "start")
    //   );
    // svg
    //   .append("g")
    //   .attr("fill", "#fc941f")
    //   .selectAll("rect")
    //   .data(data)
    //   .join("rect")
    //   .attr("x", x(0))
    //   .attr("y", (d, i) => y(i))
    //   .attr("width", (d) => x(d.value) - x(0))
    //   .attr("height", y.bandwidth());
    //
    svg
      .append("g")
      .attr("transform", `translate(${this.margin.left},0)`)
      .call(
        axisLeft(y)
          .tickFormat((i) => data[i].name)
          .tickSizeOuter(0)
      );
  }
}
