import { gql } from "graphql-tag";

export const data_deal_query_gql = gql`
  query ($limit: Int!, $subset: Subset, $filters: [Filter]) {
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
      current_contract_size
      current_implementation_status
      current_crops
      current_animals
      current_mineral_resources
      intended_size
      locations
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
