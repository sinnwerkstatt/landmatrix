<script lang="ts">
  import { _ } from "svelte-i18n";
  import type { Investor } from "$lib/types/investor";

  // import { classification_choices } from "$utils/choices";
  // import { investor_color, primary_color } from "$utils/colors";
  //

  // import tippy from "tippy.js";
  //

  // TODO  maybe use d3: https://codepen.io/fabvit86/pen/RLKbab ?

  function makePopper(ele) {
    let ref = ele.popperRef(); // used only for positioning
    // if (ref) {
    //   // unfortunately, a dummy element must be passed as tippy only accepts a dom element as the target
    //   // https://github.com/atomiks/tippyjs/issues/661
    //   let dummyDomEle = document.createElement("div");
    //
    //   ele.tippy = tippy(dummyDomEle, {
    //     trigger: "manual", // call show() and hide() yourself
    //     lazy: false, // needed for onCreate()
    //     onCreate: (instance) => {
    //       instance.popperInstance.reference = ref;
    //     }, // needed for `ref` positioning
    //     content: () => {
    //       let tipEl = document.createElement("div");
    //       tipEl.classList.add("g-tooltip");
    //       if (ele.data().dealNode) {
    //         // tooltip content of deal node
    //         tipEl.classList.add("deal");
    //         tipEl.innerHTML = `Deal ${ele.data().name}`;
    //       } else {
    //         // tooltip content of investor node
    //         let content = `<span class="name">${ele.data().name} (#${
    //           ele.data().id
    //         })</span>`;
    //         if ("country" in ele.data() && ele.data().country)
    //           content += `${ele.data().country.name}, `;
    //         if (
    //           "classification" in ele.data() &&
    //           classification_choices[ele.data().classification]
    //         )
    //           content += classification_choices[ele.data().classification];
    //         tipEl.innerHTML = content;
    //       }
    //       return tipEl;
    //     },
    //   });
    // }
  }

  export let investor: Investor;
  export let showDealsOnLoad: true;
  export let controls: true;
  export let initDepth: 1;

  const maxDepth = 9;
  let depth = initDepth;

  let modalData = {};
  let network_fs = false;
  let showInvestorModal = false;
  let showDealModal = false;
  let showDeals = true;

  // $: elements = calculateGraph(investor, null, showDeals, initDepth);

  //   mounted() {
  //     this.showDeals = this.showDealsOnLoad;
  //     this.do_the_graph();
  //   },
  //   methods: {
  //     fullscreen_switch() {
  //       this.network_fs = !this.network_fs;
  //       this.$nextTick(() => {
  //         this.do_the_graph();
  //       });
  //     },
  //     refresh_graph() {
  //       this.$emit("newDepth", this.depth);
  //       cy.elements().remove();
  //       cy.add(this.elements);
  //       window.setTimeout(() => {
  //         cy.layout(cyconfig.layout).run();
  //         this.add_onclick_modal();
  //       }, 200);
  //     },
  //     add_onclick_modal() {
  //       cy.ready(() => {
  //         cy.nodes().forEach(function (ele) {
  //           makePopper(ele);
  //         });
  //         cy.nodes().unbind("mouseover");
  //         cy.nodes().bind("mouseover", (event) => event.target.tippy.show());
  //         cy.nodes().unbind("mouseout");
  //         cy.nodes().bind("mouseout", (event) => event.target.tippy.hide());
  //       });
  //       cy.nodes().on("tap", this.showNodeModal);
  //       cy.nodes().on("cxttap", this.showNodeModal);
  //     },
  //     showNodeModal(e) {
  //       e.preventDefault();
  //       this.modalData = e.target.data();
  //       // delay to avoid context menu from opening
  //       window.setTimeout(() => {
  //         if (this.modalData.rootNode) this.showInvestorModal = true;
  //         if (this.modalData.dealNode) this.showDealModal = true;
  //         else this.showInvestorModal = true;
  //       }, 10);
  //     },

  //     do_the_graph() {
  //       cy = cytoscape({
  //         container: document.getElementById("investor-network"),
  //         elements: this.elements,
  //         ...cyconfig,
  //       });
  //       this.add_onclick_modal();
  //     },
  //
</script>

<div class="max-w-[1000px]">
  <!--    <InvestorDetailInvestorModal v-model="showInvestorModal" :investor="modalData" />-->
  <!--    <InvestorDetailDealModal v-model="showDealModal" :deal="modalData" />-->

  <p class="mb-0 font-italic small">
    {$_("Please click the nodes to get more details.")}
  </p>
  <!--    <div id="investor-network-wrapper" :class="{ network_fs }">-->
  <!--      <div class="close_button">-->
  <!--        <a class="" @click="fullscreen_switch">-->
  <!--          <i v-if="network_fs" class="fas fa-compress"></i>-->
  <!--          <i v-else class="fas fa-expand"></i>-->
  <!--        </a>-->
  <!--      </div>-->
  <!--      <div id="investor-network" :class="{ network_fs }"></div>-->

  <!--      <div class="row bottom-content">-->
  <!--        <div v-if="controls" id="investor-level" class="col-sm-6 mt-1">-->
  <!--          <div class="slider-container col-sm-8">-->
  <!--            <label>-->
  <!--              <strong>{{ $t("Level of parent investors") }}</strong>-->
  <!--              <input-->
  <!--                v-model="depth"-->
  <!--                type="range"-->
  <!--                class="custom-range"-->
  <!--                min="1"-->
  <!--                :max="maxDepth"-->
  <!--                @change="refresh_graph"-->
  <!--              />-->

  <!--              <em>{{ depth }}</em>-->
  <!--            </label>-->
  <!--          </div>-->

  <!--          <div class="col-sm-8 custom-control custom-checkbox">-->
  <!--            <input-->
  <!--              id="show_deals"-->
  <!--              v-model="showDeals"-->
  <!--              type="checkbox"-->
  <!--              class="form-check-input custom-control-input"-->
  <!--              @change="refresh_graph"-->
  <!--            />-->
  <!--            <label for="show_deals" class="form-check-label custom-control-label">-->
  <!--              Show deals-->
  <!--            </label>-->
  <!--          </div>-->
  <!--        </div>-->
  <!--        <div-->
  <!--          id="investor-legend"-->
  <!--          class="mt-1"-->
  <!--          :class="{ 'col-sm-6': controls, 'col-sm-12': !controls }"-->
  <!--        >-->
  <!--          <h6>Legend</h6>-->
  <!--          <ul class="list-unstyled">-->
  <!--            <li v-if="showDeals">-->
  <!--              <span class="legend-icon deal"></span>Is operating company of-->
  <!--            </li>-->
  <!--            <li><span class="legend-icon parent"></span>Is parent company of</li>-->
  <!--            <li>-->
  <!--              <span class="legend-icon tertiary"></span>Is tertiary investor/lender of-->
  <!--            </li>-->
  <!--          </ul>-->
  <!--        </div>-->
  <!--      </div>-->
  <!--    </div>-->
</div>

<!--<style lang="scss">-->

<!--  #investor-network-wrapper {-->
<!--    position: relative;-->

<!--    .close_button {-->
<!--      right: 12px;-->
<!--      position: absolute;-->
<!--      text-align: right;-->
<!--      top: 7px;-->
<!--      z-index: 2000;-->
<!--      cursor: pointer;-->
<!--    }-->

<!--    &.network_fs {-->
<!--      position: fixed;-->
<!--      top: 100px;-->
<!--      left: 0;-->
<!--      margin-left: 5%;-->
<!--      margin-right: 5%;-->
<!--      margin-top: 0;-->
<!--      width: 90%;-->
<!--      max-height: 80%;-->
<!--      background: #ffffff;-->
<!--      z-index: 1000;-->
<!--      border: 1px solid black;-->

<!--      .close_button {-->
<!--        right: 10px;-->
<!--        top: 5px;-->
<!--      }-->

<!--      #investor-legend {-->
<!--      }-->
<!--    }-->
<!--  }-->

<!--  div#investor-network {-->
<!--    border: 2px solid #ddd;-->
<!--    display: block;-->
<!--    max-width: 1000px;-->
<!--    min-height: 300px;-->
<!--    max-height: 500px;-->
<!--    cursor: all-scroll;-->
<!--    overflow: hidden;-->

<!--    &.network_fs {-->
<!--      width: 100%;-->
<!--      max-width: 100%;-->
<!--      height: 60vh;-->
<!--      max-height: 60vh;-->
<!--      min-height: 60vh;-->
<!--    }-->
<!--  }-->

<!--  .network_fs {-->
<!--    min-height: 60vh;-->

<!--    .bottom-content {-->
<!--      padding: 15px;-->
<!--      height: 40%;-->
<!--    }-->
<!--  }-->

<!--  #investor-level {-->
<!--    .custom-range {-->
<!--      margin-left: -15px;-->

<!--      &::-webkit-slider-thumb,-->
<!--      &::-moz-range-thumb,-->
<!--      &::-ms-thumb {-->
<!--        background: var(&#45;&#45;color-lm-orange);-->
<!--      }-->
<!--    }-->

<!--    .custom-checkbox {-->
<!--      margin-top: 0.3em;-->
<!--      margin-bottom: 2em;-->
<!--    }-->
<!--  }-->

<!--  #investor-legend {-->
<!--    .legend-icon {-->
<!--      display: inline-block;-->
<!--      width: 1em;-->
<!--      height: 1em;-->
<!--      position: relative;-->
<!--      top: 0.15em;-->
<!--      margin-right: 0.75em;-->
<!--    }-->

<!--    .legend-icon.deal {-->
<!--      border-style: none;-->
<!--      border-width: 0;-->
<!--      background-color: var(&#45;&#45;color-lm-orange);-->
<!--      margin-left: 0;-->
<!--      margin-right: 0.5em;-->
<!--      top: -0.3em;-->
<!--      height: 0.15em;-->
<!--      width: 1.25em;-->
<!--    }-->

<!--    .legend-icon.parent {-->
<!--      border-style: solid;-->
<!--      border-width: 0.5em 0.75em 0.5em 0;-->
<!--      border-color: transparent #72b0fd transparent transparent;-->
<!--      margin-left: -0.25em;-->
<!--      margin-right: 1em;-->
<!--    }-->

<!--    .legend-icon.parent:after,-->
<!--    .legend-icon.tertiary:after {-->
<!--      content: " ";-->
<!--      border-top: 2px solid #72b0fd;-->
<!--      position: absolute;-->
<!--      top: 50%;-->
<!--      left: 1em;-->
<!--      width: 0.5em;-->
<!--      margin-top: -1px;-->
<!--    }-->

<!--    .legend-icon.tertiary:after {-->
<!--      border-top-color: #f78e8f;-->
<!--    }-->

<!--    .legend-icon.tertiary {-->
<!--      border-style: solid;-->
<!--      border-width: 0.5em 0.75em 0.5em 0;-->
<!--      border-color: transparent #f78e8f transparent transparent;-->
<!--      margin-left: -0.25em;-->
<!--      margin-right: 1em;-->
<!--    }-->

<!--    .legend-icon.has-children {-->
<!--      border-width: 2px;-->
<!--      border-style: dotted;-->
<!--      border-color: #44b7b6;-->
<!--      border-radius: 50%;-->
<!--    }-->

<!--    .legend-icon.investor {-->
<!--      border-width: 2px;-->
<!--      border-style: solid;-->
<!--      border-color: #44b7b6;-->
<!--      border-radius: 50%;-->
<!--    }-->
<!--  }-->

<!--  .g-tooltip {-->
<!--    background-color: var(&#45;&#45;color-lm-investor);-->
<!--    color: white;-->
<!--    border-radius: 3px;-->
<!--    padding: 3px 7px;-->
<!--    margin-top: -5px;-->
<!--    text-align: center;-->

<!--    .name {-->
<!--      font-weight: bold;-->
<!--      display: block;-->
<!--    }-->

<!--    &.deal {-->
<!--      background-color: var(&#45;&#45;color-lm-orange);-->
<!--    }-->
<!--  }-->
<!--</style>-->
