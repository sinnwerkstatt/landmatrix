<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { _ } from "svelte-i18n"

  import {
    LamaSankey,
    sankey_links_to_csv_cross,
  } from "$lib/data/charts/intentionsPerCategory"
  import type {
    MySankeyLink,
    MySankeyNode,
  } from "$lib/data/charts/intentionsPerCategory"
  import { createLabels, fieldChoices } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/data"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import {
    downloadCSV,
    downloadJSON,
    downloadSVG,
    type FileType,
  } from "$components/Data/Charts/utils"

  let title = $derived(
    $_(
      "Number of intentions per category of production according to implementation status",
    ),
  )

  interface Props {
    deals?: DealVersion2[]
  }

  let { deals = [] }: Props = $props()

  let svgComp: SVGElement | undefined = $state()
  let sankey_links: MySankeyLink[] = $state([])
  let sankey = new LamaSankey()
  let sankeyLegendNumbers: { x: number; y: number; z: number } | undefined = $derived(
    deals?.length
      ? {
          x: deals.filter(d => d.current_intention_of_investment?.length > 1).length,
          y: deals
            .map(d => d.current_intention_of_investment?.length || 0)
            .reduce((a, b) => a + b, 0),
          z: deals.length,
        }
      : undefined,
  )

  let ioiLabels = $derived(createLabels($fieldChoices.deal.intention_of_investment))

  let impStatLabels = $derived(createLabels($fieldChoices.deal.implementation_status))

  let nodesAndLinks = $derived.by(() => {
    let datanodes: Set<string> = new Set()
    let datalinks: { [key: string]: number } = {}
    let i_status_counter: { [key: string]: number } = {}
    deals.forEach(d => {
      const i_stat = d.current_implementation_status ?? "S_UNKNOWN"
      const ivis = d.current_intention_of_investment ?? ["I_UNKNOWN"]

      datanodes.add(i_stat)
      i_status_counter[i_stat] = i_status_counter[i_stat] + 1 || 1

      ivis.forEach(ivi => {
        datanodes.add(ivi)
        datalinks[`${i_stat},${ivi}`] = datalinks[`${i_stat},${ivi}`] + 1 || 1
      })
    })
    let nodes: MySankeyNode[] = [...datanodes].map(n => {
      const istatus = impStatLabels[n] || n === "S_UNKNOWN"
      const deal_count = istatus ? i_status_counter[n] : 0
      const name =
        (n === "S_UNKNOWN" && $_("Status unknown")) ||
        (n === "I_UNKNOWN" && $_("Intention unknown")) ||
        impStatLabels[n] ||
        ioiLabels[n]
      return { id: n, istatus, deal_count, name }
    })
    let links: MySankeyLink[] = Object.entries(datalinks).map(([k, v]) => {
      const [source, target] = k.split(",")
      return { source, target, value: v }
    })
    return [nodes, links]
  })

  $effect(() => {
    const [nodes, links] = nodesAndLinks
    sankey_links = JSON.parse(JSON.stringify(links))
    sankey.do_the_sank(svgComp, { nodes, links })
  })

  const handleDownload = (fileType: FileType) => {
    if ($tracker) $tracker.trackEvent("Chart", "Intentions per category", fileType)
    switch (fileType) {
      case "json":
        return downloadJSON(JSON.stringify(sankey_links, null, 2), title)
      case "csv":
        return downloadCSV(sankey_links_to_csv_cross(sankey_links), title)
      default:
        return downloadSVG(svgComp, fileType, title)
    }
  }
</script>

<ChartWrapper ondownload={handleDownload} {title}>
  <svg bind:this={svgComp} id="sankey-chart" />

  {#snippet legend()}
    <div>
      {$_("This figure lists the intention of investments per negotiation status.")}
      <br />
      {$_("Please note: a deal may have more than one intention.")}
      <br />
      {#if sankeyLegendNumbers}
        <i>
          {$_(
            "{x} deals have multiple intentions, resulting in a total of {y} intentions for {z} deals.",
            { values: sankeyLegendNumbers },
          )}
        </i>
      {/if}
    </div>
  {/snippet}
</ChartWrapper>

<style>
  :global(#sankey .link:hover) {
    stroke-opacity: 0.9;
  }
</style>
