<template>
  <div>
    <div class="chart-container" :style="containerStyle">
      <canvas ref="chart-canvas"></canvas>
    </div>
    <!--    <Legend v-if="legendItems && (displayLegend || legends)" :items="legendItems" />-->
  </div>
</template>

<script lang="ts">
  import {
    Chart,
    ArcElement,
    PieController,
    Title,
    Tooltip,
    Legend,
    SubTitle,
  } from "chart.js";
  import numeral from "numeral";

  import Vue from "vue";

  Chart.register(ArcElement, PieController, Legend, Tooltip, SubTitle, Title);

  export default Vue.extend({
    name: "StatusPieChart",
    // components: { Legend },
    props: {
      dealData: { type: Array, required: true },
      aspectRatio: { type: Number, default: 2 },
      containerStyle: { type: Object, default: () => ({ maxWidth: "auto" }) },
      unit: { type: String, required: false, default: null },
      valueField: { type: String, default: "value" },
      // legends: { type: Object, default: null },
    },
    data: function () {
      return {
        canvasCtx: null,
        chart: null,
      };
    },
    computed: {
      chartoptions() {
        return {
          cutoutPercentage: 0,
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                boxWidth: 10,
                textAlign: "left",
              },
            },
            // title: { display: true, text: "Custom Chart Title" },
            tooltip: {
              callbacks: {
                label: (context) => {
                  let value = context.dataset.data[context.dataIndex];
                  value = numeral(value).format("0,0");
                  if (this.unit) value += ` ${this.unit}`;
                  return `${context.label}: ${value}`;
                },
              },
            },
          },
          aspectRatio: this.aspectRatio,
          responsive: true,
        };
      },
      chartdata() {
        return {
          labels: this.dealData.map((n) => n.label),
          datasets: [
            {
              data: this.dealData.map((n) => n[this.valueField]),
              backgroundColor: this.dealData.map((n) => n.color),
            },
          ],
        };
      },
      legendItems() {
        if (this.legends) return this.legends;
        else return this.dealData;
      },
    },
    watch: {
      dealData: {
        deep: true,
        handler() {
          this.updateChart();
        },
      },
      valueField: {
        handler() {
          this.updateChart();
        },
      },
    },
    mounted() {
      this.createChart();
    },
    methods: {
      createChart() {
        if (this.dealData) {
          let chart_container = this.$refs["chart-canvas"];
          this.chart = new Chart(chart_container, {
            type: "pie",
            data: this.chartdata,
            options: this.chartoptions,
          });
        }
      },
      updateChart() {
        if (this.chart && this.dealData) {
          this.chart.data = this.chartdata;
          this.chart.update();
        } else {
          this.createChart();
        }
      },
    },
  });
</script>

<style lang="scss" scoped>
  .chart-container {
    width: 90%;
    margin: auto;
  }
</style>
