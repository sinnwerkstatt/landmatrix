<script lang="ts">
  import {
    ArcElement,
    CategoryScale,
    Chart as ChartJS,
    Legend,
    Title,
    Tooltip,
  } from "chart.js";
  import { Pie } from "svelte-chartjs";

  ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);

  export let data;
  export let unit = "";
</script>

<Pie
  {data}
  options={{
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
    },
  }}
/>
