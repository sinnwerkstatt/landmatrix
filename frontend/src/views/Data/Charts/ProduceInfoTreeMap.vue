<template>
  <ChartsContainer>
    <LoadingPulse v-if="$apollo.loading" />
    <div id="produce-info">
      <svg id="produceinfosvg"></svg>
    </div>
  </ChartsContainer>
</template>

<script>
  import LoadingPulse from "/components/Data/LoadingPulse";
  import { data_deal_produce_query, data_deal_query } from "../query";
  import * as d3 from "d3";
  import ChartsContainer from "./ChartsContainer";

  let count = 0;

  function domUid(name) {
    return new Id("O-" + (name == null ? "" : name + "-") + ++count);
  }

  function Id(id) {
    this.id = id;
    this.href = new URL(`#${id}`, location) + "";
  }

  Id.prototype.toString = function () {
    return "url(" + this.href + ")";
  };

  function buildTreeChart(treeData) {
    let format = d3.format(",d");

    let elemx = document.getElementById("produce-info");
    let width = elemx.offsetWidth;
    let height = elemx.offsetHeight;
    console.log("widht", width);
    let svg = d3
      .select("#produceinfosvg")
      .attr("viewBox", [0, 0, width, height])
      .append("svg:g")
      .attr("transform", "translate(.5,.5)");

    // format data
    var root = d3.hierarchy(treeData).sum(function (d) {
      return d.value;
    });

    // initialize graph
    var treemap = d3
      .treemap()
      .tile(d3.treemapSquarify)
      .size([width, height])
      .round(true)
      .paddingInner(1);

    // load data
    treemap(root);

    // get all leaves
    const leaf = svg
      .selectAll("g")
      .data(root.leaves())
      .join("g")
      .attr("transform", (d) => `translate(${d.x0},${d.y0})`);

    // tooltips
    leaf.append("title").text((d) => `${d.data.name}\n${format(d.value)}`);

    // colored squares
    leaf
      .append("rect")
      .attr("id", (d) => (d.leafUid = domUid("leaf")).id)
      .attr("fill", (d) => {
        while (d.depth > 1) d = d.parent;
        return d.data.color;
      })
      .attr("fill-opacity", 0.6)
      .attr("width", (d) => d.x1 - d.x0)
      .attr("height", (d) => d.y1 - d.y0);

    // mask for each rect
    leaf
      .append("clipPath")
      .attr("id", (d) => (d.clipUid = domUid("clip")).id)
      .append("use")
      .attr("xlink:href", (d) => d.leafUid.href);

    // text that is masked (to avoid text overflow)
    leaf
      .append("text")
      .attr("clip-path", (d) => d.clipUid)
      .selectAll("tspan")
      .data((d) =>
        d.data.name.split(/(?=[A-Z][a-z])|\s+/g).concat(format(d.data.value) + " ha")
      )
      .join("tspan")
      .attr("x", 3)
      .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
      .attr("fill-opacity", (d, i, nodes) => (i === nodes.length - 1 ? 0.7 : null))
      .text((d) => d);
  }

  export default {
    name: "ProduceInfoTreeMap",
    components: { ChartsContainer, LoadingPulse },
    data() {
      return {
        deals: [],
        dealsWithProduceInfo: [],
      };
    },
    apollo: {
      deals: data_deal_query,
      dealsWithProduceInfo: data_deal_produce_query,
    },
    computed: {
      treeData() {
        if (this.produceData) {
          return {
            name: "",
            children: [
              {
                name: "Livestock",
                color: "#7D4A0F",
                children: this.produceData.animals.sort((a, b) => a.value < b.value),
              },
              {
                name: "Mineral Resources",
                color: "#black",
                children: this.produceData.resources.sort((a, b) => a.value < b.value),
              },
              {
                name: "Crops",
                color: "#FC941F",
                children: this.produceData.crops.sort((a, b) => a.value < b.value),
              },
            ],
          };
        } else {
          return null;
        }
      },
      produceData() {
        let data = null;
        let areaTotals = {};
        let fields = ["crops", "animals", "resources"];
        let colors = ["#FC941F", "#7D4A0F", "black"];
        if (this.deals.length && this.dealsWithProduceInfo.length) {
          data = {};
          for (let deal of this.dealsWithProduceInfo) {
            for (let field of fields) {
              areaTotals[field] = areaTotals[field] || {};
              for (let entry of deal[field]) {
                for (let key of entry.value) {
                  let dealSize = this.deals.find((d) => d.id === deal.id).deal_size;
                  areaTotals[field][key] =
                    areaTotals[field][key] + dealSize || dealSize;
                }
              }
            }
          }
          for (let field of fields) {
            data[field] = [];
            for (let key of Object.keys(areaTotals[field])) {
              data[field].push({
                name: this.getLabel(field, key),
                value: areaTotals[field][key],
              });
            }
          }
        }
        return data;
      },
    },
    methods: {
      getLabel(field, key) {
        let map = this.$store.state.formfields.deal;
        if (map && field in map) {
          let choices = map[field].choices;
          if (key in choices) {
            return choices[key];
          }
        }
        return key;
      },
      drawChart() {
        if (this.treeData) {
          buildTreeChart(this.treeData);
        }
      },
    },
    watch: {
      treeData() {
        this.drawChart();
      },
    },
    created() {
      // window.addEventListener("resize", this.drawChart);
    },
    destroyed() {
      // window.removeEventListener("resize", this.drawChart);
    },
  };
</script>

<style lang="scss" scoped>
  #produce-info {
    padding: 4em 1em 1em;

    #produceinfosvg {
      width: 800px;
    }
  }
</style>
