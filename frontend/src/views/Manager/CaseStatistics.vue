<template>
  <div class="container">
    <div class="row" v-if="countries">
      <multiselect
        v-model="selectedCountry"
        :options="countries"
        label="name"
        placeholder="Pick a value"
      ></multiselect>
      <select v-model="selectedDateOption" @change="updateDateRange($event)">
        <option v-for="option in date_pre_options" :value="option.value">{{option.name}}</option>
      </select>
      <v-date-picker
        mode="range"
        v-model="daterange"
        :max-date="new Date()"
        @input="updateStats"
      />
    </div>
    <div class="row">
      <h2>Number of deals</h2>
      Added: {{ deals_added }}<br />
      Updated: {{ deals_updated }}<br />
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import store from "@/store";
  import dayjs from "dayjs";

  export default {
    data: function () {
      return {
        today: dayjs().format("YYYY/MM/DD"),
        daterange: {},
        selectedCountry: null,

        deals_added: null,
        deals_updated: null,

        selectedDateOption: null,
        date_pre_options: [
          {name: "Last 30 days", value: 30},
          {name: "Last 90 days", value: 90},
          {name: "Last 180 days", value: 180},
          {name: "Last 365 days", value: 365},
        ]
      };
    },
    computed: {
      regions() {
        return this.$store.state.page.regions;
      },
      countries() {
        return this.$store.state.page.countries;
      },
    },
    methods: {
      updateDateRange() {
        this.daterange = {start: dayjs().subtract(this.selectedDateOption, "day").toDate(), end: new Date()};
      },
      updateStats() {
        let query = `query Stats($filters: [Filter]) {
          deals(sort:"timestamp", limit: 0, filters: $filters) { id deal_size fully_updated status confidential }
        }`;
        let variables = {
          filters: [
            {
              field: "timestamp",
              operation: "GE",
              value: dayjs(this.daterange.start).format("YYYY-MM-DD"),
            },
            {
              field: "timestamp",
              operation: "LE",
              value: dayjs(this.daterange.end).format("YYYY-MM-DD"),
            },
          ],
        };
        axios.post("/graphql/", { query, variables }).then((response) => {
          this.deals_added = response.data.data.deals;
        });
      },
    },
    created() {},
    beforeRouteEnter(to, from, next) {
      next();
    },
  };
</script>

<style scoped></style>
