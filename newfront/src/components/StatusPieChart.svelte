<script lang="ts">
  import {
    ArcElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    Title,
    Tooltip,
  } from "chart.js";
  import type { ChartData, ChartOptions } from "chart.js";
  import { Pie } from "svelte-chartjs";

  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

  export let data: ChartData;
  export let unit = "";

  const options: ChartOptions<"pie"> = {
    responsive: true,
    aspectRatio: 1,
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => {
            let ret = `${context.label}: `;
            ret += Math.round(context.dataset.data[context.dataIndex]).toLocaleString(
              "fr"
            );
            if (unit) ret += ` ${unit}`;
            return ret;
          },
        },
      },
      legend: {
        position: "bottom",
      },
    },
  };
</script>

<!--svelte plugin for IntelliJ cannot index props for SvelteComponentTyped-->
<!--https://github.com/tomblachut/svelte-intellij/issues/206-->
<Pie {data} {options} />
