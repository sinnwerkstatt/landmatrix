import axios from "axios";

export const dealModule = {
  state: () => ({
    deals: [],
    deals_uptodate: false,
    current_deal: null,
  }),
  mutations: {
    setDeals(state, deals) {
      state.deals = deals;
      state.deals_uptodate = true;
    },
    updateDeals(state, payload) {
      let { deals, finished } = payload;
      state.deals = state.deals.concat(deals);
      state.deals_uptodate = finished;
    },
    setCurrentDeal(state, deal) {
      state.current_deal = deal;
    },
  },
  actions: {
    fetchDeals(context, options) {
      let { limit, after } = options;
      if (context.state.deals_uptodate) return;

      let query = `{
        deals(limit:${limit}, after: ${after || -1}){
          id
          deal_size
          target_country { id name }
          # top_investors { id name }
          intention_of_investment
          current_negotiation_status
          current_implementation_status
          locations { id point level_of_accuracy }
        }
      }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        let deals = response.data.data.deals;
        if (deals.length === limit) {
          context.commit("updateDeals", { deals, finished: false });
          let last_deal = deals.slice(-1)[0];
          context.dispatch("fetchDeals", { limit: limit, after: last_deal.id });
        } else {
          context.commit("updateDeals", { deals, finished: true });
        }
      });
    },
    setCurrentDeal(context, deal_id) {
      if (!deal_id) {
        context.commit("setCurrentDeal", {});
        return;
      }

      let query = `{
        deal(id:${deal_id}) {
          id
        # General Info
        ## Land area
        target_country { id }
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
        purchase_price_currency {id}
        purchase_price_type
        purchase_price_area
        purchase_price_comment
        ## Leasing fees
        annual_leasing_fee
        annual_leasing_fee_currency {id}
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
        operating_company {id}
        involved_actors {role value}
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
        crops_yield
        crops_export
        crops_comment
        animal
        animal_yield
        animal_export
        animal_comment
        resources
        resources_yield
        resources_export
        resources_comment
        contract_farming_crops
        contract_farming_crops_comment
        contract_farming_animals
        contract_farming_animals_comment
        has_domestic_use
        domestic_use
        has_export
        export_country1 {id}
        export_country1_ratio
        export_country2 {id}
        export_country2_ratio
        export_country3 {id}
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
        # locations { id point level_of_accuracy }
        geojson
        }
      }`;
      axios.post("/graphql/", { query: query }).then((response) => {
        context.commit("setCurrentDeal", response.data.data.deal);
      });
    },
  },
  getters: {},
};