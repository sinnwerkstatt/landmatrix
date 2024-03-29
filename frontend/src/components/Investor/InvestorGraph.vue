<template>
  <div v-if="investor.involvements" class="investor-graph">
    <InvestorDetailInvestorModal v-model="showInvestorModal" :investor="modalData" />
    <InvestorDetailDealModal v-model="showDealModal" :deal="modalData" />

    <p class="mb-0 font-italic small">
      {{ $t("Please click the nodes to get more details.") }}
    </p>
    <div id="investor-network-wrapper" :class="{ network_fs }">
      <div class="close_button">
        <a class="" @click="fullscreen_switch">
          <i v-if="network_fs" class="fas fa-compress"></i>
          <i v-else class="fas fa-expand"></i>
        </a>
      </div>
      <div id="investor-network" :class="{ network_fs }"></div>

      <div class="row bottom-content">
        <div v-if="controls" id="investor-level" class="col-sm-6 mt-1">
          <div class="slider-container col-sm-8">
            <label>
              <strong>{{ $t("Level of parent investors") }}</strong>
              <input
                v-model="depth"
                type="range"
                class="custom-range"
                min="1"
                :max="maxDepth"
                @change="refresh_graph"
              />

              <em>{{ depth }}</em>
            </label>
          </div>

          <div class="col-sm-8 custom-control custom-checkbox">
            <input
              id="show_deals"
              v-model="showDeals"
              type="checkbox"
              class="form-check-input custom-control-input"
              @change="refresh_graph"
            />
            <label for="show_deals" class="form-check-label custom-control-label">
              Show deals
            </label>
          </div>
        </div>
        <div
          id="investor-legend"
          class="mt-1"
          :class="{ 'col-sm-6': controls, 'col-sm-12': !controls }"
        >
          <h6>Legend</h6>
          <ul class="list-unstyled">
            <li v-if="showDeals">
              <span class="legend-icon deal"></span>Is operating company of
            </li>
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
  import { classification_choices } from "$utils/choices";
  import { investor_color, primary_color } from "$utils/colors";

  import cytoscape from "cytoscape";
  import coseBilkent from "cytoscape-cose-bilkent";
  import popper from "cytoscape-popper";
  import { pick } from "lodash-es";
  import tippy from "tippy.js";

  import InvestorDetailDealModal from "./InvestorDetailDealModal";
  import InvestorDetailInvestorModal from "./InvestorDetailInvestorModal";

  cytoscape.use(coseBilkent);
  cytoscape.use(popper);

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

  function makePopper(ele) {
    let ref = ele.popperRef(); // used only for positioning
    if (ref) {
      // unfortunately, a dummy element must be passed as tippy only accepts a dom element as the target
      // https://github.com/atomiks/tippyjs/issues/661
      let dummyDomEle = document.createElement("div");

      ele.tippy = tippy(dummyDomEle, {
        trigger: "manual", // call show() and hide() yourself
        lazy: false, // needed for onCreate()
        onCreate: (instance) => {
          instance.popperInstance.reference = ref;
        }, // needed for `ref` positioning
        content: () => {
          let tipEl = document.createElement("div");
          tipEl.classList.add("g-tooltip");
          if (ele.data().dealNode) {
            // tooltip content of deal node
            tipEl.classList.add("deal");
            tipEl.innerHTML = `Deal ${ele.data().name}`;
          } else {
            // tooltip content of investor node
            let content = `<span class="name">${ele.data().name} (#${
              ele.data().id
            })</span>`;
            if ("country" in ele.data() && ele.data().country)
              content += `${ele.data().country.name}, `;
            if (
              "classification" in ele.data() &&
              classification_choices[ele.data().classification]
            )
              content += classification_choices[ele.data().classification];
            tipEl.innerHTML = content;
          }
          return tipEl;
        },
      });
    }
  }

  export default {
    name: "InvestorGraph",
    components: { InvestorDetailDealModal, InvestorDetailInvestorModal },
    props: {
      investor: { type: Object, required: true },
      showDealsOnLoad: { type: Boolean, default: true },
      controls: { type: Boolean, default: true },
      initDepth: { type: Number, default: 1 },
    },
    data() {
      return {
        depth: this.initDepth,
        maxDepth: 9,
        modalData: {},
        network_fs: false,
        showInvestorModal: false,
        showDealModal: false,
        showDeals: true,
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
    mounted() {
      this.showDeals = this.showDealsOnLoad;
      this.do_the_graph();
    },
    methods: {
      fullscreen_switch() {
        this.network_fs = !this.network_fs;
        this.$nextTick(() => {
          this.do_the_graph();
        });
      },
      refresh_graph() {
        this.$emit("newDepth", this.depth);
        cy.elements().remove();
        cy.add(this.elements);
        window.setTimeout(() => {
          cy.layout(cyconfig.layout).run();
          this.add_onclick_modal();
        }, 200);
      },
      add_onclick_modal() {
        cy.ready(() => {
          cy.nodes().forEach(function (ele) {
            makePopper(ele);
          });
          cy.nodes().unbind("mouseover");
          cy.nodes().bind("mouseover", (event) => event.target.tippy.show());
          cy.nodes().unbind("mouseout");
          cy.nodes().bind("mouseout", (event) => event.target.tippy.hide());
        });
        cy.nodes().on("tap", this.showNodeModal);
        cy.nodes().on("cxttap", this.showNodeModal);
      },
      showNodeModal(e) {
        e.preventDefault();
        this.modalData = e.target.data();
        // delay to avoid context menu from opening
        window.setTimeout(() => {
          if (this.modalData.rootNode) this.showInvestorModal = true;
          if (this.modalData.dealNode) this.showDealModal = true;
          else this.showInvestorModal = true;
        }, 10);
      },
      build_graph(investor, elements, depth) {
        if (depth <= 0) return;

        if (this.showDeals) {
          investor.deals.forEach((deal) => {
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
        this.add_onclick_modal();
      },
    },
  };
</script>

<style lang="scss">
  .investor-graph {
    max-width: 1000px;
  }

  #investor-network-wrapper {
    position: relative;

    .close_button {
      right: 12px;
      position: absolute;
      text-align: right;
      top: 7px;
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
        top: 5px;
      }

      #investor-legend {
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
      max-height: 60vh;
      min-height: 60vh;
    }
  }

  .network_fs {
    min-height: 60vh;

    .bottom-content {
      padding: 15px;
      height: 40%;
    }
  }

  #investor-level {
    .custom-range {
      margin-left: -15px;

      &::-webkit-slider-thumb,
      &::-moz-range-thumb,
      &::-ms-thumb {
        background: var(--color-lm-orange);
      }
    }

    .custom-checkbox {
      margin-top: 0.3em;
      margin-bottom: 2em;
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
      background-color: var(--color-lm-orange);
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

  .g-tooltip {
    background-color: var(--color-lm-investor);
    color: white;
    border-radius: 3px;
    padding: 3px 7px;
    margin-top: -5px;
    text-align: center;

    .name {
      font-weight: bold;
      display: block;
    }

    &.deal {
      background-color: var(--color-lm-orange);
    }
  }
</style>
