<template>
  <table
    class="table table-striped"
    id="latest-database-modifications"
    v-if="modifications"
  >
    <thead>
      <tr>
        <th>Deal #</th>
        <th>Date</th>
        <th>Status</th>
        <th>Target country</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="deal in modifications" :key="deal.id">
        <td>
          <router-link
            :to="{ name: 'deal_detail', params: { deal_id: deal.id } }"
            class="label label-default"
            v-slot="{ href }"
          >
            <a :href="href">{{ deal.id }}</a>
          </router-link>
        </td>
        <td>{{ deal.timestamp }}</td>
        <td>{{ deal.status }}</td>
        <td>{{ deal.country }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import axios from "axios";

  export default {
    props: ["value"],
    data: function () {
      return {
        modifications: [],
      };
    },
    created() {
      let query = `{ deals(sort:"-timestamp", limit: ${this.value.limit})
      { id country { name } status timestamp }
      }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        this.modifications = response.data.data.deals.map((d) => {
          return {
            id: d.id,
            timestamp: d.timestamp.split("T")[0],
            country: d.country.name,
            status: "TODO",
          };
        });
      });
    },
  };
</script>
