<script lang="ts">
  import type { ChartData, ChartOptions } from "chart.js"
  import {
    ArcElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    Title,
    Tooltip,
  } from "chart.js?client"
  import { Pie } from "svelte-chartjs?client"

  import { isDarkMode } from "$lib/stores/basics"

  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

  export let data: ChartData
  export let unit = ""
  export let chart: ChartJS | undefined = undefined

  isDarkMode.subscribe(v => {
    ChartJS.defaults.color = v ? "#ffffff" : "#000000"
    if (chart) chart?.update()
  })

  $: totals = data.datasets.map(dSet => dSet.data.reduce((sum, value) => sum + value))

  let options: ChartOptions<"pie">
  $: options = {
    responsive: true,
    aspectRatio: 1,
    plugins: {
      tooltip: {
        callbacks: {
          label: context => {
            const value = context.dataset.data[context.dataIndex]
            const percentage = (value / totals[context.datasetIndex]) * 100

            let ret = `${context.label}: `
            ret += Math.round(value).toLocaleString("fr").replace(",", ".")
            if (unit) ret += ` ${unit}`
            ret += " (" + percentage.toFixed(0) + "%)"
            return ret
          },
        },
      },
      legend: {
        maxHeight: 50,
        position: "bottom",
      },
    },
  }
</script>

<!--svelte plugin for IntelliJ cannot index props for SvelteComponentTyped-->
<!--https://github.com/tomblachut/svelte-intellij/issues/206-->
<Pie bind:chart {data} {options} />
