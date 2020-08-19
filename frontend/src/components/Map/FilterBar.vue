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
        <strong>Filter</strong>
        <div>
          <div>
            <b-button block v-b-toggle.accordion-1>Region</b-button>
            <b-collapse id="accordion-1" accordion="my-accordion" role="tabpanel">
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
            </b-collapse>
          </div>

          <div>
            <b-button block v-b-toggle.accordion-2>Country</b-button>
            <b-collapse id="accordion-2" accordion="my-accordion" role="tabpanel">
              <b-form-group>
                <multiselect
                  v-model="selectedCountry"
                  :options="countries"
                  label="name"
                  placeholder="Country"
                />
              </b-form-group>
            </b-collapse>
          </div>

          <div>
            <div>Deal size</div>
          </div>
          <div>
            <div>Negotiation status</div>
          </div>
          <div>
            <div>Investor</div>
          </div>
          <div>
            <div>Year of initiation</div>
          </div>
          <div>
            <div>Implementation status</div>
          </div>
          <div>
            <div>Intention of Investment</div>
          </div>
          <div>
            <div>Produce</div>
          </div>
        </div>

        Deals: {{ deals.length }}
      </div>
      <div style="position: absolute; bottom: 0;">
        <h4>Map settings</h4>
        Displayed data
        <hr />
        Layers
        <hr />
      </div>
    </div>
  </div>
</template>

<script>
  import { mapState } from "vuex";

  export default {
    name: "FilterBar",
    props: ["deals"],
    data() {
      return {
        showFilterOverlay: true,
        selectedRegion: -1,
        selectedCountry: null,
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
      }),
    },
  };
</script>

<style lang="scss">
  .divs {
    font-size: 12px;
  }
  button.div {
    padding-top: 2px;
    padding-bottom: 3px;
    padding-left: 4px;
    padding-right: 5px;

    font-size: 14px;
  }
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
</style>
