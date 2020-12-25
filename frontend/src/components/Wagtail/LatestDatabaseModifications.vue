<template>
  <table
    v-if="modifications"
    id="latest-database-modifications"
    class="table table-striped"
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
            :to="{ name: 'deal_detail', params: { dealId: deal.id } }"
            class="label label-default"
          >
            {{ deal.id }}
          </router-link>
        </td>
        <td>{{ dayjs(deal.modified_at).format("YYYY-MM-DD") }}</td>
        <td>{{ $t(parse_status(deal.status)) }}</td>
        <td>{{ deal.country ? deal.country.name : "" }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import gql from "graphql-tag";
  import dayjs from "dayjs";
  export default {
    props: ["value"],
    data: function () {
      return {
        modifications: [],
        deals: [],
      };
    },
    apollo: {
      modifications: {
        query: gql`
          query Deals($limit: Int!, $subset: Subset, $filters: [Filter]) {
            modifications: deals(
              sort: "-modified_at"
              subset: $subset
              limit: $limit
              filters: $filters
            ) {
              id
              country {
                name
              }
              status
              modified_at
            }
          }
        `,
        update: (data) => data.deals,
        variables() {
          return {
            limit: +this.value.limit,
            filters: this.current_region_or_country,
            subset: this.$store.getters.userAuthenticated ? "ACTIVE" : "PUBLIC",
          };
        },
      },
    },
    computed: {
      current_region_or_country() {
        let wtpage = this.$store.state.page.wagtailPage;
        if (wtpage.meta.type === "wagtailcms.RegionPage") {
          return [
            {
              field: "country.fk_region_id",
              value: wtpage.region.id.toString(),
            },
          ];
        }
        if (wtpage.meta.type === "wagtailcms.CountryPage") {
          return [
            {
              field: "country_id",
              value: wtpage.country.id.toString(),
            },
          ];
        }

        return [];
      },
    },
    methods: {
      dayjs,
      parse_status(status) {
        return {
          1: "Draft",
          2: "Live",
          3: "Updated",
          4: "Deleted",
          5: "Rejected",
          6: "To Delete",
        }[status];
      },
    },
  };
</script>
