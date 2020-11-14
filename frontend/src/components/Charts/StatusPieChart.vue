<template>
  <div>
    <div class="chart-container">
      <canvas ref="chart-canvas"></canvas>
    </div>
    <Legend v-if="displayLegend || legends" :items="legendItems"></Legend>
  </div>
</template>

<script>
  import Chart from "chart.js";
  import Legend from "./Legend";
  import numeral from "numeral";

  export default {
    components: { Legend },
    props: ["dealData", "displayLegend", "legends", "aspectRatio"],
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
          legend: {
            display: false,
          },
          aspectRatio: this.aspectRatio || 2,
          responsive: true,
          title: {
            display: false,
            text: this.title,
          },
          animation: {
            animateScale: true,
            animateRotate: true,
          },
          tooltips: {
            callbacks: {
              label: (item, data) => {
                let origItem = this.dealData[item.datasetIndex];
                let label = data.labels[item.index];
                let value = data.datasets[item.datasetIndex].data[item.index];
                if (origItem.precision) {
                  value = numeral(value).format(
                    "0,0." + "0".repeat(origItem.precision)
                  );
                } else {
                  value = numeral(value).format("0,0");
                }
                let unit = origItem.unit ? " " + origItem.unit : "";
                label = `${label}: ${value}${unit}`;
                return label;
              },
            },
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
              data: this.dealData.map((n) => {
                return n.value;
              }),
              backgroundColor: this.dealData.map((n) => {
                return n.color;
              }),
            },
          ],
        };
      },
      legendItems() {
        if (this.legends) return this.legends;
        else return this.dealData;
      },
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
    mounted() {
      this.createChart();
    },
    watch: {
      dealData: {
        deep: true,
        handler: function () {
          this.updateChart();
        },
      },
    },
  };
</script>

<style lang="scss" scoped>
  .chart-container {
    width: 90%;
    max-width: 200px;
    margin: auto;
  }
</style>