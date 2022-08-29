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
  import { _ } from "svelte-i18n"

  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale)

  export let data: ChartData<"pie", number[], string>
  export let unit = ""

  $: totals = data.datasets.map(dSet => dSet.data.reduce((sum, value) => sum + value))
  let i18nData: ChartData<"pie", number[], string>
  // TODO Marcus: refactor $_(label) up to the source
  $: i18nData = { ...data, labels: data.labels?.map(label => $_(label)) }

  const options: ChartOptions<"pie"> = {
    responsive: true,
    aspectRatio: 1,
    plugins: {
      tooltip: {
        callbacks: {
          label: context => {
            const value = context.dataset.data[context.dataIndex]
            const percentage = (value / totals[context.datasetIndex]) * 100

            let ret = `${context.label}: `
            ret += Math.round(value).toLocaleString("fr")
            if (unit) ret += ` ${unit}`
            ret += " (" + percentage.toFixed(0) + "%)"
            return ret
          },
        },
      },
      legend: {
        position: "bottom",
      },
    },
  }
</script>

<!--svelte plugin for IntelliJ cannot index props for SvelteComponentTyped-->
<!--https://github.com/tomblachut/svelte-intellij/issues/206-->
<Pie data={i18nData} {options} />
