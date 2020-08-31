<template>
  <div class="filter-overlay" :class="{ collapsed: !showFilterOverlay }">
    <div class="toggle-button">
      <a href="#" @click.prevent="showFilterOverlay = !showFilterOverlay">
        <i
          class="fas"
          :class="[showFilterOverlay ? 'fa-chevron-left' : 'fa-chevron-right']"
        ></i>
      </a>
    </div>
    <div class="overlay-content">
      <div class="main-pane">
        <strong>{{ $t("Filter") }} ({{ deals.length }})</strong>
        <div class="form-check">
          <label class="form-check-label">
            <input class="form-check-input" type="checkbox" v-model="defaultFilters" />
            {{ $t("Default filter") }}
          </label>
        </div>

        <FilterCollapse title="Region">
          <b-form-group>
            <b-form-radio
              v-model="selection.region"
              name="regionRadio"
              :value="reg.id"
              v-for="reg in regions"
              @change="selection.country = null"
            >
              {{ reg.name }}
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>

        <FilterCollapse title="Country">
          <multiselect
            v-model="selection.country"
            :options="countries"
            label="name"
            placeholder="Country"
            @input="selection.region = null"
          />
        </FilterCollapse>
        <FilterCollapse title="Deal size">
          <div class="input-group">
            <input
              v-model="selection.deal_size_min"
              type="number"
              class="form-control"
              placeholder="from"
              aria-label="from"
              :max="selection.deal_size_max"
            />
            <div class="input-group-append">
              <span class="input-group-text">ha</span>
            </div>
          </div>
          <div class="input-group">
            <input
              type="number"
              v-model="selection.deal_size_max"
              class="form-control"
              placeholder="to"
              aria-label="to"
              :min="selection.deal_size_min"
            />
            <div class="input-group-append">
              <span class="input-group-text">ha</span>
            </div>
          </div>
        </FilterCollapse>

        <FilterCollapse :title="$t('Negotiation status')">
          <div v-for="(nsname, nsval) in choices.negotiation_status" class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              :value="nsval"
              :id="nsval"
              v-model="selection.negotiation_status"
            />
            <label class="form-check-label" :for="nsval">
              {{ nsname }}
            </label>
          </div>
        </FilterCollapse>

        <FilterCollapse title="Investor">
          <div>
            <multiselect
              v-model="selection.investion"
              :options="investors"
              :multiple="false"
              :close-on-select="true"
              placeholder="Investor"
              track-by="id"
              label="name"
            />
          </div>
        </FilterCollapse>
        <FilterCollapse title="Year of initiation">
          <form class="form-inline">
            <div class="input-group">
              <input
                type="number"
                v-model="selection.initiation_year_min"
                class="form-control"
                placeholder="from"
                aria-label="from"
              />
            </div>
            <div class="input-group">
              <input
                type="number"
                v-model="selection.initiation_year_max"
                class="form-control"
                placeholder="to"
                aria-label="to"
              />
            </div>
            <label>
              <input
                type="checkbox"
                :disabled="
                  !selection.initiation_year_min && !selection.initiation_year_max
                "
                v-model="selection.initiation_year_unknown"
              />
              Include unknown years
            </label>
          </form>
        </FilterCollapse>
        <FilterCollapse title="Implementation status">
          <div
            v-for="(isname, isval) in choices.implementation_status"
            class="form-check"
          >
            <input
              class="form-check-input"
              type="checkbox"
              :value="isval"
              :id="isval"
              v-model="selection.implementation_status"
            />
            <label class="form-check-label" :for="isval">
              {{ isname }}
            </label>
          </div>
        </FilterCollapse>
        <FilterCollapse title="Intention of Investment">
          <multiselect
            v-model="selection.intention_of_investment"
            :options="intention_of_investment_choices"
            :multiple="true"
            :close-on-select="false"
            placeholder="Intention"
            :group-select="true"
            group-label="type"
            group-values="options"
            track-by="id"
            label="name"
          />
        </FilterCollapse>
        <FilterCollapse title="Produce">
          <multiselect
            v-model="selection.produce"
            :options="produces"
            :multiple="true"
            :close-on-select="false"
            placeholder="Produce"
            :group-select="true"
            group-label="type"
            group-values="options"
            track-by="id"
            label="name"
          />
        </FilterCollapse>
      </div>
      <div class="bottom-pane">
        <slot ></slot>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import FilterCollapse from "./FilterCollapse";
  import gql from "graphql-tag";
  import Cookies from "js-cookie";

  export default {
    name: "FilterBar",
    components: { FilterCollapse },
    props: ["deals"],
    data() {
      return {
        showFilterOverlay: true,
        investors: [],
        defaultFilters: true,
        selection: {
          region: null,
          country: null,
          deal_size_min: 200,
          deal_size_max: null,
          negotiation_status: ["CONCLUDED"],
          investor: null,
          initiation_year_min: 2000,
          initiation_year_max: null,
          initiation_year_unknown: true,
          implementation_status: [],
          intention_of_investment: [],
          produce: [],
        },
        choices: {
          negotiation_status: {
            CONCLUDED: this.$t("Concluded"),
            INTENDED: this.$t("Intended"),
            FAILED: this.$t("Failed"),
          },
          implementation_status: {
            PROJECT_NOT_STARTED: this.$t("Project not started"),
            STARTUP_PHASE: this.$t("Start-up phase"),
            IN_OPERATION: this.$t("In Operation"),
            PROJECT_ABANDONED: this.$t("Project abandoned"),
          },
        },
      };
    },
    apollo: {
      investors: {
        query: gql`
          query {
            investors(limit: 0) {
              id
              name
            }
          }
        `,
      },
    },
    watch: {
      defaultFilters(val, old) {
        if (val) {
          this.$store.dispatch("resetFilters");
        }
      },
      aggFilters(newfilt, oldfilt) {
        this.$store.dispatch("setFilters", newfilt);
      },
    },
    created() {
      let filters_cookie = Cookies.get("filters");
      if (!filters_cookie) {
        this.$store.dispatch("resetFilters");
        return;
      }
      for (let filt of JSON.parse(filters_cookie)) {
        switch (filt.field) {
          case "deal_size":
            if (filt.operation === "GE") this.selection.deal_size_min = filt.value;
            else this.selection.deal_size_max = filt.value;
            break;
          case "current_negotiation_status":
            break;
          default:
            break;
        }
      }
    },
    computed: {
      ...mapState({
        countries: (state) => state.page.countries,
        regions: (state) => {
          let global = {
            id: null,
            name: "Global",
          };
          return [global, ...state.page.regions];
        },
        dealFormfields: (state) => state.formfields.deal,
      }),
      intention_of_investment_choices() {
        if (!this.dealFormfields) return [];
        return Object.entries(this.dealFormfields.intention_of_investment.choices).map(
          ([k, v]) => {
            return {
              type: k,
              options: Object.entries(v).map(([ke, ve]) => ({
                name: ve,
                id: ke,
              })),
            };
          }
        );
      },
      produces() {
        if (!this.dealFormfields) return [];
        return [
          {
            type: "Crop",
            options: Object.entries(
              this.dealFormfields.crops.choices
            ).map(([k, v]) => ({ name: v, id: `crop_${k}`, value: k })),
          },
          {
            type: "Livestock",
            options: Object.entries(
              this.dealFormfields.animals.choices
            ).map(([k, v]) => ({ name: v, id: `animal_${k}`, value: k })),
          },
          {
            type: "Minerals",
            options: Object.entries(
              this.dealFormfields.resources.choices
            ).map(([k, v]) => ({ name: v, id: `mineral_${k}`, value: k })),
          },
        ];
      },
      aggFilters() {
        let filters = [];
        if (this.selection.region) {
          filters.push({
            field: "country.fk_region_id",
            value: this.selection.region.toString(),
          });
        }
        if (this.selectedCountry) {
          filters.push({
            field: "country_id",
            value: this.selectedCountry.id.toString(),
          });
        }
        if (this.selection.deal_size_min) {
          filters.push({
            field: "deal_size",
            operation: "GE",
            value: this.selection.deal_size_min.toString(),
          });
        }
        if (this.selection.deal_size_max) {
          filters.push({
            field: "deal_size",
            operation: "LE",
            value: this.selection.deal_size_max.toString(),
          });
        }
        if (this.selection.negotiation_status.length > 0) {
          let negstat = [];
          if (this.selection.negotiation_status.includes("CONCLUDED"))
            negstat.push("ORAL_AGREEMENT", "CONTRACT_SIGNED");
          if (this.selection.negotiation_status.includes("INTENDED"))
            negstat.push(
              "EXPRESSION_OF_INTEREST",
              "UNDER_NEGOTIATION",
              "MEMORANDUM_OF_UNDERSTANDING"
            );
          if (this.selection.negotiation_status.includes("FAILED"))
            negstat.push("NEGOTIATIONS_FAILED", "CONTRACT_CANCELED");
          filters.push({
            field: "current_negotiation_status",
            operation: "IN",
            value: negstat,
          });
        }
        if (this.selection.implementation_status.length > 0) {
          filters.push({
            field: "current_implementation_status",
            operation: "IN",
            value: this.selection.implementation_status,
          });
        }

        if (this.selection.investion) {
          filters.push({
            field: "operating_company",
            value: this.selection.investion.id.toString(),
          });
        }
        if (!!this.selection.initiation_year_min) {
          filters.push({
            field: "initiation_year",
            operation: "GE",
            value: this.selection.initiation_year_min.toString(),
            allow_null: this.selection.initiation_year_unknown,
          });
        }
        if (!!this.selection.initiation_year_max) {
          filters.push({
            field: "initiation_year",
            operation: "LE",
            value: this.selection.initiation_year_max.toString(),
            allow_null: this.selection.initiation_year_unknown,
          });
        }
        if (this.selection.intention_of_investment.length > 0) {
          // exclude logic
          // TODO: use the INTENTION_CHOICES from deal.py here too?
          let invlist = [
            "BIOFUELS",
            "FOOD_CROPS",
            "FODDER",
            "LIVESTOCK",
            "NON_FOOD_AGRICULTURE",
            "AGRICULTURE_UNSPECIFIED",
            "TIMBER_PLANTATION",
            "FOREST_LOGGING",
            "CARBON",
            "FORESTRY_UNSPECIFIED",
            "MINING",
            "OIL_GAS_EXTRACTION",
            "TOURISM",
            "INDUSTRY",
            "CONVERSATION",
            "LAND_SPECULATION",
            "RENEWABLE_ENERGY",
            "OTHER",
          ];
          let flatflist = this.selection.intention_of_investment.map((x) => x.id);
          let xlist = invlist.filter((i) => {
            return !flatflist.includes(i);
          });

          filters.push({
            field: "current_intention_of_investment",
            operation: "OVERLAP",
            value: xlist,
            exclusion: true,
          });
        }

        // if (this.selection.produce && this.selection.produce.length > 0) {
        //   let crops = [];
        //   let animals = [];
        //   let minerals = [];
        //   this.selection.produce.map(prod => {
        //     if(prod.startsWith('crop_')) crops.push(prod.replace('crop_',''));
        //   });
        //   if(crops.length>0) {
        //     filters.push({
        //     field: "current_implementation_status",
        //     operation: "IN",
        //     value: this.selection.implementation_status,
        //   })
        //   }
        //   console.log(this.selection.produce);
        // }

        return filters;
      },
    },
  };
</script>

<style lang="scss">
  @import "../../scss/colors";

  .filter-overlay {
    position: absolute;
    background-color: rgba(255, 255, 255, 0.95);
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 10;
    display: flex;
    .toggle-button {
      position: absolute;
      right: 10px;
    }
    .overlay-content {
      width: 20vw;
      max-width: 230px;
      height: 100%;
      overflow-y: auto;
      padding: 0.5em;
      display: flex;
      flex-direction: column;
      .main-pane {
        align-self: flex-start;
      }
      .bottom-pane {
        align-self: flex-end;
        margin-top: auto;
        padding-top: 40px;
        width: 100%;
      }
    }
    &.collapsed {
      width: 25px;
      .toggle-button {
        position: static;
      }
      .overlay-content {
        display: none;
      }
    }
  }
  ul.layer-list {
    padding-left: 5px;
    list-style: none;
    div {
      color: $primary;
    }
    a {
      cursor: pointer;
    }
  }
</style>
