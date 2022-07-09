import { gql } from "graphql-tag";

export const investor_gql_query = gql`
  query Investor(
    $id: Int!
    $version: Int
    $subset: Subset
    $depth: Int
    $includeDeals: Boolean!
  ) {
    investor(
      id: $id
      version: $version
      subset: $subset
      involvements_depth: $depth
      involvements_include_ventures: true
    ) {
      id
      name
      country {
        id
        name
      }
      classification
      homepage
      opencorporates
      datasources
      comment
      status
      draft_status
      created_at
      modified_at
      investors {
        id
        investment_type
        role
        parent_relation
        percentage
        investor {
          id
          name
          classification
          country {
            id
          }
        }
      }
      ventures {
        id
        investment_type
        role
        parent_relation
        percentage
        venture {
          id
          name
          classification
          country {
            id
          }
        }
      }
      deals @include(if: $includeDeals) {
        id
        country {
          id
          name
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
      involvements
      workflowinfos {
        id
        from_user {
          id
          username
          full_name
        }
        to_user {
          username
          full_name
        }
        draft_status_before
        draft_status_after
        timestamp
        comment
        processed_by_receiver
      }
      versions {
        id
        investor {
          status
          draft_status
        }
        created_at
        created_by {
          id
          full_name
        }
        object_id
      }
    }
  }
`;
