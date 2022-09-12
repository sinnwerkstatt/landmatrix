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
      id: this.$store.state.wagtailPage.id,
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
      url
    }
  }
`;

export const blogcategories_query = {
  query: gql`
    query ($language: String) {
      blogcategories(language: $language) {
        id
        name
        slug
      }
    }
  `,
  variables() {
    return { language: this.$i18n.locale };
  },
};

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
        resolved
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

export const investor_edit_query = gql`
  query Investor($id: Int!, $version: Int) {
    investor(id: $id, version: $version, subset: UNFILTERED) {
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
      created_at
      modified_at
      investors {
        id
        investor {
          id
          name
        }
        role
        investment_type
        percentage
        loans_amount
        loans_currency {
          id
          code
          name
        }
        loans_date
        parent_relation
        comment
      }
    }
  }
`;

export const markers_query = {
  query: gql`
    query Markers($region_id: Int, $country_id: Int) {
      markers(region_id: $region_id, country_id: $country_id)
    }
  `,
  variables() {
    return { region_id: +this.regionId, country_id: +this.countryId };
  },
};

export const deal_gql_query = gql`
  query Deal($id: Int!, $version: Int, $subset: Subset) {
    deal(id: $id, version: $version, subset: $subset) {
      id
      # General Info
      ## Land area
      country {
        id
        name
        code_alpha2
        point_lat_min
        point_lat_max
        point_lon_min
        point_lon_max
      }
      intended_size
      contract_size
      production_size
      land_area_comment
      ## Intention of investment
      intention_of_investment
      intention_of_investment_comment
      ## Nature of the deal
      nature_of_deal
      nature_of_deal_comment
      negotiation_status
      negotiation_status_comment
      implementation_status
      implementation_status_comment
      ## Purchase price
      purchase_price
      purchase_price_currency {
        id
        name
      }
      purchase_price_type
      purchase_price_area
      purchase_price_comment
      ## Leasing fees
      annual_leasing_fee
      annual_leasing_fee_currency {
        id
        name
      }
      annual_leasing_fee_type
      annual_leasing_fee_area
      annual_leasing_fee_comment
      ## Contract farming
      contract_farming
      on_the_lease_state
      on_the_lease
      off_the_lease_state
      off_the_lease
      contract_farming_comment
      # Employment
      total_jobs_created
      total_jobs_planned
      total_jobs_planned_employees
      total_jobs_planned_daily_workers
      total_jobs_current
      total_jobs_created_comment
      foreign_jobs_created
      foreign_jobs_planned
      foreign_jobs_planned_employees
      foreign_jobs_planned_daily_workers
      foreign_jobs_current
      foreign_jobs_created_comment
      domestic_jobs_created
      domestic_jobs_planned
      domestic_jobs_planned_employees
      domestic_jobs_planned_daily_workers
      domestic_jobs_current
      domestic_jobs_created_comment
      # Investor info
      operating_company {
        id
        name
      }
      involved_actors
      project_name
      investment_chain_comment
      # Local communities / indigenous peoples
      name_of_community
      name_of_indigenous_people
      people_affected_comment
      recognition_status
      recognition_status_comment
      community_consultation
      community_consultation_comment
      community_reaction
      community_reaction_comment
      land_conflicts
      land_conflicts_comment
      displacement_of_people
      displaced_people
      displaced_households
      displaced_people_from_community_land
      displaced_people_within_community_land
      displaced_households_from_fields
      displaced_people_on_completion
      displacement_of_people_comment
      negative_impacts
      negative_impacts_comment
      promised_compensation
      received_compensation
      promised_benefits
      promised_benefits_comment
      materialized_benefits
      materialized_benefits_comment
      presence_of_organizations
      # Former user
      former_land_owner
      former_land_owner_comment
      former_land_use
      former_land_use_comment
      former_land_cover
      former_land_cover_comment
      # Produce info
      crops
      crops_comment
      animals
      animals_comment
      mineral_resources
      mineral_resources_comment
      contract_farming_crops
      contract_farming_crops_comment
      contract_farming_animals
      contract_farming_animals_comment
      has_domestic_use
      domestic_use
      has_export
      export
      export_country1 {
        id
        name
      }
      export_country1_ratio
      export_country2 {
        id
        name
      }
      export_country2_ratio
      export_country3 {
        id
        name
      }
      export_country3_ratio
      use_of_produce_comment
      in_country_processing
      in_country_processing_comment
      in_country_processing_facilities
      in_country_end_products
      # Water
      water_extraction_envisaged
      water_extraction_envisaged_comment
      source_of_water_extraction
      source_of_water_extraction_comment
      how_much_do_investors_pay_comment
      water_extraction_amount
      water_extraction_amount_comment
      use_of_irrigation_infrastructure
      use_of_irrigation_infrastructure_comment
      water_footprint
      # Gender-related info
      gender_related_information
      # Overall comment
      overall_comment
      # Meta
      created_at
      created_by {
        id
        username
      }
      modified_at
      modified_by {
        id
        username
      }
      fully_updated
      fully_updated_at
      confidential
      confidential_comment
      is_public
      not_public_reason
      has_known_investor
      locations
      contracts
      datasources
      geojson
      versions {
        id
        deal {
          fully_updated
          status
          draft_status
          confidential
        }
        created_at
        created_by {
          id
          full_name
        }
        object_id
      }
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
        resolved
      }
      current_draft {
        id
      }
      status
      draft_status
    }
  }
`;
