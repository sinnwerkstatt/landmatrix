import gql from "graphql-tag";
import { OperationVariables } from "apollo-client/core/types";

export const data_deal_query_gql = gql`
  query Deals($limit: Int!, $subset: Subset, $filters: [Filter]) {
    deals(limit: $limit, subset: $subset, filters: $filters) {
      id
      deal_size
      country {
        id
        name
        fk_region {
          id
        }
      }
      current_intention_of_investment
      current_negotiation_status
      current_implementation_status
      locations
      #      locations {
      #        id
      #        point
      #        level_of_accuracy
      #      }
      fully_updated_at # for listing
      operating_company {
        # for map pin popover & listing
        id
        name
      }
      top_investors {
        # for listing
        id
        name
        classification
      }
    }
  }
`;

export const data_deal_query = {
  query: data_deal_query_gql,
  variables(): OperationVariables {
    return {
      limit: 0,
      filters: this.$store.getters.filtersForGQL,
      subset: this.$store.getters.userAuthenticated
        ? this.$store.state.filters.publicOnly
          ? "PUBLIC"
          : "ACTIVE"
        : "PUBLIC",
    };
  },
  debounce: 200,
};

export const data_deal_produce_query = {
  query: gql`
    query Deals($limit: Int!, $subset: Subset, $filters: [Filter]) {
      dealsWithProduceInfo: deals(limit: $limit, subset: $subset, filters: $filters) {
        id
        current_crops
        current_animals
        current_mineral_resources
      }
    }
  `,
  variables(): OperationVariables {
    return {
      limit: 0,
      filters: this.$store.getters.filtersForGQL,
      subset: this.$store.getters.userAuthenticated
        ? this.$store.state.filters.publicOnly
          ? "PUBLIC"
          : "ACTIVE"
        : "PUBLIC",
    };
  },
};
