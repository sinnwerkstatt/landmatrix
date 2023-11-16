<script lang="ts">
  import { format, hierarchy, select, treemap, treemapSquarify } from "d3"
  import type { BaseType, HierarchyNode } from "d3"
  import { afterUpdate, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import type { BucketMap } from "$lib/data/buckets"
  import { createBucketMapReducer, sortBuckets } from "$lib/data/buckets"
  import { formfields } from "$lib/stores"
  import type { Deal } from "$lib/types/deal"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"
  import { showContextBar, showFilterBar } from "$components/Data/stores"

  export let deals: Deal[] = []
  export let title: string

  let svgComp: SVGElement

  const SIZE_THRESHOLD = 0.005

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const asKeyMap = (array: { value: any; label: string }[] | undefined) =>
    array
      ? array.reduce((acc, { value, label }) => ({ ...acc, [value]: label }), {})
      : {}

  $: keyMap = {
    ...asKeyMap($formfields.deal["crops"].choices),
    ...asKeyMap($formfields.deal["animals"].choices),
    ...asKeyMap($formfields.deal["mineral_resources"].choices),
  }

  interface ProduceAccumulator {
    crops: BucketMap
    animals: BucketMap
    mineralResources: BucketMap
  }

  interface ProduceTreeData {
    name: string
    children: {
      name: string
      color: string
      children: { name: string; value: number }[]
    }[]
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
        name: $_("Mineral resources"),
        color: "black",
        children: createChildren(acc.mineralResources),
      })

    return root
  }

  const createChildren = (
    bucketMap: BucketMap,
  ): ProduceTreeData["children"]["children"] => {
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

    const width = 800
    const height = 500

    // reset first!
    select(svgComp).selectAll("*").remove()

    const svg = select<BaseType, ProduceTreeData>(svgComp)
      .attr("viewBox", [0, 0, width, height])
      .attr("height", "100%")
      .attr("width", "100%")
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
  afterUpdate(() => buildTreeChart(treeData))

  const asCsv = (treeData: ProduceTreeData): string => {
    const csvHeader = "Produce Name,Total Deal Size (ha)\n"
    const csvData = treeData.children
      .map(group =>
        group.children.map(({ name, value }) => `"${name}",${value}`).join("\n"),
      )
      .join("\n")
    return csvHeader + csvData
  }

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(treeData, null, 2), title)
      case "csv":
        return downloadCSV(asCsv(treeData), title)
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }
</script>

<ChartWrapper {title} wrapperClasses="mx-auto w-full" on:download={handleDownload}>
  <svg id="produce-info-map" bind:this={svgComp} />
</ChartWrapper>
