import gql from "graphql-tag";

export const data_deal_query_gql = gql`
  query Deals($limit: Int!, $subset: Subset, $filters: [Filter]) {
    deals(limit: $limit, subset: $subset, filters: $filters) {
      id
      deal_size
      country {
        id
        fk_region {
          id
        }
      }
      current_intention_of_investment
      current_negotiation_status
      current_implementation_status
      locations {
        id
        point
        level_of_accuracy
      }
      fully_updated_at # for listing
      operating_company {
        # for map pin popover & listing
        id
      }
      top_investors {
        # for listing
        id
      }
    }
  }
`;

export const data_deal_query = {
  query: data_deal_query_gql,
  variables() {
    let user = this.$store.state.page.user;
    return {
      limit: 0,
      filters: this.$store.getters.filtersForGQL,
      subset: user && user.is_authenticated ? "ACTIVE" : "PUBLIC",
    };
  },
};

export const data_deal_produce_query = {
  query: gql`
    query Deals($limit: Int!, $subset: Subset, $filters: [Filter]) {
      dealsWithProduceInfo: deals(limit: $limit, subset: $subset, filters: $filters) {
        id
        crops
        animals
        resources
      }
    }
  `,
  variables() {
    let user = this.$store.state.page.user;
    return {
      limit: 0,
      filters: this.$store.getters.filtersForGQL,
      subset: user && user.is_authenticated ? "ACTIVE" : "PUBLIC",
    };
  },
};
