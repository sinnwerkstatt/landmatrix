import axios from "axios";

export const dealModule = {
  state: () => ({
    deals: [],
    deals_uptodate: false,
    current_deal: null,
    deal_fields: null,
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
    setDealFields(state, fields) {
      state.deal_fields = fields;
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
          country { id name }
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
    setCurrentDeal(context, { deal_id, deal_version }) {
      if (!deal_id) {
        context.commit("setCurrentDeal", {});
        return;
      }
      let filter = `id:${deal_id}`;
      let version = "";
      if (deal_version) {
        filter = `id:${deal_id},version:${deal_version}`;
        version = `(version:${deal_version})`;
      }
      // let filter = deal_version
      //   ? `id:${deal_id},version:${deal_version}`
      //   : `id:${deal_id}`;
      // let version = deal_version?`(version:${deal_version})`:'';
      let query = `{
        deal(${filter}) {
        id
        # General Info
        ## Land area
        country { id name }
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
        purchase_price_currency {id name}
        purchase_price_type
        purchase_price_area
        purchase_price_comment
        ## Leasing fees
        annual_leasing_fee
        annual_leasing_fee_currency {id name}
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
        operating_company {id name}
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
        export_country1 {id name}
        export_country1_ratio
        export_country2 {id name}
        export_country2_ratio
        export_country3 {id name}
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
        locations${version} {
          id
          name
          description
          point
          facility_name
          level_of_accuracy
          comment
        }
        contracts${version} {
          id
          number
          date
          expiration_date
          agreement_duration
          comment
        }
        datasources${version} {
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
          deal { fully_updated status draft_status }
          revision {
            id
            date_created
            user { id full_name }
            comment
          }
        }
        }
      }`;

      return new Promise(function (resolve, reject) {
        axios
          .post("/graphql/", {
            query,
          })
          .then((response) => {
            let resdata = response.data.data;
            if (resdata) {
              context.commit("setCurrentDeal", resdata.deal);
              resolve(resdata.deal);

              let title = `Deal #${deal_id}`;
              context.commit("setTitle", title);
              context.commit("setBreadcrumbs", [
                {
                  link: {
                    name: "wagtail",
                  },
                  name: "Home",
                },
                {
                  link: {
                    name: "deal_list",
                  },
                  name: "Data",
                },
                { name: title },
              ]);
            }
            reject(resdata);
          });
      });
    },
  },
  getters: {},
};
