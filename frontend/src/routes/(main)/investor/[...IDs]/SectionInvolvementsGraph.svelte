<script lang="ts">
  import type { ElementDefinition, EventHandler, Core as Graph } from "cytoscape"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { loading } from "$lib/stores"
  import type { InvestorHull } from "$lib/types/newtypes"

  import DealDetailModal from "./DealDetailModal.svelte"
  import InvestorDetailModal from "./InvestorDetailModal.svelte"
  import { createGraph, LAYOUT_OPTIONS, registerTippy } from "./investorGraphNew"

  // import { createGraph, registerTippy } from "$components/Investor/investorGraph"

  export let investor: InvestorHull

  export let hideControls = false
  export let showDeals = true

  let cyGraph: Graph
  let graphContainer: HTMLDivElement
  let modalData: { dealNode: boolean } = {}
  let showInvestorModal = false
  let showDealModal = false

  let depth = 3
  let max_depth = 30
  let reachedMaxDepth = false

  let elements: ElementDefinition[] = []

  async function fetchInvolvments() {
    loading.set(true)
    const ret = await fetch(
      `/api/investors/${investor.id}/involvements_graph/?depth=${depth}&include_deals=${showDeals}`,
    )
    const retJson = await ret.json()

    elements = retJson.network.elements
    console.log("nodes", elements.nodes.length)
    if (retJson.network.full_depth) {
      reachedMaxDepth = true
      max_depth = retJson.network.full_depth
      depth = max_depth
    }
    loading.set(false)
  }
  onMount(async () => {
    await fetchInvolvments()
  })

  const showNodeModal: EventHandler = e => {
    e.preventDefault()
    modalData = e.target.data()

    if (modalData.dealNode) {
      showDealModal = true
    } else {
      showInvestorModal = true
    }
  }

  const registerModal = (cyGraph: Graph) => {
    cyGraph.ready(() => {
      cyGraph.nodes().on("tap", showNodeModal)
      cyGraph.nodes().on("cxttap", showNodeModal)
    })
  }

  const drawGraph = () => {
    if (!cyGraph) cyGraph = createGraph(graphContainer, elements)
    else {
      cyGraph.json({ elements: elements })
      cyGraph.elements().layout(LAYOUT_OPTIONS).run()
    }

    registerTippy(cyGraph)
    registerModal(cyGraph)
  }

  $: if (elements && graphContainer) {
    drawGraph()
  }
</script>

<!--{JSON.stringify(elements)}-->
<div class="h-[800px]">
  <div
    bind:this={graphContainer}
    class="min-h-full w-full cursor-all-scroll border-2 border-solid"
  />
</div>

<div class="flex flex-row bg-white dark:bg-gray-700">
  {#if !hideControls}
    <div class="basis-1/2 p-2">
      <div class="pb-3">
        <label for="investor-level">
          <strong>{$_("Involvements graph depth")}</strong>
        </label>
        <div class="w-1/2">
          <input
            bind:value={depth}
            id="investor-level"
            type="range"
            min="1"
            max={max_depth}
            on:change={fetchInvolvments}
            disabled={$loading}
          />
          {depth}
        </div>
        {#if reachedMaxDepth && depth === max_depth}
          You've reached max depth, the graph is not going to get any bigger
        {/if}
      </div>

      <div>
        <label class="pr-3">
          <input
            bind:checked={showDeals}
            disabled={$loading}
            type="checkbox"
            on:change={fetchInvolvments}
          />
          <strong>{$_("Show deals")}</strong>
        </label>
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

<style lang="postcss">
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
