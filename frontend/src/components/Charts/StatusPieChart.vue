<template>
  <div class="chart-container">
    <canvas ref="chart-canvas"></canvas>
  </div>
</template>

<script>
  import Chart from "chart.js";

  export default {
    props: ["dealData"],
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
            display: true,
            position: "bottom",
            align: "start",
            fullWidth: false,
            labels: {
              boxWidth: 10,
              padding: 5,
            },
          },
          aspectRatio: 1.3,
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
