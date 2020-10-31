<template>
  <div class="filter-overlay" :class="{ collapsed: !showFilterOverlay }">
    <span class="wimpel" @click.prevent="showFilterOverlay = !showFilterOverlay">
      <svg viewBox="0 0 2 20" width="20px">
        <path d="M0,0 L2,2 L2,18 L0,20z"></path>
        <text x="0.3" y="11">
          {{ showFilterOverlay ? "&lsaquo;" : "&rsaquo;" }}
        </text>
      </svg>
    </span>
    <div class="overlay-content">
      <div class="main-pane">
        <strong>{{ $t("Filter") }}</strong
        ><br />
        <span style="font-size: 0.8em;">
          <a href="#" @click="$store.dispatch('resetFilters')">Set default filters</a> |
          <a href="#" @click="$store.dispatch('clearFilters')">Clear filters</a>
        </span>

        <FilterCollapse
          :title="$t('Region')"
          :clearable="region_id"
          @click="region_id = null"
        >
          <b-form-group>
            <b-form-radio
              v-model="region_id"
              name="regionRadio"
              :value="reg.id"
              v-for="reg in regions"
              @input="country = null"
            >
              {{ $t(reg.name) }}
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>

        <FilterCollapse
          :title="$t('Country')"
          :clearable="country"
          @click="country = null"
        >
          <multiselect
            v-model="country"
            :options="countries_with_deals"
            label="name"
            placeholder="Country"
            @input="region_id = null"
          />
        </FilterCollapse>
        <FilterCollapse
          :title="$t('Deal size')"
          :clearable="deal_size_min || deal_size_max"
          @click="deal_size_min = deal_size_max = null"
        >
          <div class="input-group">
            <input
              v-model="deal_size_min"
              type="number"
              class="form-control"
              :placeholder="$t('from')"
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
              :placeholder="$t('to')"
              aria-label="to"
              :min="deal_size_min"
            />
            <div class="input-group-append">
              <span class="input-group-text">ha</span>
            </div>
          </div>
        </FilterCollapse>

        <FilterCollapse
          :title="$t('Negotiation status')"
          :clearable="negotiation_status.length > 0"
          @click="negotiation_status = []"
        >
          <div v-for="(nsname, nsval) in choices.negotiation_status" class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              :value="nsval"
              :id="nsval"
              v-model="negotiation_status"
            />
            <label class="form-check-label" :for="nsval">
              {{ $t(nsname) }}
            </label>
          </div>
        </FilterCollapse>

        <FilterCollapse
          :title="$t('Nature of Deal')"
          :clearable="nature_of_deal.length > 0"
          @click="nature_of_deal = []"
        >
          <div v-for="(isname, isval) in choices.nature_of_deal" class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              :value="isval"
              :id="isval"
              v-model="nature_of_deal"
            />
            <label class="form-check-label" :for="isval">
              {{ $t(isname) }}
            </label>
          </div>
        </FilterCollapse>

        <FilterCollapse
          :title="$t('Investor')"
          :clearable="investor"
          @click="investor = null"
        >
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

        <FilterCollapse
          :title="$t('Year of initiation')"
          :clearable="initiation_year_min || initiation_year_max"
          @click="initiation_year_min = initiation_year_max = null"
        >
          <form class="form-inline">
            <div class="input-group">
              <input
                type="number"
                v-model="initiation_year_min"
                class="form-control"
                placeholder="from"
                aria-label="from"
                min="1970"
                :max="year"
              />
            </div>
            <div class="input-group">
              <input
                type="number"
                v-model="initiation_year_max"
                class="form-control"
                placeholder="to"
                aria-label="to"
                min="1970"
                :max="year"
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

        <FilterCollapse
          :title="$t('Implementation status')"
          :clearable="implementation_status.length > 0"
          @click="implementation_status = []"
        >
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
              {{ $t(isname) }}
            </label>
          </div>
        </FilterCollapse>

        <FilterCollapse
          :title="$t('Intention of Investment')"
          :clearable="intention_of_investment.length > 0"
          @click="intention_of_investment = []"
        >
          <div v-for="(options, name) in choices.intention_of_investment">
            <strong>{{ $t(name) }}</strong>
            <div v-for="(isname, isval) in options" class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                :value="isval"
                :id="isval"
                v-model="intention_of_investment"
              />
              <label class="form-check-label" :for="isval">
                {{ $t(isname) }}
              </label>
            </div>
          </div>
        </FilterCollapse>

        <FilterCollapse
          :title="$t('Produce')"
          :clearable="produce.length > 0"
          @click="produce = []"
        >
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
        <FilterCollapse
          :title="$t('Transnational')"
          :clearable="transnational !== null"
          @click="transnational = null"
        >
          <b-form-group>
            <b-form-radio
              v-model="transnational"
              name="transnationalRadio"
              :value="true"
            >
              Transnational
            </b-form-radio>
            <b-form-radio
              v-model="transnational"
              name="transnationalRadio"
              :value="false"
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
        <FilterCollapse
          :title="$t('Forest Concession')"
          :clearable="forest_concession !== null"
          @click="forest_concession = null"
        >
          <b-form-group>
            <b-form-radio
              v-model="forest_concession"
              name="forest_concessionRadio"
              :value="true"
            >
              {{ $t("Included") }}
            </b-form-radio>
            <b-form-radio
              v-model="forest_concession"
              name="forest_concessionRadio"
              :value="false"
            >
              {{ $t("Excluded") }}
            </b-form-radio>
            <b-form-radio
              v-model="forest_concession"
              name="forest_concessionRadio"
              :value="null"
            >
              {{ $t("Both") }}
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
  import {
    implementation_status_choices,
    intention_of_investment_choices,
    nature_of_deal_choices,
  } from "/choices";

  export default {
    name: "FilterBar",
    components: { FilterCollapse },
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
        year: new Date().getFullYear(),
        investors: [],
        defaultFilters: true,
        choices: {
          negotiation_status: {
            CONCLUDED: "Concluded",
            INTENDED: "Intended",
            FAILED: "Failed",
          },
          implementation_status: implementation_status_choices,
          nature_of_deal: nature_of_deal_choices,
          intention_of_investment: intention_of_investment_choices,
        },
      };
    },
    computed: {
      showFilterOverlay: {
        get() {
          return this.$store.state.map.showFilterOverlay;
        },
        set(value) {
          this.$store.dispatch("showFilterOverlay", value);
        },
      },
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
          this.$store.dispatch("setFilter", {
            filter: "country_id",
            value: value ? value.id : value,
          });
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
      nature_of_deal: {
        get() {
          return this.filters.nature_of_deal;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "nature_of_deal", value });
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
      forest_concession: {
        get() {
          return this.filters.forest_concession;
        },
        set(value) {
          this.$store.dispatch("setFilter", { filter: "forest_concession", value });
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
      countries_with_deals() {
        return this.countries.filter((c) => {
          return c.deals.length > 0;
        });
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
    filter: drop-shadow(3px -3px 3px rgba(0, 0, 0, 0.3));
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 110;
    display: flex;
    transition: width 0.5s, min-width 0.5s;
    width: 20%;
    min-width: 220px;

    .overlay-content {
      width: 100%;
      height: 100%;
      overflow-y: auto;
      padding: 0.5em;
      display: flex;
      flex-direction: column;

      .main-pane {
        width: 100%;
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
      width: 0;
      min-width: 0;

      .toggle-button {
        position: static;
      }

      .overlay-content {
        display: none;
      }
    }
  }

  .wimpel {
    position: absolute;
    top: calc(50% - 100px);
    cursor: pointer;
    right: -20px;
    svg {
      opacity: 0.8;
      filter: drop-shadow(1px -1px 1px rgba(0, 0, 0, 0.3));
      color: black;
      path {
        fill: $primary;
      }
      text {
        font-size: 4px;
        fill: white;
      }
    }
  }
</style>
