<script lang="ts">
  import type { ElementDefinition, EventHandler, Core as Graph } from "cytoscape";
  import { onMount, tick } from "svelte";
  import { _ } from "svelte-i18n";
  import type { Investor } from "$lib/types/investor";
  import CompressIcon from "$components/icons/CompressIcon.svelte";
  import ExpandIcon from "$components/icons/ExpandIcon.svelte";
  import DealDetailModal from "$components/Investor/DealDetailModal.svelte";
  import InvestorDetailModal from "$components/Investor/InvestorDetailModal.svelte";
  import {
    createGraph,
    createGraphElements,
    registerTippy,
  } from "$components/Investor/investorGraph";

  export let investor: Investor;
  export let showDealsOnLoad = true;
  export let initDepth = 1;

  const MAX_DEPTH = 5;
  let depth = initDepth;

  let modalData = {};
  let isFullscreen = false;
  let showInvestorModal = false;
  let showDealModal = false;
  let showDeals = showDealsOnLoad;

  let cyGraph: Graph;
  const drawGraph = () => {
    cyGraph = createGraph(elements);
    registerTippy(cyGraph);
    registerModal(cyGraph);
  };

  let elements: ElementDefinition[] = [];
  $: {
    if (investor) {
      elements = createGraphElements(investor, [], showDeals, depth);
      if (cyGraph) {
        drawGraph();
      }
    }
  }

  const registerModal = (cyGraph) => {
    cyGraph.ready(() => {
      cyGraph.nodes().on("tap", showNodeModal);
      cyGraph.nodes().on("cxttap", showNodeModal);
    });
  };

  const showNodeModal: EventHandler = (e) => {
    e.preventDefault();
    modalData = e.target.data();

    if (modalData.dealNode) showDealModal = true;
    else showInvestorModal = true;
  };

  const toggleFullscreen = async () => {
    isFullscreen = !isFullscreen;
    await tick();
    drawGraph();
  };

  onMount(drawGraph);
</script>

<InvestorDetailModal
  visible={showInvestorModal}
  investor={modalData}
  on:close={() => (showInvestorModal = false)}
/>

<DealDetailModal
  visible={showDealModal}
  deal={modalData}
  on:close={() => (showDealModal = false)}
/>

<p class="mb-5">
  {$_("Please click the nodes to get more details.")}
</p>

<div id="investor-network-wrapper" class:network-fullscreen={isFullscreen}>
  <div id="toggle-fullscreen-button">
    <button type="button" on:click={toggleFullscreen}>
      {#if isFullscreen}
        <CompressIcon />
      {:else}
        <ExpandIcon />
      {/if}
    </button>
  </div>

  <div id="investor-network" class:network-fullscreen={isFullscreen} />

  <div id="investor-controls" class="flex flex-row">
    <div class="basis-1/2 p-2">
      <div class="pb-3">
        <label for="investor-level">
          <strong>{$_("Level of parent investors")}</strong>
        </label>
        <div class="w-1/2">
          <input
            bind:value={depth}
            id="investor-level"
            type="range"
            min="1"
            max={MAX_DEPTH}
          />
          {depth}
        </div>
      </div>

      <div>
        <label for="investor-deals" class="pr-3"
          ><strong>{$_("Show deals")}</strong></label
        >
        <input bind:checked={showDeals} id="investor-deals" type="checkbox" />
      </div>
    </div>

    <div id="investor-legend" class="basis-1/2 p-2">
      <strong>Legend</strong>
      <ul>
        <li>
          <span class="legend-icon deal" />{$_("Is operating company of")}
        </li>
        <li><span class="legend-icon parent" />{$_("Is parent company of")}</li>
        <li>
          <span class="legend-icon tertiary" />{$_("Is tertiary investor/lender of")}
        </li>
      </ul>
    </div>
  </div>
</div>

<style lang="scss">
  #investor-network-wrapper {
    position: relative;

    #toggle-fullscreen-button {
      right: 12px;
      position: absolute;
      top: 7px;
      z-index: 99;
      cursor: pointer;
    }

    &.network-fullscreen {
      position: fixed;
      top: 100px;
      left: 0;
      margin-left: 5%;
      margin-right: 5%;
      margin-top: 0;
      width: 90%;
      max-height: 80%;
      background: #ffffff;
      z-index: 98;
      border: 1px solid black;

      #toggle-fullscreen-button {
        right: 10px;
        top: 5px;
      }
    }

    #investor-network {
      border: 2px solid #ddd;
      display: block;
      width: 100%;
      min-height: 400px;
      max-height: 400px;
      cursor: all-scroll;
      overflow: hidden;

      &.network-fullscreen {
        width: 100%;
        max-width: 100%;
        height: 60vh;
        max-height: 60vh;
        min-height: 60vh;
      }
    }
  }

  #investor-legend {
    @mixin arrow {
      border-color: transparent;
      border-style: solid;
      border-width: 0.5em 0.75em 0.5em 0;
      margin-left: -0.25em;
      margin-right: 1em;

      &:after {
        content: " ";
        border-top: 2px solid;
        position: absolute;
        top: 50%;
        left: 1em;
        width: 0.5em;
        margin-top: -1px;
      }
    }

    .legend-icon {
      display: inline-block;
      width: 1em;
      height: 1em;
      position: relative;
      top: 0.15em;
      margin-right: 0.75em;

      &.deal {
        border-style: none;
        border-width: 0;
        background-color: var(--color-lm-orange);
        margin-left: 0;
        margin-right: 0.5em;
        top: -0.3em;
        height: 0.15em;
        width: 1.25em;
      }

      &.parent {
        @include arrow;
        border-right-color: #f78e8f;

        &:after {
          border-top-color: #f78e8f;
        }
      }

      &.tertiary {
        @include arrow;
        border-right-color: #72b0fd;

        &:after {
          border-top-color: #72b0fd;
        }
      }
    }
  }

  :global(.g-tooltip) {
    color: white;
    border-radius: 3px;
    padding: 3px 7px;
    margin-top: -5px;
    text-align: center;

    :global(.name) {
      font-weight: bold;
      display: block;
    }
  }

  :global(.g-tooltip.deal) {
    background-color: var(--color-lm-orange);
  }
  :global(.g-tooltip.investor) {
    background-color: var(--color-lm-investor);
  }
</style>
