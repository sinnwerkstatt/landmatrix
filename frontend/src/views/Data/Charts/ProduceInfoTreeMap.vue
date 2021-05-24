<template>
  <ChartsContainer>
    <template #default>
      <LoadingPulse v-if="$apollo.loading" />
      <div id="produce-info" ref="container">
        <svg :style="svgStyle"></svg>
      </div>
    </template>
    <template #ContextBar>
      <h2 class="bar-title">{{ $t("Produce info map") }}</h2>
      <div v-html="chart_desc" />

      <Legend :items="legendItems"></Legend>
    </template>
  </ChartsContainer>
</template>

<script>
  import Legend from "$components/Charts/Legend";
  import LoadingPulse from "$components/Data/LoadingPulse";

  import { format } from "d3-format";
  import { hierarchy, treemap, treemapSquarify } from "d3-hierarchy";
  import { select, selectAll } from "d3-selection";

  import { data_deal_produce_query, data_deal_query } from "../query";

  import ChartsContainer from "./ChartsContainer";

  let count = 0;

  function domUid(name) {
    return new Id("O-" + (name == null ? "" : name + "-") + ++count);
  }

  function Id(id) {
    this.id = id;
  }

  // FIXME: commented out because variable location doesnt exist
  // function Id(id) {
  //   this.id = id;
  //   this.href = new URL(`#${id}`, location) + "";
  // }
  //
  // Id.prototype.toString = function () {
  //   return "url(" + this.href + ")";
  // };

  function buildTreeChart(treeData) {
    let myformat = format(",d");

    let elemx = document.getElementById("produce-info");
    if (!elemx) return;

    let width = elemx.offsetWidth;
    let height = (width / 4) * 3;

    // reset first!
    selectAll("#produce-info > svg > *").remove();

    let svg = select("#produce-info > svg")
      .attr("viewBox", [0, 0, width, height])
      .append("svg:g")
      .attr("transform", "translate(.5,.5)");

    // format data
    let root = hierarchy(treeData).sum(function (d) {
      return d.value;
    });

    // initialize graph
    let mytreemap = treemap()
      .tile(treemapSquarify)
      .size([width, height])
      .round(true)
      .paddingInner(1);

    // load data
    mytreemap(root);

    // get all leaves
    const leaf = svg
      .selectAll("g")
      .data(root.leaves())
      .join("g")
      .attr("transform", (d) => `translate(${d.x0},${d.y0})`);

    // tooltips
    leaf.append("title").text((d) => `${d.data.name}\n${myformat(d.value)}`);

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
        d.data.name.split(/(?=[A-Z][a-z])|\s+/g).concat(myformat(d.data.value) + " ha")
      )
      .join("tspan")
      .attr("x", 3)
      .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
      .attr("fill-opacity", (d, i, nodes) => (i === nodes.length - 1 ? 0.7 : null))
      .text((d) => d);
  }

  export default {
    name: "ProduceInfoTreeMap",
    components: { ChartsContainer, LoadingPulse, Legend },
    metaInfo() {
      return { title: this.$t("Produce info map") };
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => {
        vm.$store.dispatch("showContextBar", true);
      });
    },
    data() {
      return {
        deals: [],
        dealsWithProduceInfo: [],
        svgStyle: {},
      };
    },
    apollo: {
      deals: data_deal_query,
      dealsWithProduceInfo: data_deal_produce_query,
    },
    computed: {
      chart_desc() {
        if (!this.$store.state.page.chartDescriptions) return null;
        return this.$store.state.page.chartDescriptions.produce_info_map;
      },
      legendItems() {
        if (this.treeData) {
          return this.treeData.children.map((l) => {
            return {
              label: l.name,
              color: l.color,
            };
          });
        }
        return [];
      },
      treeData() {
        if (this.produceData) {
          return {
            name: "",
            children: [
              {
                name: this.$t("Livestock"),
                color: "#7D4A0F",
                children: this.produceData.animals,
              },
              {
                name: this.$t("Mineral resources"),
                color: "black",
                children: this.produceData.mineral_resources,
              },
              {
                name: this.$t("Crops"),
                color: "#FC941F",
                children: this.produceData.crops,
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
        let fields = ["crops", "animals", "mineral_resources"];
        let totalSize = 0;
        if (
          this.deals.length &&
          this.deals.length === this.dealsWithProduceInfo.length &&
          !this.$apollo.loading
        ) {
          data = {};
          // map deals for faster access
          let dealMap = {};
          for (let deal of this.deals) {
            dealMap[deal.id] = deal;
          }
          // sum area for each produce
          for (let deal of this.dealsWithProduceInfo) {
            for (let field of fields) {
              areaTotals[field] = areaTotals[field] || {};
              if (deal["current_" + field]) {
                let dealSize = dealMap[deal.id].deal_size;
                for (let key of deal["current_" + field]) {
                  // TODO: not correct to add full dealsize for each produce
                  totalSize += dealSize;
                  areaTotals[field][key] =
                    areaTotals[field][key] + dealSize || dealSize;
                }
              }
            }
          }
          // group by field and summarize smaller than 0.1% as other for each field
          let threshHoldSize = totalSize * 0.005;
          for (let field of fields) {
            data[field] = [];
            let otherSize = 0;
            for (let key of Object.keys(areaTotals[field])) {
              let value = areaTotals[field][key];
              if (value < threshHoldSize) {
                otherSize += value;
              } else {
                data[field].push({
                  name: this.getLabel(field, key),
                  value: areaTotals[field][key],
                });
              }
            }
            // sort first
            data[field] = data[field].sort((a, b) => a.value < b.value);
            // then add other
            if (otherSize) {
              data[field].push({
                name: "Other",
                value: otherSize,
              });
            }
          }
        }
        return data;
      },
    },
    watch: {
      treeData() {
        this.drawChart();
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
  };
</script>

<style lang="scss" scoped>
  #produce-info {
    width: 100%;
    margin: 4em 2em 2em 2em;
    padding-top: 75%; // aspect ratio 4:3
    position: relative;
    align-self: safe center;
    max-height: 100%;

    > svg {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
    }
  }
</style>

<style lang="scss">
  .context-bar-container-content {
    .legend {
      font-size: 0.9rem;
    }
  }
</style>
