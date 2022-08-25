<script lang="ts">
  import cn from "classnames";
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
  export let showControls = false;

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

<div
  class={isFullscreen
    ? "fixed bg-white border border-solid border-black top-12 left-0 mx-[5%] my-[5%] w-[90%] h-[70%]"
    : "relative"}
>
  <div class="absolute right-3 top-1.5 z-[9] cursor-pointer">
    <button type="button" on:click={toggleFullscreen}>
      {#if isFullscreen}
        <CompressIcon />
      {:else}
        <ExpandIcon />
      {/if}
    </button>
  </div>

  <div class={isFullscreen ? "h-full" : "h-96"}>
    <div
      id="investor-network"
      class="min-h-full w-full cursor-all-scroll border-2 border-solid"
    />
  </div>

  <div class="flex flex-row bg-white">
    {#if showControls}
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
    {/if}
    <div class="basis-1/2 p-2">
      <strong>{$_("Legend")}</strong>
      <ul>
        <li>
          <span
            class={cn(
              "inline-block relative w-5 h-1.5 mr-1",
              "border-t-2 border-t-orange"
            )}
          />{$_("Is operating company of")}
        </li>
        <li>
          <span
            class={cn(
              "inline-block relative w-0 h-0 mr-3",
              "border-y-transparent border-y-8 border-r-[12px] border-[#f78e8f]",
              "after:absolute after:w-3 after:left-2 after:border-t-2 after:border-[#f78e8f]"
            )}
          />{$_("Is parent company of")}
        </li>
        <li>
          <span
            class={cn(
              "inline-block relative w-0 h-0 mr-3",
              "border-y-transparent border-y-8 border-r-[12px] border-[#72b0fd]",
              "after:absolute after:w-3 after:left-2 after:border-t-2 after:border-[#72b0fd]"
            )}
          />{$_("Is tertiary investor/lender of")}
        </li>
      </ul>
    </div>
  </div>
</div>

<style>
  :global(.g-tooltip) {
    color: white;
    border-radius: 3px;
    padding: 3px 7px;
    margin-top: -5px;
    text-align: center;
  }

  /*Space between classes to indicate nesting*/
  :global(.g-tooltip .name) {
    font-weight: bold;
    display: block;
  }

  /*No space when all classes apply to same element*/
  :global(.g-tooltip.deal) {
    background-color: var(--color-lm-orange);
  }
  :global(.g-tooltip.investor) {
    background-color: var(--color-lm-investor);
  }
</style>
