<template>
  <div class="chart-container">
    <canvas id="myChart" ref="myChart"></canvas>
  </div>
</template>

<script>
  import Chart from "chart.js";
  import ChartDataLabels from 'chartjs-plugin-datalabels';

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
            display: false,
            position: "top",
          },
          aspectRatio: 1,
          responsive: true,
          title: {
            display: true,
            text: "Status",
          },
          animation: {
            animateScale: true,
            animateRotate: true,
          },
          plugins: {
            datalabels: {
              anchor: "end",
              offset: 10,
              formatter: (value, context) => {
                return this.dealData[context.dataIndex].label + ': ' + value;
              }
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
            // {
            //   label: "Hectares",
            //   data: neg_status.map((n) => {
            //     return n.hectares;
            //   }),
            //   backgroundColor: ["#83C3C2", "#153838", "#44B7B6", "#263838", "#318583"],
            // },
            {
              label: "Number of deals",
              data: this.dealData.map((n) => {
                return n.count;
              }),
              backgroundColor: ["#FDB86A", "#7D4A0F", "#FC941F", "#7D5B34", "#C97718"],
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
