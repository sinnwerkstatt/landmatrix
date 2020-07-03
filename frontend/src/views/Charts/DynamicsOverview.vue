<template>
  <div class="">
    <ul class="nav nav-pills nav-fill">
      <li class="nav-item">
        <a class="nav-link active" href="#">Intention of investment</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Negotiation status</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Implementation status</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Investment in Agriculture</a>
      </li>
    </ul>
    <div style="height: 300px;">
      <canvas id="myChart" ref="myChart" height="100%"></canvas>
    </div>
  </div>
</template>

<script>
  import store from "@/store";
  import Chart from "chart.js";

  let neg_status = [
    {
      name: "Intended (Expression of interest)",
      deals: 144,
      hectares: 9730586,
    },
    {
      name: "Intended (Under negotiation)",
      deals: 215,
      hectares: 9190533,
    },
    {
      name: "Intended (Memorandum of understanding)",
      deals: 25,
      hectares: 2727129,
    },
    {
      name: "Concluded (Oral Agreement)",
      deals: 151,
      hectares: 2314975,
    },
    {
      name: "Concluded (Contract signed)",
      deals: 3760,
      hectares: 120445330,
    },
    {
      name: "Failed (Negotiations failed)",
      deals: 125,
      hectares: 11239909,
    },
    {
      name: "Failed (Contract cancelled)",
      deals: 110,
      hectares: 3750871,
    },
    {
      name: "Contract expired",
      deals: 6,
      hectares: 28915,
    },
    {
      name: "Change of ownership",
      deals: 16,
      hectares: 740102,
    },
  ];

  export default {
    data: function () {
      return {
        canvasCtx: null,
        chart: null,
      };
    },
    computed: {},
    mounted() {
      this.canvasCtx = this.$refs.myChart.getContext("2d");
      this.chart = new Chart(this.canvasCtx, {
        type: "bar",
        data: {
          labels: neg_status.map((n) => {
            return n.name;
          }),
          datasets: [
            {
              label: "deal size / ha",
              backgroundColor: "#44b7b6",
              data: neg_status.map((n) => {
                return n.hectares;
              }),
              borderWidth: 1,
            },
            {
              label: "deal count",
              backgroundColor: "#fc941f",
              yAxisID: "B",
              data: neg_status.map((n) => {
                return n.deals;
              }),
            },
          ],
        },
        options: {
          scales: {
            yAxes: [
              {
                ticks: { beginAtZero: true },
                id: "A",
                type: "linear",
                position: "left",
              },
              {
                id: "B",
                type: "linear",
                position: "right",
              },
            ],
          },
        },
      });
    },
    methods: {},
    beforeRouteEnter(to, from, next) {
      let title = "Dynamics Overview";
      store.dispatch("setPageContext", {
        title,
        breadcrumbs: [
          { link: { name: "wagtail" }, name: "Home" },
          { link: { name: "charts" }, name: "Charts" },
          { name: title },
        ],
      });
      next();
    },
  };
</script>

<style lang="scss" scoped>
  @import "../../scss/colors";

  .nav-pills .nav-link.active {
    background: $primary;
  }
</style>
