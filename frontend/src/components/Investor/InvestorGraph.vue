<template>
  <div v-if="investor && investor.involvements.length">
    <div id="investor-network"></div>
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

        <!--        <div class="col-sm-8">-->
        <!--          <input-->
        <!--            type="checkbox"-->
        <!--            class="show_deals"-->
        <!--            id="show_deals"-->
        <!--            checked="checked"-->
        <!--            autocomplete="off"-->
        <!--          />-->
        <!--          <label for="show_deals">Show deals</label>-->
        <!--        </div>-->
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
        maxDepth: 10,
        modalInfo: {},
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
      refresh_graph() {
        // cy.elements().remove();
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
  div#investor-network {
    border: 2px solid #ddd;
    display: block;
    max-width: 900px;
    min-height: 300px;
    max-height: 460px;
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
