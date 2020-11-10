import gql from "graphql-tag";

export const data_deal_query = {
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
        current_intention_of_investment
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
      filters: this.$store.getters.filtersForGQL,
    };
  },
};

export const data_deal_produce_query = {
  query: gql`
    query Deals($limit: Int!, $filters: [Filter]) {
      dealsWithProduceInfo: deals(limit: $limit, filters: $filters) {
        id
        crops
        animals
        resources
      }
    }
  `,
  variables() {
    return {
      limit: 0,
      filters: this.$store.getters.filtersForGQL,
    };
  },
};
