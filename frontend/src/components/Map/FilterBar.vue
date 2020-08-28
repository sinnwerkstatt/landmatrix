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
      <div>
        <strong>Filter ({{ deals.length }})</strong>
        <div class="form-check">
          <label class="form-check-label">
            <input class="form-check-input" type="checkbox" v-model="defaultFilters" />
            {{ $t("Default filter") }}
          </label>
        </div>

        <FilterCollapse title="Region">
          <b-form-group>
            <b-form-radio
              v-model="selectedRegion"
              name="regionRadio"
              :value="reg.id"
              v-for="reg in regions"
              @change="selectedCountry = null"
            >
              {{ reg.name }}
            </b-form-radio>
          </b-form-group>
        </FilterCollapse>

        <FilterCollapse title="Country">
          <b-form-group>
            <multiselect
              v-model="selectedCountry"
              :options="countries"
              label="name"
              placeholder="Country"
              @input="selectedRegion = null"
            />
          </b-form-group>
        </FilterCollapse>
        <FilterCollapse title="Deal size">
          <div class="input-group">
            <input
              v-model="dealSizeMin"
              type="text"
              class="form-control"
              placeholder="from"
              aria-label="from"
            />
            <div class="input-group-append">
              <span class="input-group-text">ha</span>
            </div>
          </div>
          <div class="input-group">
            <input
              type="text"
              v-model="dealSizeMax"
              class="form-control"
              placeholder="to"
              aria-label="to"
            />
            <div class="input-group-append">
              <span class="input-group-text">ha</span>
            </div>
          </div>
        </FilterCollapse>

        <FilterCollapse title="Negotiation status">
          <div v-for="(nsname, nsval) in negotiationStatusOptions" class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              :value="nsval"
              :id="nsval"
              v-model="negotiationStatus"
            />
            <label class="form-check-label" :for="nsval">
              {{ nsname }}
            </label>
          </div>
        </FilterCollapse>

        <FilterCollapse title="Investor">
          <div>Investor</div>
        </FilterCollapse>
        <FilterCollapse title="Year of initiation">
          <div></div>
        </FilterCollapse>
        <FilterCollapse title="Implementation status">
          <div
            v-for="(isname, isval) in implementationStatusOptions"
            class="form-check"
          >
            <input
              class="form-check-input"
              type="checkbox"
              :value="isval"
              :id="isval"
              v-model="implementationStatus"
            />
            <label class="form-check-label" :for="isval">
              {{ isname }}
            </label>
          </div>
        </FilterCollapse>
        <FilterCollapse title="Intention of Investment">
          <div></div>
        </FilterCollapse>
        <FilterCollapse title="Produce">
          <div></div>
        </FilterCollapse>
      </div>
      <div style="position: absolute; bottom: 0;">
        <h4>Map settings</h4>
        <FilterCollapse title="Base layer">
          <ul class="layer-list">
            <li v-for="layer in tileLayers">
              <div v-if="layer.name === visibleLayer">{{ layer.name }}</div>
              <a v-else @click.prevent="$store.dispatch('setCurrentLayer', layer.name)">
                {{ layer.name }}
              </a>
            </li>
          </ul>
        </FilterCollapse>
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";
  import FilterCollapse from "./FilterCollapse";

  export default {
    name: "FilterBar",
    components: { FilterCollapse },
    props: ["deals"],
    data() {
      return {
        showFilterOverlay: true,
        defaultFilters: true,
        selectedRegion: null,
        selectedCountry: null,
        dealSizeMin: 200,
        dealSizeMax: null,
        negotiationStatus: ["CONCLUDED"],
        negotiationStatusOptions: {
          CONCLUDED: "Concluded",
          INTENDED: "Intended",
          FAILED: "Failed",
        },
        implementationStatus: [],
        implementationStatusOptions: {
          PROJECT_NOT_STARTED: "Project not started",
          STARTUP_PHASE: "Start-up phase",
          IN_OPERATION: "In Operation",
          PROJECT_ABANDONED: "Project abandoned",
        },
      };
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
    computed: {
      aggFilters() {
        let filters = [];
        if (this.selectedRegion) {
          filters.push({
            field: "country.fk_region_id",
            value: this.selectedRegion.toString(),
          });
        }
        if (this.selectedCountry) {
          filters.push({
            field: "country_id",
            value: this.selectedCountry.id.toString(),
          });
        }
        if (this.dealSizeMin) {
          filters.push({
            field: "deal_size",
            operation: "GE",
            value: this.dealSizeMin.toString(),
          });
        }
        if (this.dealSizeMax) {
          filters.push({
            field: "deal_size",
            operation: "LE",
            value: this.dealSizeMax.toString(),
          });
        }
        if (this.negotiationStatus.length > 0) {
          let negstat = [];
          if (this.negotiationStatus.includes("CONCLUDED"))
            negstat.push("ORAL_AGREEMENT", "CONTRACT_SIGNED");
          if (this.negotiationStatus.includes("INTENDED"))
            negstat.push(
              "EXPRESSION_OF_INTEREST",
              "UNDER_NEGOTIATION",
              "MEMORANDUM_OF_UNDERSTANDING"
            );
          if (this.negotiationStatus.includes("FAILED"))
            negstat.push("NEGOTIATIONS_FAILED", "CONTRACT_CANCELED");
          filters.push({
            field: "current_negotiation_status",
            operation: "IN",
            value: negstat,
          });
          if (this.implementationStatus.length > 0) {
            filters.push({
            field: "current_implementation_status",
            operation: "IN",
            value: this.implementationStatus,
          });
          }
        }
        return filters;
      },
      ...mapState({
        countries: (state) => state.page.countries,
        regions: (state) => {
          let world = {
            id: null,
            name: "Global",
            slug: "global",
          };
          return [world, ...state.page.regions];
        },
        tileLayers: (state) => state.map.layers,
        visibleLayer: (state) => state.map.visibleLayer,
      }),
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
