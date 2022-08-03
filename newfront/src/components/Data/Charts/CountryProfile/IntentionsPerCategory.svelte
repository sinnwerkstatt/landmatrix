<script lang="ts">
  import { _ } from "svelte-i18n";
  import { browser } from "$app/env";
  import type { Deal } from "$lib/types/deal";
  import {
    flat_intention_of_investment_map,
    implementation_status_choices,
  } from "$components/Fields/Display/choices";
  import { a_download, fileName } from "../utils";
  import CountryProfileChartWrapper from "./CountryProfileChartWrapper.svelte";
  import { LamaSankey, sankey_links_to_csv_cross } from "./intentions_per_category";

  const title = $_(
    "Number of intentions per category of production according to implementation status"
  );

  export let deals: Deal[] = [];

  let sankey_links = [];
  let sankey = new LamaSankey();
  let sankey_legend_numbers;

  const downloadJSON = async () => {
    let data =
      "data:application/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(sankey_links, null, 2));
    a_download(data, fileName(title, ".json"));
  };
  const downloadCSV = async () => {
    const csv = sankey_links_to_csv_cross(sankey_links);
    let data = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
    a_download(data, fileName(title, ".csv"));
  };

  $: if (deals?.length > 0) {
    sankey_legend_numbers = {
      x: deals.filter((d) => d.current_intention_of_investment?.length > 1).length,
      y: deals
        .map((d) => d.current_intention_of_investment?.length || 0)
        .reduce((a, b) => a + b, 0),
      z: deals.length,
    };
  }

  $: if (browser && deals.length > 0) {
    let datanodes: Set<string> = new Set();
    let datalinks: { [key: string]: number } = {};
    let i_status_counter: { [key: string]: number } = {};
    deals.forEach((d) => {
      const i_stat = d.current_implementation_status ?? "S_UNKNOWN";
      const ivis = d.current_intention_of_investment ?? ["I_UNKNOWN"];

      datanodes.add(i_stat);
      i_status_counter[i_stat] = i_status_counter[i_stat] + 1 || 1;

      ivis.forEach((ivi) => {
        datanodes.add(ivi);
        datalinks[`${i_stat},${ivi}`] = datalinks[`${i_stat},${ivi}`] + 1 || 1;
      });
    });
    const nodes = [...datanodes].map((n) => {
      const istatus = implementation_status_choices[n] || n === "S_UNKNOWN";
      const deal_count = istatus ? i_status_counter[n] : 0;
      const name = $_(
        (n === "S_UNKNOWN" && "Status unknown") ||
          (n === "I_UNKNOWN" && "Intention unknown") ||
          implementation_status_choices[n] ||
          flat_intention_of_investment_map[n]
      );

      return { id: n, istatus, deal_count, name };
    });
    const links = Object.entries(datalinks).map(([k, v]) => {
      let [source, target] = k.split(",");
      return { source, target, value: v };
    });
    sankey_links = JSON.parse(JSON.stringify(links));
    if (sankey) sankey.do_the_sank("#sankey", { nodes, links });
  }
</script>

<CountryProfileChartWrapper
  svgID="sankey"
  {title}
  on:downloadJSON={downloadJSON}
  on:downloadCSV={downloadCSV}
>
  <svg id="sankey" />

  <div slot="legend">
    {$_("This figure lists the intention of investments per negotiation status.")}
    <br />
    {$_("Please note: a deal may have more than one intention.")}<br />
    {#if sankey_legend_numbers}
      <i>
        {$_(
          "{x} deals have multiple intentions, resulting in a total of {y} intentions for {z} deals.",
          { values: sankey_legend_numbers }
        )}
      </i>
    {/if}
  </div>
</CountryProfileChartWrapper>

<style>
  :global(#sankey .link:hover) {
    stroke-opacity: 0.9;
  }
</style>
