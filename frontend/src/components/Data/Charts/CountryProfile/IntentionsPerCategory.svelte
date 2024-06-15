<script lang="ts">
  import { tracker } from "@sinnwerkstatt/sveltekit-matomo"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import {
    LamaSankey,
    sankey_links_to_csv_cross,
  } from "$lib/data/charts/intentionsPerCategory"
  import type {
    MySankeyLink,
    MySankeyNode,
  } from "$lib/data/charts/intentionsPerCategory"
  import { fieldChoices, getFieldChoicesLabel } from "$lib/stores"
  import type { DealVersion2 } from "$lib/types/data"

  import ChartWrapper from "$components/Data/Charts/DownloadWrapper.svelte"
  import { downloadCSV, downloadJSON, downloadSVG } from "$components/Data/Charts/utils"
  import type { DownloadEvent } from "$components/Data/Charts/utils"

  $: title = $_(
    "Number of intentions per category of production according to implementation status",
  )

  export let deals: DealVersion2[] = []

  let svgComp: SVGElement

  let sankey_links: MySankeyLink[] = []
  let sankey = new LamaSankey()
  let sankey_legend_numbers: { x: number; y: number; z: number }

  $: if (deals?.length > 0) {
    sankey_legend_numbers = {
      x: deals.filter(d => d.current_intention_of_investment?.length > 1).length,
      y: deals
        .map(d => d.current_intention_of_investment?.length || 0)
        .reduce((a, b) => a + b, 0),
      z: deals.length,
    }
  }

  let nodes: MySankeyNode[] = []
  let links: MySankeyLink[] = []

  $: getIoILabel = getFieldChoicesLabel(
    $fieldChoices["deal"]["intention_of_investment"],
  )
  $: getStatusLabel = getFieldChoicesLabel(
    $fieldChoices["deal"]["implementation_status"],
  )

  $: if (browser && deals?.length > 0) {
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
    nodes = [...datanodes].map(n => {
      const istatus = getStatusLabel(n) || n === "S_UNKNOWN"
      const deal_count = istatus ? i_status_counter[n] : 0
      const name =
        (n === "S_UNKNOWN" && $_("Status unknown")) ||
        (n === "I_UNKNOWN" && $_("Intention unknown")) ||
        getStatusLabel(n) ||
        getIoILabel(n)
      return { id: n, istatus, deal_count, name }
    })
    links = Object.entries(datalinks).map(([k, v]) => {
      const [source, target] = k.split(",")
      return { source, target, value: v }
    })
    sankey_links = JSON.parse(JSON.stringify(links))
    sankey.do_the_sank(svgComp, { nodes, links })
  }

  const handleDownload = ({ detail: fileType }: DownloadEvent) => {
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

  onMount(() => sankey.do_the_sank(svgComp, { nodes, links }))
</script>

<ChartWrapper {title} on:download={handleDownload}>
  <svg id="sankey-chart" bind:this={svgComp} />

  <div slot="legend">
    {$_("This figure lists the intention of investments per negotiation status.")}
    <br />
    {$_("Please note: a deal may have more than one intention.")}
    <br />
    {#if sankey_legend_numbers}
      <i>
        {$_(
          "{x} deals have multiple intentions, resulting in a total of {y} intentions for {z} deals.",
          { values: sankey_legend_numbers },
        )}
      </i>
    {/if}
  </div>
</ChartWrapper>

<style>
  :global(#sankey .link:hover) {
    stroke-opacity: 0.9;
  }
</style>
