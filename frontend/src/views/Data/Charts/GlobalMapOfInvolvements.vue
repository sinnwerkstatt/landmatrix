<template>
  <div class="svg-container">
    <svg id="svg"></svg>
  </div>
</template>

<script>
  import { doTheThing } from "$views/Data/Charts/global_inv_map";
  import gql from "graphql-tag";
  export default {
    name: "WebOfTransnationalDeals",
    data() {
      return {
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
        console.log(newV);
      },
    },
    mounted() {
      doTheThing("#svg", this.global_map_of_investments);
    },
    methods: {},
  };
</script>
<style lang="scss">
  .svg-container {
    max-height: 100%;
    width: 100%;
    padding: 4em 2em 2em 2em;
    svg {
      display: block;
      margin-left: auto;
      margin-right: auto;
    }

    //> svg {
    //  width: 100%;
    //  height: 100%;
    //}
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
    fill: hsl(32, 17%, 20%);
    stroke-width: 0;
    stroke-linejoin: round;
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
  .moneyline {
    fill: none;
    stroke: var(--color-lm-investor-light);
    stroke-width: 1px;
    //marker-start: url(#outgoing-marker);
  }
</style>
