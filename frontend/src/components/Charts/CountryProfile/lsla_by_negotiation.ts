/**
 *
 */
import { select } from "d3";

export class LSLAByNegotiation {
  private readonly width = 700;
  private readonly height = 700;
  private svg;

  constructor(selector: string) {
    this.svg = select(selector)
      // there is a little extra padding at the bottom (+ 10)
      .attr("viewBox", `0 0 ${this.width + 20} ${this.height + 20 + 10}`)
      .attr("height", "100%")
      .attr("width", "100%")
      .append("g")
      .attr("transform", "translate(10,10)");
  }
}
