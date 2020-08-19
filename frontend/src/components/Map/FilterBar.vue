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
        <FilterCollapse title="Region">
          <b-form-group>
            <b-form-radio
              v-model="selectedRegion"
              name="regionRadio"
              :value="reg.id"
              v-for="reg in regions"
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
          <div
            v-for="negstat in ['Concluded', 'Intended', 'Failed']"
            class="form-check"
          >
            <input
              class="form-check-input"
              type="checkbox"
              :value="negstat"
              :id="negstat"
              :checked="!negotiationStatus.indexOf(negstat)"
            />
            <label class="form-check-label" :for="negstat">
              {{ negstat }}
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
            v-for="negstat in [
              'Project not started',
              'Start-up phase',
              'In Operation',
              'Project abandoned',
            ]"
            class="form-check"
          >
            <input
              class="form-check-input"
              type="checkbox"
              :value="negstat"
              :id="negstat"
            />
            <label class="form-check-label" :for="negstat">
              {{ negstat }}
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
    props: ["deals", "bigmap"],
    data() {
      return {
        showFilterOverlay: true,
        selectedRegion: -1,
        selectedCountry: null,
        dealSizeMin: 200,
        dealSizeMax: null,
        negotiationStatus: ["Concluded"],
      };
    },
    computed: {
      ...mapState({
        countries: (state) => state.page.countries,
        regions: (state) => {
          let world = {
            id: -1,
            name: "World",
            slug: "world",
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
