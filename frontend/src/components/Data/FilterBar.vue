<template>
  <div class="filter-overlay" :class="{ collapsed: !showFilterBar }">
    <span class="wimpel" @click.prevent="showFilterBar = !showFilterBar">
      <svg viewBox="0 0 2 20" width="20px">
        <path d="M0,0 L2,2 L2,18 L0,20z"></path>
        <text x="0.3" y="11">
          {{ showFilterBar ? "&lsaquo;" : "&rsaquo;" }}
        </text>
      </svg>
    </span>
    <div class="overlay-content">
      <div class="main-pane">
        <h3>{{ $t("Filter") }}</h3>
        <span style="font-size: 0.8em;">
          <b-form-checkbox
            class="default-filter-switch"
            :class="{ active: isDefaultFilter }"
            name="check-button"
            switch
            v-model="isDefaultFilter"
            @change="updateDefaultFilter"
          >
            Default filter
          </b-form-checkbox>
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
              @change="country = null"
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
            @change="region_id = null"
            @select="region_id = null"
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
            <div class="custom-control custom-checkbox">
              <input
                class="form-check-input custom-control-input"
                type="checkbox"
                :value="nsval"
                :id="nsval"
                v-model="negotiation_status"
              />
              <label class="form-check-label custom-control-label" :for="nsval">
                {{ $t(nsname) }}
              </label>
            </div>
          </div>
        </FilterCollapse>

        <FilterCollapse
          :title="$t('Nature of deal')"
          :clearable="nature_of_deal.length > 0"
          @click="nature_of_deal = []"
        >
          <div v-for="(isname, isval) in choices.nature_of_deal" class="form-check">
            <div class="custom-control custom-checkbox">
              <input
                class="form-check-input custom-control-input"
                type="checkbox"
                :value="isval"
                :id="isval"
                v-model="nature_of_deal"
              />
              <label class="form-check-label custom-control-label" :for="isval">
                {{ $t(isname) }}
              </label>
            </div>
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
            <div class="custom-control custom-checkbox">
              <input
                type="checkbox"
                class="custom-control-input"
                :disabled="!initiation_year_min && !initiation_year_max"
                v-model="initiation_year_unknown"
                id="initiation_year_unknown"
              />
              <label class="custom-control-label" for="initiation_year_unknown">
                Include unknown years
              </label>
            </div>
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
            <div class="custom-control custom-checkbox">
              <input
                class="form-check-input custom-control-input"
                type="checkbox"
                :value="isval"
                :id="isval"
                v-model="implementation_status"
              />
              <label class="form-check-label custom-control-label" :for="isval">
                {{ $t(isname) }}
              </label>
            </div>
          </div>
        </FilterCollapse>

        <FilterCollapse
          :title="$t('Intention of investment')"
          :clearable="intention_of_investment.length > 0"
          @click="intention_of_investment = []"
        >
          <div v-for="(options, name) in choices.intention_of_investment">
            <strong>{{ $t(name) }}</strong>
            <div v-for="(isname, isval) in options" class="form-check">
              <div class="custom-control custom-checkbox">
                <input
                  class="form-check-input custom-control-input"
                  type="checkbox"
                  :value="isval"
                  :id="isval"
                  v-model="intention_of_investment"
                />
                <label class="form-check-label custom-control-label" :for="isval">
                  {{ $t(isname) }}
                </label>
              </div>
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
          </b-form-group>
        </FilterCollapse>
        <FilterCollapse
          :title="$t('Forest concession')"
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
          query Investors($limit: Int!, $subset: Subset) {
            investors(limit: $limit, subset: $subset) {
              id
              name
            }
          }
        `,
        update(data) {
          this.$store.commit("setInvestors", data.investors);
          return data.investors;
        },
        variables() {
          let user = this.$store.state.page.user;
          return {
            limit: 0,
            subset: user && user.is_authenticated ? "ACTIVE" : "PUBLIC",
          };
        },
      },
    },
    data() {
      return {
        year: new Date().getFullYear(),
        investors: [],
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
      showFilterBar: {
        get() {
          return this.$store.state.map.showFilterBar;
        },
        set(value) {
          this.$store.dispatch("showFilterBar", value);
        },
      },
      region_id: {
        get() {
          return this.filters.region_id;
        },
        set(value) {
          if (value !== this.filters.region_id) {
            this.$store.dispatch("setFilter", { filter: "region_id", value });
          }
        },
      },
      country: {
        get() {
          return this.countries.find((c) => c.id === this.filters.country_id);
        },
        set(value) {
          if ((value ? value.id : value) !== this.filters.country_id) {
            this.$store.dispatch("setFilter", {
              filter: "country_id",
              value: value ? value.id : value,
            });
          }
        },
      },
      deal_size_min: {
        get() {
          return this.filters.deal_size_min;
        },
        set(value) {
          if (value !== this.filters.deal_size_min) {
            this.$store.dispatch("setFilter", { filter: "deal_size_min", value });
          }
        },
      },
      deal_size_max: {
        get() {
          return this.filters.deal_size_max;
        },
        set(value) {
          if (value !== this.filters.deal_size_max) {
            this.$store.dispatch("setFilter", { filter: "deal_size_max", value });
          }
        },
      },
      negotiation_status: {
        get() {
          return this.filters.negotiation_status;
        },
        set(value) {
          if (value !== this.filters.negotiation_status) {
            this.$store.dispatch("setFilter", { filter: "negotiation_status", value });
          }
        },
      },
      nature_of_deal: {
        get() {
          return this.filters.nature_of_deal;
        },
        set(value) {
          if (value !== this.filters.nature_of_deal) {
            this.$store.dispatch("setFilter", { filter: "nature_of_deal", value });
          }
        },
      },
      investor: {
        get() {
          return this.filters.investor;
        },
        set(value) {
          if (value !== this.filters.investor) {
            this.$store.dispatch("setFilter", { filter: "investor", value });
          }
        },
      },
      initiation_year_min: {
        get() {
          return this.filters.initiation_year_min;
        },
        set(value) {
          if (value !== this.filters.initiation_year_min) {
            this.$store.dispatch("setFilter", { filter: "initiation_year_min", value });
          }
        },
      },
      initiation_year_max: {
        get() {
          return this.filters.initiation_year_max;
        },
        set(value) {
          if (value !== this.filters.initiation_year_max) {
            this.$store.dispatch("setFilter", { filter: "initiation_year_max", value });
          }
        },
      },
      initiation_year_unknown: {
        get() {
          return this.filters.initiation_year_unknown;
        },
        set(value) {
          if (value !== this.filters.initiation_year_unknown) {
            this.$store.dispatch("setFilter", {
              filter: "initiation_year_unknown",
              value,
            });
          }
        },
      },
      implementation_status: {
        get() {
          return this.filters.implementation_status;
        },
        set(value) {
          if (value !== this.filters.implementation_status) {
            this.$store.dispatch("setFilter", {
              filter: "implementation_status",
              value,
            });
          }
        },
      },
      intention_of_investment: {
        get() {
          return this.filters.intention_of_investment;
        },
        set(value) {
          if (value !== this.filters.intention_of_investment) {
            this.$store.dispatch("setFilter", {
              filter: "intention_of_investment",
              value,
            });
          }
        },
      },
      produce: {
        get() {
          return this.filters.produce;
        },
        set(value) {
          if (value !== this.filters.produce) {
            this.$store.dispatch("setFilter", { filter: "produce", value });
          }
        },
      },
      transnational: {
        get() {
          return this.filters.transnational;
        },
        set(value) {
          if (value !== this.filters.transnational) {
            this.$store.dispatch("setFilter", { filter: "transnational", value });
          }
        },
      },
      forest_concession: {
        get() {
          return this.filters.forest_concession;
        },
        set(value) {
          if (value !== this.filters.forest_concession) {
            this.$store.dispatch("setFilter", { filter: "forest_concession", value });
          }
        },
      },
      isDefaultFilter: {
        get() {
          return this.$store.state.filters.isDefaultFilter;
        },
        set(value) {
          // do nothing - only on user action: see updateDefaultFilter()
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
    methods: {
      updateDefaultFilter(checked) {
        if (checked) this.$store.dispatch("resetFilters");
        else this.$store.dispatch("clearFilters");
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
    //transition: width 0.5s, min-width 0.5s;
    width: 20%;
    min-width: 220px;
    max-width: 300px;
    font-size: 0.9rem;

    h3 {
      color: black;
      margin-top: 0.5em;
      margin-bottom: 0.2em;
    }

    .overlay-content {
      width: 100%;
      height: 100%;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 0.5rem;
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

    .default-filter-switch {
      &.active {
        color: $lm_orange;
      }

      label.custom-control-label {
        font-size: 0.9rem;

        &:hover {
          cursor: pointer;
        }

        &:before {
          font-size: 0.8rem;
          background-color: rgba(black, 0.1);
          border-width: 0;
          width: 1.9em;
          height: 0.65em;
          margin-top: 0.2em;
          margin-left: 0.15em;

          &:focus {
            outline: none;
          }
        }

        &:after {
          margin-top: -0.1em;
          background-color: white;
          box-shadow: 0px 1px 2px rgba(black, 0.3);
        }
      }
    }

    .custom-switch .custom-control-input:checked ~ .custom-control-label {
      &:before {
        background-color: rgba($lm_orange, 0.1);
      }

      &:after {
        background-color: $lm_orange;
        box-shadow: 0px 0px 0px 1px rgba($lm_orange, 0.7);
      }
    }

    .custom-control-input:focus ~ .custom-control-label {
      &:before {
        box-shadow: none;
      }
    }

    .form-check {
      padding: 0;
      .custom-control.custom-checkbox {
        min-height: 0;
        padding-left: 1.3rem;
        label.custom-control-label {
          &:hover {
            cursor: pointer;
          }
          line-height: 1.2;
          &:before,
          &:after {
            top: 1px;
            left: -1.3rem;
          }
        }
      }
      .custom-control-input:focus ~ .custom-control-label {
        &:before {
          border-color: #adb5bd;
        }
      }
      .custom-control-input:checked ~ .custom-control-label {
        &:before {
          background-color: rgba($lm_orange, 1);
          border-color: transparent;
        }
      }
      &:not(:first-child) {
        .custom-control.custom-checkbox {
          margin-top: 2px;
        }
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
