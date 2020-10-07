<template>
  <div class="chart-container">
    <h5>{{ title }}</h5>
    <canvas id="myChart" ref="myChart"></canvas>
  </div>
</template>

<script>
  import Chart from "chart.js";

  export default {
    props: ["dealData", "title"],
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
          aspectRatio: 1,
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
            // {
            //   label: "Hectares",
            //   data: neg_status.map((n) => {
            //     return n.hectares;
            //   }),
            //   backgroundColor: ["#83C3C2", "#153838", "#44B7B6", "#263838", "#318583"],
            // },
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
          let chart_container = document.getElementById("myChart");
          // this.canvasCtx = this.$refs.myChart.getContext("2d");
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
    width: 100%;
    min-height: 300px;
  }

</style>
