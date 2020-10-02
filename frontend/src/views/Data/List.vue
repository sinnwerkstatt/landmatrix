<template>
  <div>
    <DataContainer>
      <template v-slot:default>
        <LoadingPulse v-if="$apollo.queries.deals.loading" />
        asdfasdf
      </template>
    </DataContainer>
  </div>
</template>

<script>
  import gql from "graphql-tag";
  import DataContainer from "./DataContainer";
  import LoadingPulse from "/components/Data/LoadingPulse";

  export default {
    name: "DataList",
    components: { LoadingPulse, DataContainer },
    apollo: {
      deals: {
        query: gql`
          query Deals($limit: Int!, $filters: [Filter]) {
            deals(limit: $limit, filters: $filters) {
              id
              deal_size
              country {
                id
                fk_region {
                  id
                }
              }
              # top_investors { id name }
              intention_of_investment
              current_negotiation_status
              current_implementation_status
              locations {
                id
                point
                level_of_accuracy
              }
            }
          }
        `,
        variables() {
          return {
            limit: 0,
            filters: this.$store.getters.filtersForGQL
          };
        }
      }
    },
    data() {
      return {
        deals: []
      };
    }
  };
</script>
<style lang="scss"></style>
