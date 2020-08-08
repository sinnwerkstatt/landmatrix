<template>
  <div v-if="investor.involvements.length">
    <b-modal
      id="investor-detail-modal"
      :title="`${modalInfo.name} (#${modalInfo._id})`"
    >
      <p>{{ modalInfo.classification }}</p>
      <p>{{ modalInfo.comment }}</p>
      <p>{{ modalInfo.country && modalInfo.country.name }}</p>

      <div v-if="modalInfo.involvement">
        <h2>Involvement</h2>
        {{ modalInfo.involvement }}
      </div>
      <template v-slot:modal-footer>
        <div class="w-100">
          <router-link
            :to="modalInfo.link"
            class="btn btn-primary investor-link float-right"
            target="_blank"
            v-slot="{ href }"
            v-if="modalInfo.link"
          >
            <a :href="href">More details about this investor</a>
          </router-link>
        </div>
      </template>
    </b-modal>

    <div id="investor-network-wrapper" :class="{ network_fs }">
      <div class="close_button">
        <a class="" @click="fullscreen_switch">
          <i v-if="network_fs" class="fas fa-compress"></i>
          <i v-else class="fas fa-expand"></i>
        </a>
      </div>
      <div id="investor-network" :class="{ network_fs }"></div>

      <div class="row">
        <div id="investor-level" class="col-sm-6">
          <h5>Level of parent investors</h5>
          <div class="slider-container col-sm-8">
            <input
              type="range"
              min="1"
              :max="maxDepth"
              value="1"
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
                v-model="show_deals"
                @change="refresh_graph"
              />
              Show deals
            </label>
          </div>
        </div>
        <div id="investor-legend" class="col-sm-6">
          <h5>Legend</h5>
          <ul class="list-unstyled">
            <li><span class="legend-icon deal"></span>Is operating company of</li>
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

  cytoscape.use(coseBilkent);

  let cy = null;

  const cyconfig = {
    layout: {
      name: "cose-bilkent",
      quality: "proof",
      nodeDimensionsIncludeLabels: true,
      // padding: 50,
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

  const investor_fields = ["id", "name", "comment", "country", "classification"];

  export default {
    props: ["investor"],
    data() {
      return {
        depth: 1,
        maxDepth: 4,
        modalInfo: {},
        show_deals: true,
        network_fs: false,
      };
    },
    computed: {
      elements() {
        let elements = [
          {
            data: {
              ...pick(this.investor, investor_fields),
              _id: this.investor.id,
              bgcolor: "#44b7b6",
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
        cy.layout(cyconfig.layout).run();
        this.add_rightclick_modal();
      },
      add_rightclick_modal() {
        cy.nodes().on("cxttap", (e) => {
          this.modalInfo = e.target.data();
          this.$bvModal.show("investor-detail-modal");
        });
      },
      build_graph(investor, elements, depth) {
        if (depth <= 0) return;

        if (this.show_deals) {
          investor.deals.forEach((deal) => {
            let deal_node = {
              data: {
                id: "D" + deal.id,
                name: "#" + deal.id,
                _id: deal.id,
                bgcolor: "#fc941f",
                link: { name: "deal_detail", params: { deal_id: deal.id } },
              },
            };
            let deal_edge = {
              data: {
                id: `${investor.id}_D${deal.id}`,
                source: investor.id,
                target: "D" + deal.id,
                edge_color: "#fc941f",
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
              _id: involvement.investor.id,
              involvement: pick(involvement, ["role", "involvement_type"]),
              link: {
                name: "investor_detail",
                params: { investor_id: involvement.investor.id },
              },
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
        this.add_rightclick_modal();
      },
    },
    mounted() {
      this.do_the_graph();
    },
  };
</script>

<style lang="scss">
  #investor-network-wrapper {
    .close_button {
      right: 20px;
      position: absolute;
      z-index: 2000;
      cursor: pointer;
    }
    &.network_fs {
      position: fixed;
      top: 100px;
      left: 0;

      margin-left: 5%;
      margin-right: 5%;
      width: 90%;
      height: 80%;
      background: #ffffff;
      z-index: 1000;
      border: 1px solid black;
      .close_button {
        right: 5px;
      }
    }
  }
  div#investor-network {
    border: 2px solid #ddd;
    display: block;
    max-width: 900px;
    min-height: 300px;
    max-height: 460px;
    cursor: all-scroll;
    overflow: hidden;
    &.network_fs {
      width: 100%;
      max-width: 100%;
      height: 80%;
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
