<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import type { ElementDefinition, EventHandler, Core as Graph } from "cytoscape"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { loading } from "$lib/stores/basics"

  import DealDetailModal from "./DealDetailModal.svelte"
  import InvestorDetailModal from "./InvestorDetailModal.svelte"
  import { createGraph, LAYOUT_OPTIONS, registerTippy } from "./investorGraphNew"

  interface Props {
    investorID: number | null
    hideControls?: boolean
    skipVentures?: boolean
  }

  let { investorID, hideControls = false, skipVentures = false }: Props = $props()
  let showDeals = $state(true)

  let cyGraph: Graph
  let graphContainer: HTMLDivElement | undefined = $state()
  let modalData: { dealNode?: boolean } = $state({})
  let showInvestorModal = $state(false)
  let showDealModal = $state(false)

  let depth = $state(3)
  let max_depth = $state(30)
  let reachedMaxDepth = $state(false)

  let elements: ElementDefinition[] = $state([])

  async function fetchInvolvments() {
    loading.set(true)
    const ret = await fetch(
      `/api/investors/${investorID}/involvements_graph/?depth=${depth}&include_deals=${showDeals}&show_ventures=${!skipVentures}`,
    )
    // using 418-Teapot, because fetch goes into auto-retry mode
    // on 408 (request timeout), which ought to be the correct response here 🙄
    if (ret.status === 418) {
      loading.set(false)
      toast.push("We timed out on this request. Try a smaller graph", {
        classes: ["error"],
      })
      return
    }

    const retJson = await ret.json()

    elements = retJson.elements
    if (retJson.full_depth) {
      reachedMaxDepth = true
      max_depth = retJson.full_depth
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

  $effect(() => {
    if (elements && graphContainer) {
      drawGraph()
    }
  })
</script>

<div class={skipVentures ? "h-[400px]" : "h-[600px]"}>
  <div
    bind:this={graphContainer}
    class="min-h-full w-full cursor-all-scroll border-2 border-solid"
  ></div>
</div>

<div class="flex bg-white py-3 dark:bg-gray-700">
  {#if !hideControls}
    <div class="basis-1/2">
      <div class="pb-3">
        <label for="investor-level">
          <strong>
            {$_("Involvements graph depth")}:
            <span class="text-lg">{depth}</span>
          </strong>
        </label>
        <div class="w-1/2">
          <input
            bind:value={depth}
            id="investor-level"
            type="range"
            min="1"
            max={max_depth}
            onchange={fetchInvolvments}
            disabled={$loading}
            class="w-full"
          />
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
            onchange={fetchInvolvments}
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
        <span class="colored-line" style:--color="rgba(252,148,30,1)"></span>
        {$_("Is operating company of")}
      </li>
      <li>
        <span class="colored-arrow" style:--color="rgba(234,128,121,1)"></span>
        {$_("Is parent company of")}
      </li>
      <li>
        <span class="colored-arrow" style:--color="rgba(133,146,238,1)"></span>
        {$_("Is tertiary investor/lender of")}
      </li>
    </ul>
  </div>
</div>

<InvestorDetailModal
  visible={showInvestorModal}
  investor={modalData}
  onclose={() => (showInvestorModal = false)}
/>

<DealDetailModal
  visible={showDealModal}
  deal={modalData}
  onclose={() => (showDealModal = false)}
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
</style>
