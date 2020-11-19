<template>
  <div>
    <canvas id="myChart" ref="myChart"></canvas>
  </div>
</template>

<script>
  import Chart from "chart.js";

  let neg_status = [
    {
      name: "Project not started",
      deals: 76,
      hectares: 2357261,
    },
    {
      name: "Startup phase (no production)",
      deals: 155,
      hectares: 3568599,
    },
    {
      name: "In operation (production)",
      deals: 1317,
      hectares: 35710546,
    },
    {
      name: "Project abandoned",
      deals: 119,
      hectares: 3854423,
    },
  ];

  let chartoptions = {
    cutoutPercentage: 25,
    legend: {
      display: true,
      position: "top",
    },
    responsive: true,
    title: {
      display: true,
      text: "Implementation status",
    },
    animation: {
      animateScale: true,
      animateRotate: true,
    },
    tooltips: {
      callbacks: {
        label: function (item, data) {
          console.log(data.labels, item);
          return (
            data.datasets[item.datasetIndex].label +
            ": " +
            data.labels[item.index] +
            ": " +
            data.datasets[item.datasetIndex].data[item.index]
          );
        },
      },
    },
  };
  let chartdata = {
    labels: neg_status.map((n) => {
      return n.name;
    }),
    datasets: [
      {
        label: "Hectares",
        data: neg_status.map((n) => {
          return n.hectares;
        }),
        backgroundColor: ["#83C3C2", "#153838", "#44B7B6", "#263838", "#318583"],
      },
      {
        label: "Number of deals",
        data: neg_status.map((n) => {
          return n.deals;
        }),
        backgroundColor: ["#FDB86A", "#7D4A0F", "#FC941F", "#7D5B34", "#C97718"],
      },
    ],
  };

  export default {
    data: function () {
      return {
        canvasCtx: null,
        chart: null,
      };
    },
    methods: {
      dothechart() {
        // this.canvasCtx = this.$refs.myChart.getContext("2d");
        this.chart = new Chart(document.getElementById("myChart"), {
          type: "pie",
          data: chartdata,
          options: chartoptions,
        });
      },
    },
    mounted() {
      this.dothechart();
    },
  };
</script>

<style lang="scss" scoped></style>
