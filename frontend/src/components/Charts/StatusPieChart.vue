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
    // ArcElement,
    // LineElement,
    // BarElement,
    // PointElement,
    // BarController,
    // BubbleController,
    // DoughnutController,
    // LineController,
    // PieController,
    // PolarAreaController,
    // RadarController,
    // ScatterController,
    // CategoryScale,
    // LinearScale,
    // LogarithmicScale,
    // RadialLinearScale,
    // TimeScale,
    // TimeSeriesScale,
    // Decimation,
    // Filler,
    // Title,
    // Tooltip,
    // SubTitle,
    registerables,
  } from "chart.js";
  import numeral from "numeral";
  // import Legend from "./Legend";
  import Vue from "vue";

  Chart.register(...registerables);
  // Chart.register(
  //   ArcElement,
  //   LineElement,
  //   BarElement,
  //   PointElement,
  //   BarController,
  //   BubbleController,
  //   DoughnutController,
  //   LineController,
  //   PieController,
  //   PolarAreaController,
  //   RadarController,
  //   ScatterController,
  //   CategoryScale,
  //   LinearScale,
  //   LogarithmicScale,
  //   RadialLinearScale,
  //   TimeScale,
  //   TimeSeriesScale,
  //   Decimation,
  //   Filler,
  //   Title,
  //   Tooltip,
  //   SubTitle
  // );

  export default Vue.extend({
    name: "StatusPieChart",
    // components: { Legend },
    props: {
      dealData: { type: Array, required: true },
      aspectRatio: { type: Number, default: 2 },
      maxWidth: { type: String, default: "200px" },
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
      containerStyle() {
        return {
          maxWidth: this.maxWidth,
        };
      },
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
            tooltip: {
              callbacks: {
                label: (item, data) => {
                  console.log({ item, data });
                  // let origItem = this.dealData[item.datasetIndex];
                  // let label = data.labels[item.index];
                  // let value = data.datasets[item.datasetIndex].data[item.index];
                  // console.log({ origItem, label, value });
                  return "xx";
                },
                // label: (item, data) => {
                //   if (origItem.precision) {
                //     value = numeral(value).format(
                //       "0,0." + "0".repeat(origItem.precision)
                //     );
                //   } else {
                //     value = numeral(value).format("0,0");
                //   }
                //   label = `${label}: ${value}${this.unit ? ` ${this.unit}` : ""}`;
                //   return label;
                // },
              },
            },
          },
          aspectRatio: this.aspectRatio,
          responsive: true,
          title: {
            display: false,
            text: this.title,
          },
          animation: {
            animateScale: true,
            animateRotate: true,
            duration: 0,
          },
        };
      },
      chartdata() {
        return {
          labels: this.dealData.map((n) => {
            return n.label;
          }),
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
