<script lang="ts">
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import { classification_choices } from "$lib/choices"
  import type { Deal } from "$lib/types/deal"

  import { a_download, fileName } from "../utils"
  import CountryProfileChartWrapper from "./CountryProfileChartWrapper.svelte"
  import { dynamics_csv, DynamicsOfDeal } from "./dynamics_of_deal"
  import type { DynamicsDataPoint } from "./dynamics_of_deal"

  const title = $_("Dynamics of deal by investor type")
  const svg = new DynamicsOfDeal()

  export let deals: Deal[] = []

  let multideals = 0
  let payload: DynamicsDataPoint[] = []

  $: if (browser && deals?.length > 0) {
    let pots: { [key: string]: number } = {}
    deals.forEach(d => {
      if (d.top_investors.length > 1) multideals += 1
      d.top_investors.forEach(i => {
        const cl = i.classification
        pots[cl] = pots[cl]
          ? pots[cl] + d.current_contract_size
          : d.current_contract_size
      })
    })

    payload = Object.entries(pots).map(([k, v]) => ({
      name: $_(classification_choices[k]) || $_("Unknown"),
      value: v,
    }))

    svg.do_the_graph("#dynamicsofdeal", payload)
  }

  function downloadJSON() {
    let data =
      "data:application/json;charset=utf-8," +
      encodeURIComponent(JSON.stringify(payload, null, 2))
    a_download(data, fileName(title, ".json"))
  }
  function downloadCSV() {
    const csv = dynamics_csv(payload)
    let data = "data:text/csv;charset=utf-8," + encodeURIComponent(csv)
    a_download(data, fileName(title, ".csv"))
  }
</script>

<CountryProfileChartWrapper
  svgID="dynamicsofdeal"
  {title}
  on:downloadJSON={downloadJSON}
  on:downloadCSV={downloadCSV}
>
  <svg id="dynamicsofdeal" />

  <div slot="legend">
    {$_(
      "Please note: {number} deals have multiple investor types. The full size of the deal is assigned to each investor type.",
      { values: { number: multideals } },
    )}
  </div>
</CountryProfileChartWrapper>
