<template>
  <div class="investor-graph" v-if="investor.involvements.length">
    <InvestorDetailInvestorModal v-model="showInvestorModal" :investor="modalData" />
    <InvestorDetailDealModal v-model="showDealModal" :deal="modalData" />

    <p class="mb-0 font-italic small">Please right-click the nodes to get more details.</p>
    <div id="investor-network-wrapper" :class="{ network_fs }">
      <div class="close_button">
        <a class="" @click="fullscreen_switch">
          <i v-if="network_fs" class="fas fa-compress"></i>
          <i v-else class="fas fa-expand"></i>
        </a>
      </div>
      <div id="investor-network" :class="{ network_fs }"></div>

      <div class="row">
        <div v-if="controls" id="investor-level" class="col-sm-6 mt-1">
          <h6>Level of parent investors</h6>
          <div class="slider-container col-sm-8">
            <input
              type="range"
              min="1"
              :max="maxDepth"
              v-model="depth"
              @change="refresh_graph"
            />
            <em>{{ depth }}</em>
          </div>

          <div class="col-sm-8">
            <label for="show_deals">
              <input
                type="checkbox"
                id="show_deals"
                v-model="showDeals"
                @change="refresh_graph"
              />
              Show deals
            </label>
          </div>
        </div>
        <div id="investor-legend" class="mt-1" :class="{ 'col-sm-6': controls, 'col-sm-12': !controls }">
          <h6>Legend</h6>
          <ul class="list-unstyled">
            <li v-if="showDeals"><span class="legend-icon deal"></span>Is operating company of</li>
            <li><span class="legend-icon parent"></span>Is parent company of</li>
            <li>
              <span class="legend-icon tertiary"></span>Is tertiary investor/lender of
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import cytoscape from "cytoscape";
  import coseBilkent from "cytoscape-cose-bilkent";
  import { pick } from "lodash";
  import { investor_color, primary_color } from "../../colors";
  import InvestorDetailInvestorModal from "./InvestorDetailInvestorModal";
  import InvestorDetailDealModal from "./InvestorDetailDealModal";

  cytoscape.use(coseBilkent);

  let cy = null;

  const cyconfig = {
    minZoom: 0.3,
    maxZoom: 5,
    layout: {
      name: "cose-bilkent",
      quality: "proof",
      nodeDimensionsIncludeLabels: true,
      animate: "end",
    },
    style: [
      {
        selector: "node",
        style: {
          "background-color": (obj) => {
            return obj.data("bgcolor") || "#bee7e7";
          },
          label: (obj) => {
            return obj.data("name");
          },
          "text-valign": "center",
          "font-size": "9pt",
          "text-wrap": "wrap",
          "text-max-width": "120px",
          // "shape": "ellipse",
        },
      },
      {
        selector: "edge",
        style: {
          width: 1,
          "line-color": "data(edge_color)",
          "target-arrow-color": "data(edge_color)",
          "target-arrow-shape": (obj) => {
            return obj.data("target_arrow_shape") || "none  ";
          },
          "curve-style": "bezier",
        },
      },
    ],
  };

  const investor_fields = [
    "id",
    "name",
    "comment",
    "country",
    "classification",
    "homepage",
  ];
  const involvement_fields = [
    "role",
    "investment_type",
    "involvement_type",
    "percentage",
    "loans_amount",
    "loans_currency",
    "loans_date",
    "parent_relation",
    "comment",
  ];

  export default {
    name: "InvestorGraph",
    components: { InvestorDetailDealModal, InvestorDetailInvestorModal },
    props: {
      investor: Object,
      showDeals: {
        type: Boolean,
        default: true,
      },
      controls: {
        type: Boolean,
        default: true,
      },
      depth: {
        type: Number,
        default: 1,
      },
    },
    data() {
      return {
        // depth: 1,
        maxDepth: 4,
        modalData: {},
        network_fs: false,
        showInvestorModal: false,
        showDealModal: false,
      };
    },
    computed: {
      elements() {
        let elements = [
          {
            data: {
              ...pick(this.investor, investor_fields),
              bgcolor: investor_color,
              rootNode: true,
            },
          },
        ];
        this.build_graph(this.investor, elements, this.depth);

        return elements;
      },
    },
    methods: {
      fullscreen_switch() {
        this.network_fs = !this.network_fs;
        this.$nextTick(() => {
          this.do_the_graph();
        });
      },
      refresh_graph() {
        cy.elements().remove();
        cy.add(this.elements);
        window.setTimeout(() => {
          cy.layout(cyconfig.layout).run();
          this.add_rightclick_modal();
        },200);
      },
      add_rightclick_modal() {
        cy.nodes().on("cxttap", (e) => {
          this.modalData = e.target.data();
          // delay to avoid context menu from opening
          window.setTimeout(() => {
            if (this.modalData.rootNode) this.showInvestorModal = true;
            if (this.modalData.dealNode) this.showDealModal = true;
            else this.showInvestorModal = true;
          }, 10);
        });
      },
      build_graph(investor, elements, depth) {
        if (depth <= 0) return;

        if (this.showDeals) {
          investor.deals.forEach((deal) => {
            console.log(deal);
            let deal_node = {
              data: {
                ...deal,
                _id: deal.id,
                id: "D" + deal.id,
                name: "#" + deal.id,
                bgcolor: primary_color,
                dealNode: true,
              },
            };
            let deal_edge = {
              data: {
                id: `${investor.id}_D${deal.id}`,
                source: investor.id,
                target: "D" + deal.id,
                edge_color: primary_color,
              },
            };

            elements.push(deal_node);
            elements.push(deal_edge);
          });
        }

        if (!investor.involvements || !investor.involvements.length) return;
        investor.involvements.forEach((involvement) => {
          let investor_node = {
            data: {
              ...pick(involvement.investor, investor_fields),
              involvement: pick(involvement, involvement_fields),
            },
          };
          let investor_edge = {
            data: {
              id: `${investor.id}_${involvement.investor.id}`,
              edge_color: involvement.role === "PARENT" ? "#72B0FD" : "#F78E8F",
              ...(involvement.involvement_type === "VENTURE"
                ? { source: investor.id, target: involvement.investor.id }
                : { source: involvement.investor.id, target: investor.id }),
              target_arrow_shape: "triangle",
            },
          };

          elements.push(investor_node);
          elements.push(investor_edge);

          this.build_graph(involvement.investor, elements, depth - 1);
        });
      },
      do_the_graph() {
        cy = cytoscape({
          container: document.getElementById("investor-network"),
          elements: this.elements,
          ...cyconfig,
        });
      },
    },
    mounted() {
      this.do_the_graph();
    },
  };
</script>

<style lang="scss">
  .investor-graph{
    max-width: 1000px;
  }
  #investor-network-wrapper {
    margin-top: -20px;
    .close_button {
      right: 12px;
      position: relative;
      text-align: right;
      top: 28px;
      z-index: 2000;
      cursor: pointer;
    }
    &.network_fs {
      position: fixed;
      top: 100px;
      left: 0;

      margin-left: 5%;
      margin-right: 5%;
      margin-top: 0;
      width: 90%;
      max-height: 80%;
      background: #ffffff;
      z-index: 1000;
      border: 1px solid black;
      .close_button {
        right: 10px;
        position: absolute;
        top: 5px;
      }
      #investor-legend {
        margin-left: 1rem;
        margin-top: 1rem !important;
      }
    }
  }
  div#investor-network {
    border: 2px solid #ddd;
    display: block;
    max-width: 1000px;
    min-height: 300px;
    max-height: 500px;
    cursor: all-scroll;
    overflow: hidden;
    &.network_fs {
      width: 100%;
      max-width: 100%;
      height: 60vh;
      max-height: 80%;
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
