<script lang="ts">
  import type { ElementDefinition, EventHandler, Core as Graph } from "cytoscape"
  import { tick } from "svelte"
  import { _ } from "svelte-i18n"
  import { gql, queryStore } from "@urql/svelte"

  import { page } from "$app/stores"

  import type { Investor, Involvement } from "$lib/types/investor"

  import CompressIcon from "$components/icons/CompressIcon.svelte"
  import ExpandIcon from "$components/icons/ExpandIcon.svelte"
  import DealDetailModal from "$components/Investor/DealDetailModal.svelte"
  import InvestorDetailModal from "$components/Investor/InvestorDetailModal.svelte"
  import {
    createGraph,
    createGraphElements,
    registerTippy,
  } from "$components/Investor/investorGraph"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  export let investor: Investor
  export let showDealsOnLoad = true
  export let initDepth = 1
  export let includeVentures = false
  export let showControls = false

  const MAX_DEPTH = 5
  let depth = initDepth

  $: involvements = queryStore({
    client: $page.data.urqlClient,
    query: gql<{ involvement_network: Involvement[] }>`
      query InvolvementNetwork($id: Int!, $depth: Int!, $include_ventures: Boolean) {
        involvement_network(id: $id, depth: $depth, include_ventures: $include_ventures)
      }
    `,
    variables: {
      id: investor.id,
      depth: depth,
      include_ventures: includeVentures,
    },
  })

  let modalData: { dealNode: boolean } = {}
  let isFullscreen = false
  let showInvestorModal = false
  let showDealModal = false
  let showDeals = showDealsOnLoad

  let cyGraph: Graph
  const drawGraph = () => {
    cyGraph = createGraph(graphContainer, elements)
    registerTippy(cyGraph)
    registerModal(cyGraph)
  }

  let elements: ElementDefinition[] = []
  $: if (investor && $involvements.data) {
    elements = createGraphElements(
      investor,
      $involvements.data.involvement_network,
      [],
      showDeals,
      depth,
    )
  }

  let graphContainer: HTMLDivElement
  $: if (graphContainer) {
    drawGraph()
  }

  const registerModal = cyGraph => {
    cyGraph.ready(() => {
      cyGraph.nodes().on("tap", showNodeModal)
      cyGraph.nodes().on("cxttap", showNodeModal)
    })
  }

  const showNodeModal: EventHandler = e => {
    e.preventDefault()
    modalData = e.target.data()

    if (modalData.dealNode) showDealModal = true
    else showInvestorModal = true
  }

  const toggleFullscreen = async () => {
    isFullscreen = !isFullscreen
    await tick()
    drawGraph()
  }
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
    ? "fixed top-12 left-0 mx-[5%] my-[5%] h-[70%] w-[90%] border border-solid border-black bg-white"
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
    {#if $involvements.fetching}
      <LoadingPulse class="pt-5" />
    {:else if $involvements.error}
      <p>Error...{$involvements.error.message}</p>
    {:else}
      <div
        bind:this={graphContainer}
        class="min-h-full w-full cursor-all-scroll border-2 border-solid"
      />
    {/if}
  </div>

  <div class="flex flex-row bg-white dark:bg-gray-700">
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
          <label for="investor-deals" class="pr-3">
            <strong>{$_("Show deals")}</strong>
          </label>
          <input bind:checked={showDeals} id="investor-deals" type="checkbox" />
        </div>
      </div>
    {/if}
    <div class="basis-1/2 p-2">
      <strong>{$_("Legend")}</strong>
      <ul>
        <li>
          <span class="colored-line" style:--color="#fc941f" />
          {$_("Is operating company of")}
        </li>
        <li>
          <span class="colored-arrow" style:--color="#f78e8f" />
          {$_("Is parent company of")}
        </li>
        <li>
          <span class="colored-arrow" style:--color="#72b0fd" />
          {$_("Is tertiary investor/lender of")}
        </li>
      </ul>
    </div>
  </div>
</div>

<style lang="css">
  .colored-line {
    @apply relative mr-1 inline-block h-1.5 w-5 border-t-2 border-t-[var(--color)];
  }
  .colored-arrow {
    @apply relative mr-3 inline-block h-0 w-0;
    @apply border-y-8 border-r-[12px] border-[var(--color)] border-y-transparent;
    @apply after:absolute after:left-2 after:w-3 after:border-t-2 after:border-[var(--color)];
  }

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
