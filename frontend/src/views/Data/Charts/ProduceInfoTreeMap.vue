<template>
  <ChartsContainer
    @filterbar-toggle="toggleContextContainer"
    @contextbar-toggle="toggleContextContainer"
  >
    <template #default>
      <LoadingPulse v-if="$apollo.loading" />
      <div id="produce-info" ref="container">
        <svg></svg>
      </div>
    </template>
    <template #ContextBar>
      <h2 class="bar-title">{{ $t("Produce info map") }}</h2>
      <div v-html="chart_desc" />

      <Legend :items="legendItems"></Legend>
    </template>
  </ChartsContainer>
</template>

<script lang="ts">
  import Vue from "vue";
  import { format, hierarchy, treemap, treemapSquarify, select, selectAll } from "d3";
  import Legend from "$components/Charts/Legend.vue";
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import ChartsContainer from "./ChartsContainer.vue";
  import { data_deal_produce_query, data_deal_query } from "../query";

  function buildTreeChart(treeData) {
    if (!treeData) return;
    let count = 0;
    const domUid = (name) => `O-${name}-${++count}`;
    let myformat = format(",d");

    let elemx = document.getElementById("produce-info");
    if (!elemx) return;

    let width = elemx.offsetWidth;
    let height = elemx.offsetHeight;

    // reset first!
    selectAll("#produce-info > svg > *").remove();

    let svg = select("#produce-info > svg")
      .attr("viewBox", [0, 0, width, height])
      .append("svg:g")
      .attr("transform", "translate(.5,.5)");

    // format data
    let root = hierarchy(treeData).sum((d) => d.value);

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
        d.data.name
          .split(/(?=[A-Z][a-z]\(\) )\s+/g)
          .concat(`${Math.round(d.data.value).toLocaleString("fr")} ha`)
      )
      .join("tspan")
      .attr("x", 2)
      .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
      .attr("fill-opacity", (d, i, nodes) => (i === nodes.length - 1 ? 0.7 : null))
      .text((d) => d);
  }

  export default Vue.extend({
    name: "ProduceInfoTreeMap",
    components: { ChartsContainer, LoadingPulse, Legend },
    metaInfo() {
      return { title: this.$t("Produce info map").toString() };
    },
    beforeRouteEnter(to, from, next) {
      next((vm) => vm.$store.dispatch("showContextBar", true));
    },
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
      chart_desc() {
        return this.$store.state.page.chartDescriptions?.produce_info_map;
      },
      legendItems() {
        if (this.treeData) {
          return this.treeData.children.map((l) => ({ label: l.name, color: l.color }));
        }
        return [];
      },
      treeData() {
        if (!this.produceData) return null;
        let ret = { name: "", children: [] };
        if (this.produceData.animals.length > 0) {
          ret.children.push({
            name: this.$t("Livestock"),
            color: "#7D4A0F",
            children: this.produceData.animals,
          });
        }
        if (this.produceData.mineral_resources.length > 0) {
          console.log("minres", this.produceData.mineral_resources);
          ret.children.push({
            name: this.$t("Mineral resources"),
            color: "black",
            children: this.produceData.mineral_resources,
          });
        }
        if (this.produceData.crops.length > 0) {
          ret.children.push({
            name: this.$t("Crops"),
            color: "#FC941F",
            children: this.produceData.crops,
          });
        }

        return ret;
      },
      produceData() {
        let data = null;
        let areaTotals = {};
        let fields = ["crops", "animals", "mineral_resources"];
        let totalSize = 0;
        console.log(this.dealsWithProduceInfo);
        if (
          this.deals.length > 0 &&
          this.deals.length === this.dealsWithProduceInfo.length &&
          !this.$apollo.loading
        ) {
          data = {};
          // map deals for faster access
          let dealMap = {};
          for (let deal of this.deals) dealMap[deal.id] = deal;

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
        // console.log("tree data changed.", this.treeData);
        buildTreeChart(this.treeData);
      },
    },
    methods: {
      toggleContextContainer() {
        buildTreeChart(this.treeData);
      },
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
    },
  });
</script>

<style lang="scss" scoped>
  #produce-info {
    width: 100%;
    height: 100%;
    padding: 3em;
    align-self: safe center;

    > svg {
      max-height: 100%;
      max-width: 100%;
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
