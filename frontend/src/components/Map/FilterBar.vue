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
        <strong>{{ $t("Filter") }} ({{ deals.length }})</strong><br />
        <span style="font-size: 0.8em;">
          <a @click="$store.dispatch('resetFilters')">Set default filters</a> |
          <a @click="$store.dispatch('clearFilters')">Clear filters</a>
        </span>

        <FilterCollapse :title="$t('Region')">
          <b-form-group>
            <b-form-radio
              v-model="region_id"
              name="regionRadio"
              :value="reg.id"
              v-for="reg in regions"
              @change="country_id = null"
            >
              {{ reg.name }}
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>

        <FilterCollapse :title="$t('Country')">
          <multiselect
            v-model="country"
            :options="countries"
            label="name"
            placeholder="Country"
            @input="region_id = null"
          />
        </FilterCollapse>
        <FilterCollapse :title="$t('Deal size')">
          <div class="input-group">
            <input
              v-model="deal_size_min"
              type="number"
              class="form-control"
              placeholder="from"
              aria-label="from"
              :max="deal_size_max"
            />
            <div class="input-group-append">
              <span class="input-group-text">ha</span>
            </div>
          </div>
          <div class="input-group">
            <input
              type="number"
              v-model="deal_size_max"
              class="form-control"
              placeholder="to"
              aria-label="to"
              :min="deal_size_min"
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
              v-model="negotiation_status"
            />
            <label class="form-check-label" :for="nsval">
              {{ nsname }}
            </label>
          </div>
        </FilterCollapse>

        <FilterCollapse :title="$t('Investor')">
          <div>
            <multiselect
              v-model="investor"
              :options="investors"
              :multiple="false"
              :close-on-select="true"
              placeholder="Investor"
              track-by="id"
              label="name"
            />
          </div>
        </FilterCollapse>

        <FilterCollapse :title="$t('Year of initiation')">
          <form class="form-inline">
            <div class="input-group">
              <input
                type="number"
                v-model="initiation_year_min"
                class="form-control"
                placeholder="from"
                aria-label="from"
              />
            </div>
            <div class="input-group">
              <input
                type="number"
                v-model="initiation_year_max"
                class="form-control"
                placeholder="to"
                aria-label="to"
              />
            </div>
            <label>
              <input
                type="checkbox"
                :disabled="!initiation_year_min && !initiation_year_max"
                v-model="initiation_year_unknown"
              />
              Include unknown years
            </label>
          </form>
        </FilterCollapse>

        <FilterCollapse :title="$t('Implementation status')">
          <div
            v-for="(isname, isval) in choices.implementation_status"
            class="form-check"
          >
            <input
              class="form-check-input"
              type="checkbox"
              :value="isval"
              :id="isval"
              v-model="implementation_status"
            />
            <label class="form-check-label" :for="isval">
              {{ isname }}
            </label>
          </div>
        </FilterCollapse>

        <FilterCollapse :title="$t('Intention of Investment')">
          <multiselect
            v-model="intention_of_investment"
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

        <FilterCollapse :title="$t('Produce')">
          <multiselect
            v-model="produce"
            :options="produce_choices"
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
        <FilterCollapse :title="$t('Transnational')">
          <b-form-group>
            <b-form-radio
              v-model="transnational"
              name="transnationalRadio"
              value="True"
            >
              Transnational
            </b-form-radio>
            <b-form-radio
              v-model="transnational"
              name="transnationalRadio"
              value="False"
            >
              Domestic
            </b-form-radio>
            <b-form-radio
              v-model="transnational"
              name="transnationalRadio"
              :value="null"
            >
              Both
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>
      </div>
      <div class="bottom-pane">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import FilterCollapse from "./FilterCollapse";
  import gql from "graphql-tag";

  export default {
    name: "FilterBar",
    components: { FilterCollapse },
    props: ["deals"],
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
    data() {
      return {
        showFilterOverlay: true,
        investors: [],
        defaultFilters: true,
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
    computed: {
      region_id: {
        get() {
          return this.filters.region_id;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "region_id", value });
        },
      },
      country: {
        get() {
          return this.countries.find((c) => c.id === this.filters.country_id);
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "country_id", value: value.id });
        },
      },
      deal_size_min: {
        get() {
          return this.filters.deal_size_min;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "deal_size_min", value });
        },
      },
      deal_size_max: {
        get() {
          return this.filters.deal_size_max;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "deal_size_max", value });
        },
      },
      negotiation_status: {
        get() {
          return this.filters.negotiation_status;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "negotiation_status", value });
        },
      },
      investor: {
        get() {
          return this.filters.investor;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "investor", value });
        },
      },
      initiation_year_min: {
        get() {
          return this.filters.initiation_year_min;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "initiation_year_min", value });
        },
      },
      initiation_year_max: {
        get() {
          return this.filters.initiation_year_max;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "initiation_year_max", value });
        },
      },
      initiation_year_unknown: {
        get() {
          return this.filters.initiation_year_unknown;
        },
        set(value) {
          this.$store.dispatch("setFilter", {
            filter: "initiation_year_unknown",
            value,
          });
        },
      },
      implementation_status: {
        get() {
          return this.filters.implementation_status;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "implementation_status", value });
        },
      },
      intention_of_investment: {
        get() {
          return this.filters.intention_of_investment;
        },
        set(value) {
          this.$store.dispatch("setFilter", {
            filter: "intention_of_investment",
            value,
          });
        },
      },
      produce: {
        get() {
          return this.filters.produce;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "produce", value });
        },
      },
      transnational: {
        get() {
          return this.filters.transnational;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "transnational", value });
        },
      },
      ...mapState({
        filters: (state) => state.filters.filters,
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
      produce_choices() {
        if (!this.dealFormfields) return [];
        return [
          {
            type: this.$t("Crop"),
            options: Object.entries(
              this.dealFormfields.crops.choices
            ).map(([k, v]) => ({ name: v, id: `crop_${k}`, value: k })),
          },
          {
            type: this.$t("Livestock"),
            options: Object.entries(
              this.dealFormfields.animals.choices
            ).map(([k, v]) => ({ name: v, id: `animal_${k}`, value: k })),
          },
          {
            type: this.$t("Minerals"),
            options: Object.entries(
              this.dealFormfields.resources.choices
            ).map(([k, v]) => ({ name: v, id: `mineral_${k}`, value: k })),
          },
        ];
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
