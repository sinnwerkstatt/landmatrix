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
    query Investor($id: Int!, $version: Int, $depth: Int, $includeDeals: Boolean!) {
      investor(id: $id, version: $version) {
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
        involvements(depth: $depth)
        versions {
          id
          investor {
            status
            draft_status
          }
          revision {
            id
            date_created
            user {
              id
              full_name
            }
            comment
          }
          object_id
        }
      }
    }
  `,
  variables() {
    return {
      id: +this.investor_id,
      version: +this.investor_version,
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

export const deal_gql_query = gql`
  query Deal($id: Int!, $version: Int, $subset: Subset) {
    deal(id: $id, version: $version, subset: $subset) {
      id
      # General Info
      ## Land area
      country {
        id
        name
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
      on_the_lease
      on_the_lease_area
      on_the_lease_farmers
      on_the_lease_households
      off_the_lease
      off_the_lease_area
      off_the_lease_farmers
      off_the_lease_households
      contract_farming_comment
      # Employment
      total_jobs_created
      total_jobs_planned
      total_jobs_planned_employees
      total_jobs_planned_daily_workers
      total_jobs_current
      total_jobs_current_employees
      total_jobs_current_daily_workers
      total_jobs_created_comment
      foreign_jobs_created
      foreign_jobs_planned
      foreign_jobs_planned_employees
      foreign_jobs_planned_daily_workers
      foreign_jobs_current
      foreign_jobs_current_employees
      foreign_jobs_current_daily_workers
      foreign_jobs_created_comment
      domestic_jobs_created
      domestic_jobs_planned
      domestic_jobs_planned_employees
      domestic_jobs_planned_daily_workers
      domestic_jobs_current
      domestic_jobs_current_employees
      domestic_jobs_current_daily_workers
      domestic_jobs_created_comment
      # Investor info
      operating_company {
        id
        name
      }
      involved_actors {
        role
        value
      }
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
      resources
      resources_comment
      contract_farming_crops
      contract_farming_crops_comment
      contract_farming_animals
      contract_farming_animals_comment
      has_domestic_use
      domestic_use
      has_export
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
      # Guidelines & Principles
      vggt_applied
      vggt_applied_comment
      prai_applied
      prai_applied_comment
      # Overall comment
      overall_comment
      # Meta
      created_at
      modified_at
      fully_updated
      fully_updated_at
      confidential
      confidential_reason
      confidential_comment
      locations {
        id
        name
        description
        point
        facility_name
        level_of_accuracy
        comment
      }
      contracts {
        id
        number
        date
        expiration_date
        agreement_duration
        comment
      }
      datasources {
        id
        type
        url
        file
        file_not_public
        publication_title
        date
        name
        company
        email
        phone
        includes_in_country_verified_information
        open_land_contracts_id
        comment
      }
      geojson
      versions {
        id
        deal {
          fully_updated
          status
          draft_status
        }
        revision {
          id
          date_created
          user {
            id
            full_name
          }
          comment
        }
        object_id
      }
      comments {
        id
        userinfo
        comment
        submit_date
      }
      status
      draft_status
    }
  }
`;
