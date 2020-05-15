<template>
  <div class="container">
    <div class="row" v-if="countries">
      <multiselect
        v-model="selectedCountry"
        :options="countries"
        label="name"
        placeholder="Pick a value"
      ></multiselect>
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
      updateStats() {
        let query = `query Stats($filters: [Filter]) {
          deals(sort:"timestamp", filters: $filters) { id deal_size }
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
