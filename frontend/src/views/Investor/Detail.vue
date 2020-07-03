<template>
  <div class="container" v-if="investor">
    <h2>General Info</h2>
    <dl class="row">
      <dt class="col-3">Name</dt>
      <dd class="col-9">{{ investor.name }}</dd>
    </dl>
    <dl class="row">
      <dt class="col-3">Country of registration/origin</dt>
      <dd class="col-9">{{ investor.country.name }}</dd>
    </dl>
    <dl class="row">
      <dt class="col-3">Classification</dt>
      <dd class="col-9">{{ investor.classification }}</dd>
    </dl>
    <dl class="row">
      <dt class="col-3">Comment</dt>
      <dd class="col-9">{{ investor.comment }}</dd>
    </dl>

    <b-tabs content-class="mt-3">
      <b-tab :title="`Involvements (${involvements.length})`">
        <table class="table">
          <thead>
            <tr>
              <th>Investor ID</th>
              <th>Name</th>
              <th>Country</th>
              <th>Classification</th>
              <th>Relationship</th>
              <th>Ownership share</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="involvement in involvements">
              <td>
                <router-link
                  :to="{
                    name: 'investor_detail',
                    params: { investor_id: involvement.investor.id },
                  }"
                >
                  #{{ involvement.investor.id }}
                </router-link>
              </td>
              <td>{{ involvement.investor.name }}</td>
              <td>{{ involvement.investor.country.name }}</td>
              <td>{{ involvement.investor.classification }}</td>
              <td>{{ detect_role(involvement) }}</td>
              <td>{{ involvement.percentage }}</td>
            </tr>
          </tbody>
        </table>
      </b-tab>
      <b-tab
        :title="`Deals (Involvements as Operating company) (${investor.deals.length})`"
      >
        <table class="table">
          <thead>
            <tr>
              <th>Deal ID</th>
              <th>Country</th>
              <th>Classification</th>
              <th>Relationship</th>
              <th>Ownership share</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="deal in investor.deals">
              <td>
                <router-link
                  :to="{
                    name: 'deal_detail',
                    params: { deal_id: deal.id },
                  }"
                >
                  #{{ deal.id }}
                </router-link>
              </td>
              <td>{{ deal.country.name }}</td>
              <td>{{ deal }}</td>
            </tr>
          </tbody>
        </table>
      </b-tab>
    </b-tabs>

    <div id="investor-network"></div>
    <div class="row">
      <div id="investor-level" class="col-sm-6">
        <h5>Level of parent investors</h5>
        <div class="slider-container col-sm-8">
          <input
            type="range"
            min="1"
            max="10"
            value="1"
            class="slider"
            id="depth"
            autocomplete="off"
          />
        </div>
        <div class="col-sm-8">
          <input
            type="checkbox"
            class="show_deals"
            id="show_deals"
            checked="checked"
            autocomplete="off"
          />
          <label for="show_deals">{% trans "Show deals" %}</label>
        </div>
      </div>
      <div id="investor-legend" class="col-sm-6">
        <h5>{% trans "Legend" %}</h5>
        <ul class="list-unstyled">
          <li>
            <span class="legend-icon deal"></span> {% trans "Is operating company of" %}
          </li>
          <li>
            <span class="legend-icon parent"></span> {% trans "Is parent company of" %}
          </li>
          <li>
            <span class="legend-icon tertiary"></span> {% trans "Is tertiary
            investor/lender of" %}
          </li>
          <li>
            <span class="legend-icon has-children"></span> {% trans "Left-click to
            reveal related parent companies and tertiary investors/lenders." %}
          </li>
          <li>
            <span class="legend-icon investor"></span> {% trans "Right-click on
            investors to get more information." %}
          </li>
          <li>
            <span class="legend-icon none"></span> {% trans "Left-click to hide related
            parent companies and tertiary investors/lenders." %}
          </li>
          <li>
            <span class="legend-icon none"></span> {% trans "Double-click to zoom in."
            %}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
  .logo {
    width: 300px;
    text-align: center;
  }
</style>
<script>
  import store from "@/store";
  import { loadInvestorNetwork, mapValues } from "./investor-network";

  export default {
    props: ["investor_id"],
    data() {
      return {};
    },
    computed: {
      investor() {
        return this.$store.state.investor.current_investor;
      },
      involvements() {
        return this.investor.involvements;
      },
    },
    methods: {
      detect_role(investor) {
        if (investor.role === "STAKEHOLDER") {
          if (investor.involvement_type === "INVESTOR") return "Parent company";
          if (investor.involvement_type === "VENTURE")
            return "Involved in as Parent Company";
        }
        if (investor.role === "INVESTOR") {
          if (investor.involvement_type === "INVESTOR")
            return "Tertiary investor/lender";
          if (investor.involvement_type === "VENTURE")
            return "Involved in as Tertiary investor/lender";
        }
      },
    },
    mounted() {
      let compat_investors = mapValues(this.investor);
      loadInvestorNetwork(compat_investors, "#investor-network");
    },
    watch: {
      investor(newVal) {
        let compat_investors = mapValues(newVal);
        // loadInvestorNetwork(compat_investors, "#investor-network");
      },
    },
    beforeRouteEnter(to, from, next) {
      store.dispatch("setCurrentInvestor", to.params.investor_id);
      next();
    },
    beforeRouteUpdate(to, from, next) {
      store.dispatch("setCurrentInvestor", to.params.investor_id);
      next();
    },
  };
</script>

<style lang="scss">
  div#investor-network {
    border: 2px solid #ddd;
    display: block;
    width: 900px;
    height: 460px;
    cursor: all-scroll;
    overflow: hidden;

    .node {
      text-align: center;
      cursor: pointer;
    }

    .node.hover-other circle {
      fill: #f2fafa; /* .2 of primary color */
      stroke: #dcf0f0; /* .2 of primary color */
    }

    .node circle,
    .node.hover circle {
      fill: #bee7e7;
      stroke: #44b7b6;
      stroke-width: 2;
      transition: all 0.2s ease-in-out;
    }

    .node.is-root circle,
    .node.is-root.hover circle {
      fill: #44b7b6;
      stroke: #44b7b6;
    }

    .node.deal.hover-other circle {
      fill: #fff9f2; /* .2 of primary color */
      stroke: #ffe9d7; /* .2 of primary color */
    }

    .node.deal circle,
    .node.deal.hover circle {
      fill: #fcdfbf;
      stroke: #fc941f;
    }

    .node text {
      font-family: "Open Sans Condensed", sans-serif;
      font-size: 12px;
      font-weight: bold;
      transition: all 0.2s ease-in-out;
      text-anchor: middle;
      fill: #333;
      letter-spacing: 0.03em;
    }

    .node text.subtitle {
      font-weight: normal;
    }

    .link,
    .crosslink {
      fill: none;
      stroke: #333;
      stroke-width: 2;
    }

    .link {
      fill: none;
      stroke: #333;
    }

    .link.parent,
    .crosslink.parent {
      stroke: #72b0fd;
    }

    .link.tertiary,
    .crosslink.tertiary {
      stroke: #f78e8f;
    }

    .link.deal,
    .crosslink.deal {
      stroke: #fc941f;
    }

    .link.hover-other,
    .crosslink.hover-other {
      opacity: 0.2;
    }

    .link.hover,
    .crosslink.hover {
      opacity: 1;
    }

    .node.has-children circle {
      stroke-dasharray: 0.2em;
    }
  }
  #investor-legend {
    .legend-icon {
      display: inline-block;
      width: 1em;
      height: 1em;
      position: relative;
      top: 0.15em;
      margin-right: 0.75em;
    }

    .legend-icon.deal {
      border-style: none;
      border-width: 0;
      background-color: #fc941f;
      margin-left: 0;
      margin-right: 0.5em;
      top: -0.3em;
      height: 0.15em;
      width: 1.25em;
    }

    .legend-icon.parent {
      border-style: solid;
      border-width: 0.5em 0.75em 0.5em 0;
      border-color: transparent #72b0fd transparent transparent;
      margin-left: -0.25em;
      margin-right: 1em;
    }

    .legend-icon.parent:after,
    .legend-icon.tertiary:after {
      content: " ";
      border-top: 2px solid #72b0fd;
      position: absolute;
      top: 50%;
      left: 1em;
      width: 0.5em;
      margin-top: -1px;
    }

    .legend-icon.tertiary:after {
      border-top-color: #f78e8f;
    }

    .legend-icon.tertiary {
      border-style: solid;
      border-width: 0.5em 0.75em 0.5em 0;
      border-color: transparent #f78e8f transparent transparent;
      margin-left: -0.25em;
      margin-right: 1em;
    }

    .legend-icon.has-children {
      border-width: 2px;
      border-style: dotted;
      border-color: #44b7b6;
      border-radius: 50%;
    }

    .legend-icon.investor {
      border-width: 2px;
      border-style: solid;
      border-color: #44b7b6;
      border-radius: 50%;
    }
  }
</style>
