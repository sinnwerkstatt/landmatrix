<script lang="ts">
  import { format, hierarchy, select, selectAll, treemap, treemapSquarify } from "d3"
  import type { BaseType, HierarchyNode } from "d3"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import type { BucketMap } from "$lib/data/buckets"
  import { createBucketMapReducer, sortBuckets } from "$lib/data/buckets"
  import { formfields } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"

  import { showContextBar, showFilterBar } from "$components/Data"

  export let deals: Deal[] = []

  const SIZE_THRESHOLD = 0.005

  $: keyMap = {
    ...$formfields.deal["crops"].choices,
    ...$formfields.deal["animals"].choices,
    ...$formfields.deal["mineral_resources"].choices,
  }

  interface ProduceAccumulator {
    crops: BucketMap
    animals: BucketMap
    mineralResources: BucketMap
  }

  interface ProduceTreeData {
    name: string
    children: { name: string; value: number }[]
  }

  // TODO: not correct to add full deal size for each produce
  const produceReducer = (acc: ProduceAccumulator, deal: Deal): ProduceAccumulator => {
    const bucketMapReducer = createBucketMapReducer(deal.deal_size)
    return {
      crops: (deal.current_crops ?? []).reduce(bucketMapReducer, acc.crops),
      animals: (deal.current_animals ?? []).reduce(bucketMapReducer, acc.animals),
      mineralResources: (deal.current_mineral_resources ?? []).reduce(
        bucketMapReducer,
        acc.mineralResources,
      ),
    }
  }

  const createTreeData = (deals: Deal[]): ProduceTreeData => {
    const acc = deals.reduce(produceReducer, {} as ProduceAccumulator)

    const root = { name: "Produce", children: [] }
    if (acc.crops)
      root.children.push({
        name: $_("Crops"),
        color: "#FC941F",
        children: createChildren(acc.crops),
      })
    if (acc.animals)
      root.children.push({
        name: $_("Livestock"),
        color: "#7D4A0F",
        children: createChildren(acc.animals),
      })
    if (acc.mineralResources)
      root.children.push({
        name: $_("Mineral Resources"),
        color: "black",
        children: createChildren(acc.mineralResources),
      })

    return root
  }

  const createChildren = (bucketMap: BucketMap): ProduceTreeData["children"] => {
    const [keys, buckets] = sortBuckets("size", bucketMap)
    const totalSize = buckets.reduce((sum, bucket) => sum + bucket.size, 0)
    const thresholdIndex = buckets.findIndex(
      bucket => bucket.size < totalSize * SIZE_THRESHOLD,
    )
    const otherSize = buckets
      .slice(thresholdIndex)
      .reduce((sum, bucket) => sum + bucket.size, 0)

    const namedChildren = keys.slice(0, thresholdIndex).map(key => ({
      name: $_(keyMap[key]),
      value: bucketMap[key].size,
    }))
    return [
      ...namedChildren,
      {
        name: $_("Other"),
        value: otherSize,
      },
    ]
  }

  const buildTreeChart = (treeData: ProduceTreeData): void => {
    if (!treeData) return
    let count = 0
    const domUid = name => `O-${name}-${++count}`
    const myFormat = format(",d")

    const container = document.getElementById("produce-info")
    if (!container) return

    const width = container.offsetWidth
    const height = container.offsetHeight

    // reset first!
    selectAll("#produce-info > svg > *").remove()

    const svg = select<BaseType, ProduceTreeData>("#produce-info > svg")
      .attr("viewBox", [0, 0, width, height])
      .append("svg:g")
      .attr("transform", "translate(.5,.5)")

    // format data
    const root = hierarchy(treeData).sum(d => d.value)

    // initialize graph
    const myTreemap = treemap()
      .tile(treemapSquarify)
      .size([width, height])
      .round(true)
      .paddingInner(2)
      .padding(2)

    // load data
    myTreemap(root)

    // get all leaves
    const leaf = svg
      .selectAll("g")
      .data(root.leaves())
      .join("g")
      .attr("transform", d => `translate(${d.x0},${d.y0})`)

    // tooltips
    leaf.append("title").text(d => `${d.data.name}\n${myFormat(d.value as number)}`)

    // colored squares
    leaf
      .append("rect")
      .attr("id", d => (d.leafUid = domUid("leaf")).id)
      .attr("fill", d => {
        while (d.depth > 1) d = d.parent as HierarchyNode<ProduceTreeData>
        return d.data.color
      })
      .attr("fill-opacity", 0.6)
      .attr("width", d => d.x1 - d.x0)
      .attr("height", d => d.y1 - d.y0)

    // mask for each rect
    leaf
      .append("clipPath")
      .attr("id", d => (d.clipUid = domUid("clip")).id)
      .append("use")

      .attr("xlink:href", d => d.leafUid.href)

    // text that is masked (to avoid text overflow)
    leaf
      .append("text")
      .attr("clip-path", d => d.clipUid)
      .selectAll("tspan")
      .data(d =>
        d.data.name
          .split(/(?=[A-Z][a-z]\(\) )\s+/g)
          .concat(`${Math.round(d.data.value).toLocaleString("fr")} ha`),
      )
      .join("tspan")
      .attr("x", 2)
      .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
      .attr("fill-opacity", (d, i, nodes) => (i === nodes.length - 1 ? 0.7 : null))
      .text((d: string) => d)
  }

  $: treeData = createTreeData(deals)
  $: {
    // react on screen changes
    $showContextBar || $showFilterBar
    buildTreeChart(treeData)
  }
  onMount(() => buildTreeChart(treeData))
</script>

<div id="produce-info" class="h-full w-full">
  <svg />
</div>
