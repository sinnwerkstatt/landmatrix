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
  import Legend from "./Legend.vue";

  export default {
    components: {Legend},
    props: ["dealData", "displayLegend", "legends"],
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
          aspectRatio: 2,
          responsive: true,
          title: {
            display: false,
            text: this.title,
          },
          animation: {
            animateScale: true,
            animateRotate: true,
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
              backgroundColor:this.dealData.map((n) => {
                return n.color;
              }),
            },
          ],
        };
      },
      legendItems() {
        if (this.legends) return this.legends;
        else return this.dealData;
      }
    },
    methods: {
      createChart() {
        if (this.dealData) {
          let chart_container = this.$refs['chart-canvas'];
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
      }
    },
    mounted() {
      this.createChart();
    },
    watch: {
      dealData: {
        deep: true,
        handler: function() {
          this.updateChart();
        }
      }
    }
  };
</script>

<style lang="scss" scoped>

  .chart-container{
    width: 90%;
    max-width: 200px;
    margin: auto;
  }

</style>
