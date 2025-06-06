<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import type { BaseType, HierarchyNode } from "d3"
  import { format, hierarchy, select, treemap, treemapSquarify } from "d3"
  import { onDestroy } from "svelte"
  import { _ } from "svelte-i18n"

  import type { BucketMap } from "$lib/data/buckets"
  import { createBucketMapReducer, sortBuckets } from "$lib/data/buckets"
  import { createLabels, dealChoices } from "$lib/fieldChoices"
  import {
    ProduceGroup,
    type Animals,
    type Crops,
    type DealVersion,
    type Minerals,
    type Produce,
  } from "$lib/types/data"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    downloadCSV,
    downloadJSON,
    downloadSVG,
    type FileType,
  } from "$components/Data/Charts/utils"
  import { showContextBar, showFilterBar } from "$components/Data/stores"

  interface ProduceAccumulator {
    crops: BucketMap<Crops>
    animals: BucketMap<Animals>
    mineralResources: BucketMap<Minerals>
  }

  interface TreeNode {
    name: string
    value: number
  }

  interface ProduceTreeData {
    name: string
    children: {
      name: string
      color: string
      children: TreeNode[]
    }[]
  }

  interface Props {
    deals?: DealVersion[]
    title: string
  }

  let { deals = [], title }: Props = $props()

  let svgComp: SVGElement | undefined = $state()

  const SIZE_THRESHOLD = 0.005

  const labels = $derived({
    ...createLabels<Crops>($dealChoices.crops),
    ...createLabels<Animals>($dealChoices.animals),
    ...createLabels<Minerals>($dealChoices.minerals),
  })

  // TODO Later not correct to add full deal size for each produce
  const produceReducer = (
    acc: ProduceAccumulator,
    deal: DealVersion,
  ): ProduceAccumulator => {
    const bucketMapReducer = createBucketMapReducer(deal.deal_size ?? 0)
    return {
      crops: (deal.current_crops ?? []).reduce(bucketMapReducer, acc.crops),
      animals: (deal.current_animals ?? []).reduce(bucketMapReducer, acc.animals),
      mineralResources: (deal.current_mineral_resources ?? []).reduce(
        bucketMapReducer,
        acc.mineralResources,
      ),
    }
  }

  const produceGroupLabels = $derived(
    createLabels<ProduceGroup>($dealChoices.produce_group),
  )

  const createTreeData = (deals: DealVersion[]): ProduceTreeData => {
    const acc = deals.reduce(produceReducer, {} as ProduceAccumulator)

    const root: ProduceTreeData = { name: $_("Produce"), children: [] }
    if (acc.crops)
      root.children.push({
        name: produceGroupLabels[ProduceGroup.CROPS],
        color: "#FC941F",
        children: createChildren(acc.crops),
      })
    if (acc.animals)
      root.children.push({
        name: produceGroupLabels[ProduceGroup.ANIMALS],
        color: "#7D4A0F",
        children: createChildren(acc.animals),
      })
    if (acc.mineralResources)
      root.children.push({
        name: produceGroupLabels[ProduceGroup.MINERAL_RESOURCES],
        color: "black",
        children: createChildren(acc.mineralResources),
      })

    return root
  }

  const createChildren = <T extends Produce>(bucketMap: BucketMap<T>): TreeNode[] => {
    const [keys, buckets] = sortBuckets("size", bucketMap)
    const totalSize = buckets.reduce((sum, bucket) => sum + bucket.size, 0)
    const thresholdIndex = buckets.findIndex(
      bucket => bucket.size < totalSize * SIZE_THRESHOLD,
    )
    const otherSize = buckets
      .slice(thresholdIndex)
      .reduce((sum, bucket) => sum + bucket.size, 0)

    const namedChildren = keys.slice(0, thresholdIndex).map(key => ({
      name: labels[key],
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
  const treeData = $derived(createTreeData(deals))

  const buildTreeChart = (treeData: ProduceTreeData): void => {
    if (!treeData) return

    let count = 0
    const domUid = (name: string) => `O-${name}-${++count}`
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
      .attr("fill", "currentColor")
      .attr("clip-path", d => d.clipUid)
      .selectAll("tspan")
      .data(d =>
        d.data.name
          .split(/(?=[A-Z][a-z]\(\) )\s+/g)
          .concat(
            `${Math.round(d.data.value).toLocaleString("fr").replace(",", ".")} ${$_("ha")}`,
          ),
      )
      .join("tspan")
      .attr("x", 2)
      .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
      .attr("fill-opacity", (d, i, nodes) => (i === nodes.length - 1 ? 0.7 : null))
      .text((d: string) => d)
  }

  $effect(() => {
    buildTreeChart(treeData)
  })

  const asCsv = (treeData: ProduceTreeData): string => {
    const csvHeader = "Produce Name,Total Deal Size (ha)\n"
    const csvData = treeData.children
      .map(group =>
        group.children.map(({ name, value }) => `"${name}",${value}`).join("\n"),
      )
      .join("\n")
    return csvHeader + csvData
  }

  const handleDownload = (fileType: FileType) => {
    if ($tracker) $tracker.trackEvent("Chart", "Produce info map", fileType)
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(treeData, null, 2), title)
      case "csv":
        return downloadCSV(asCsv(treeData), title)
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }

  // react on screen changes
  const unsubCtxBarTrigger = showContextBar.subscribe(() => buildTreeChart(treeData))
  const unsubFltrBarTrigger = showFilterBar.subscribe(() => buildTreeChart(treeData))

  onDestroy(() => {
    unsubCtxBarTrigger()
    unsubFltrBarTrigger()
  })
</script>

<ChartWrapper ondownload={handleDownload} {title} wrapperClasses="mx-auto w-full">
  <svg bind:this={svgComp} id="produce-info-map" />
</ChartWrapper>
