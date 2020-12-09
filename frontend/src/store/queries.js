import gql from "graphql-tag";

export const blogpage_query = {
  query: gql`
    query Article($id: Int!) {
      blogpage(id: $id) {
        id
        title
        body
        date
        tags {
          slug
          name
        }
      }
    }
  `,
  variables() {
    return {
      id: this.$store.state.page.wagtailPage.id,
    };
  },
};

export const blogpages_query = gql`
  query {
    blogpages {
      id
      title
      slug
      date
      header_image
      excerpt
      categories {
        slug
      }
      tags {
        slug
      }
    }
  }
`;

export const blogcategories_query = gql`
  query {
    blogcategories {
      id
      name
      slug
    }
  }
`;

export const global_rankings_query = gql`
  query {
    global_rankings
  }
`;

export const country_investments_and_rankings_query = {
  query: gql`
    query InvestmentsAndRankings($id: Int!, $filters: [Filter]) {
      country_investments_and_rankings(id: $id, filters: $filters)
    }
  `,
  variables() {
    return {
      id: +this.country_id,
      filters: this.filters,
    };
  },
  skip() {
    return !this.country_id;
  },
};

export const investors_query = {
  query: gql`
    query Investors($limit: Int!, $subset: Subset) {
      investors(limit: $limit, subset: $subset) {
        id
        name
      }
    }
  `,
  variables() {
    let user = this.$store.state.page.user;
    return {
      limit: 0,
      subset: user && user.is_authenticated ? "ACTIVE" : "PUBLIC",
    };
  },
};

export const investor_query = {
  query: gql`
    query Investor($investorID: Int!, $depth: Int, $includeDeals: Boolean!) {
      investor(id: $investorID) {
        id
        name
        country {
          id
          name
        }
        classification
        homepage
        opencorporates
        comment
        # involvements
        status
        created_at
        modified_at
        deals @include(if: $includeDeals) {
          id
          country {
            id
          }
          recognition_status
          nature_of_deal
          intention_of_investment
          negotiation_status
          implementation_status
          current_intention_of_investment
          current_negotiation_status
          current_implementation_status
          deal_size
        }
        involvements(depth: $depth)
      }
    }
  `,
  variables() {
    return {
      investorID: +this.investor_id,
      depth: this.depth,
      includeDeals: this.includeDealsInQuery,
    };
  },
  update(data) {
    if (!data.investor) {
      this.$router.push({
        name: "404",
        params: [this.$router.currentRoute.path],
        replace: true,
      });
    }
    return data.investor;
  },
};

export const deal_aggregations_query = {
  query: gql`
    query DealAggregations($fields: [String]!, $subset: Subset, $filters: [Filter]) {
      deal_aggregations(fields: $fields, subset: $subset, filters: $filters)
    }
  `,
  variables() {
    let user = this.$store.state.page.user;
    return {
      fields: ["current_negotiation_status"],
      filters: this.locationFilter,
      subset: user && user.is_authenticated ? "ACTIVE" : "PUBLIC",
    };
  },
};
