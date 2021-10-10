<template>
  <div class="svg-container">
    <LoadingPulse v-if="$apollo.loading" />

    <svg id="svg"></svg>
  </div>
</template>

<script lang="ts">
  import gql from "graphql-tag";
  import LoadingPulse from "$components/Data/LoadingPulse.vue";
  import { GlobalInvolvementMap } from "./global_inv_map";
  import Vue from "vue";

  export default Vue.extend({
    name: "WebOfTransnationalDeals",
    components: { LoadingPulse },
    data() {
      return {
        global_map: null,
        global_map_of_investments: null,
      };
    },
    apollo: {
      global_map_of_investments: {
        query: gql`
          query ($filters: [Filter]) {
            global_map_of_investments(filters: $filters)
          }
        `,
        variables() {
          return {
            filters: this.filtered_filtersForGQL,
          };
        },
      },
    },
    watch: {
      global_map_of_investments(newV) {
        // let projection = "geoOrthographic";
        let projection = "geoNaturalEarth1";
        this.global_map.doTheThing(newV);
      },
    },
    mounted() {
      this.global_map = new GlobalInvolvementMap("#svg");
    },

    methods: {},
  });
</script>
<style lang="scss">
  .svg-container {
    height: 100%;
    max-height: 90vh;
    width: 100vw;
    overflow: hidden;
    background: #dff0fa;
    margin-top: 2rem;
    //padding: 4em 2em 2em 2em;
    svg {
      display: block;
      width: auto;
      height: auto;
      margin-left: auto;
      margin-right: auto;
    }
  }
  /**
 * from https://codepen.io/chrislaskey/pen/jqabBQ
 *
 **/

  .world-outline {
    fill: none;
    stroke: rgba(0, 0, 0, 0.1);
    stroke-width: 1px;
  }

  .back-country {
    fill: hsl(32, 57%, 90%);
    stroke: #fff;
    stroke-width: 0;
    stroke-linejoin: round;
  }

  .back-line {
    fill: none;
    stroke: #000;
    stroke-opacity: 0.05;
    stroke-width: 0.5px;
  }

  .country {
    //fill: hsl(32, 17%, 10%);
    fill: white;
    stroke-width: 0.3;
    stroke: black;
    stroke-linejoin: round;
    &.hover {
      fill: hsla(0, 0%, 62%, 0.5);
    }
    &.selected-country {
      fill: hsl(0, 0%, 32%);
    }
    &.target-country {
      fill: var(--color-lm-orange);
    }
    &.investor-country {
      fill: var(--color-lm-investor);
    }
  }

  .line {
    fill: none;
    stroke: #000;
    stroke-opacity: 0.08;
    stroke-width: 0.5px;
  }

  //#incoming-marker {
  //  fill: var(--color-lm-orange);
  //}
  //
  //#outgoing-marker {
  //  fill: var(--color-lm-investor);
  //}
  .target-country-line {
    fill: none;
    stroke: var(--color-lm-orange-light);
    stroke-width: 0.6;
    //marker-end: url(#outgoing-marker);
  }
  .investor-country-line {
    fill: none;
    stroke: var(--color-lm-investor-light);
    stroke-width: 0.6;
    //marker-start: url(#incoming-marker);
  }
  #incoming-marker {
    fill: var(--color-lm-investor);
  }

  #outgoing-marker {
    fill: var(--color-lm-orange);
  }
</style>
