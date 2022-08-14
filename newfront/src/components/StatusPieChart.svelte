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
  import { _ } from "svelte-i18n";

  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

  export let data: ChartData<"pie", number[], string>;
  export let unit = "";

  let i18nData: ChartData<"pie", number[], string>;
  $: i18nData = { ...data, labels: data.labels?.map((label) => $_(label)) };

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
<Pie data={i18nData} {options} />
