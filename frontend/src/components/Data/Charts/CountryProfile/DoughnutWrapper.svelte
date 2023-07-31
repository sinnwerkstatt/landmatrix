<script lang="ts">
  import type { Chart, ChartData, ChartOptions } from "chart.js"
  import { Doughnut } from "svelte-chartjs?client"

  interface Item<Key extends string = string> {
    key: Key
    value: number
    label: string
  }

  export let data: ChartData<"doughnut", Item[]>
  export let options: ChartOptions<"doughnut">

  const initialData = data

  $: if (chart) {
    chart.data.labels = data.labels
    data.datasets.forEach((ds, index) => {
      chart.data.datasets[index].data = ds.data
      chart.data.datasets[index].backgroundColor = ds.backgroundColor
    })
    chart.update()
  }

  let chart: Chart<"doughnut", Item[]>
</script>

<Doughnut bind:chart data={initialData} {options} />
