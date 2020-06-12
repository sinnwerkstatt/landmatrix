<template>
  <div class="container">
    <div class="row" v-if="countries">
      <div class="col">
        <multiselect
          v-model="selectedCountry"
          :options="countries"
          label="name"
          placeholder="World"
          @input="updateStats"
        />
      </div>
      <div class="col">
        <select v-model="selectedDateOption" @change="updateDateRange($event)">
          <option v-for="option in date_pre_options" :value="option.value">
            {{ option.name }}
          </option>
        </select>
        <v-date-picker
          mode="range"
          v-model="daterange"
          :max-date="new Date()"
          @input="updateStats"
        />
      </div>
    </div>
    <h2>Number of deals</h2>

    <div class="row" v-if="deals">
      <table>
        <thead>
          <tr>
            <th>Added</th>
            <th>Updated</th>
            <th>Published</th>
            <th>Pending</th>
            <th>Rejected</th>
            <th>Pending deletions</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ deals_added.length }}</td>
            <td>{{ deals_updated.length }}</td>
            <td>{{ deals_published.length }}</td>
            <td>{{ deals_pending.length }}</td>
            <td>{{ deals_rejected.length }}</td>
            <td>{{ deals_pending_deletion.length }}</td>
          </tr>
          <tr>
            <td>
              <span v-for="deal in deals_added">{{ deal.id }} </span>
            </td>
            <td>
              <span v-for="deal in deals_updated">{{ deal.id }} </span>
            </td>
            <td>
              <span v-for="deal in deals_published">{{ deal.id }} </span>
            </td>
            <td>
              <span v-for="deal in deals_pending">{{ deal.id }} </span>
            </td>
            <td>
              <span v-for="deal in deals_rejected">{{ deal.id }} </span>
            </td>
            <td>
              <span v-for="deal in deals_pending_deletion">{{ deal.id }} </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
  import axios from "axios";
  import dayjs from "dayjs";

  export default {
    data: function () {
      return {
        today: dayjs().format("YYYY/MM/DD"),
        daterange: {},
        selectedCountry: null,

        deals: null,

        selectedDateOption: 30,
        date_pre_options: [
          { name: "Last 30 days", value: 30 },
          { name: "Last 60 days", value: 60 },
          { name: "Last 180 days", value: 180 },
          { name: "Last 365 days", value: 365 },
        ],
      };
    },
    computed: {
      regions() {
        return this.$store.state.page.regions;
      },
      countries() {
        return this.$store.state.page.countries;
      },
      deals_added() {
        if (this.deals)
          return this.deals.filter((d) => {
            return d.status === 3;
          });
      },
      deals_updated() {
        if (this.deals)
          return this.deals.filter((d) => {
            return d.status === 2;
          });
      },
      deals_published() {
        if (this.deals)
          return this.deals.filter((d) => {
            return d.status === 2 || d.status === 3;
          });
      },
      deals_pending() {
        if (this.deals)
          return this.deals.filter((d) => {
            return d.status === 3 || d.status === 1;
          });
      },
      deals_rejected() {
        if (this.deals)
          return this.deals.filter((d) => {
            return d.status === 5;
          });
      },
      deals_pending_deletion() {
        if (this.deals)
          return this.deals.filter((d) => {
            return d.status === 6;
          });
      },
    },
    methods: {
      updateDateRange() {
        this.daterange = {
          start: dayjs().subtract(this.selectedDateOption, "day").toDate(),
          end: new Date(),
        };
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
        if (this.selectedCountry) {
          variables.filters.push({
            field: "target_country.id",
            operation: "EQ",
            value: this.selectedCountry.id.toString(),
          });
        }
        axios.post("/graphql/", { query, variables }).then((response) => {
          this.deals = response.data.data.deals;
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
