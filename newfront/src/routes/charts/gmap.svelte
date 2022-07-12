<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";
  import { showContextBar } from "$components/Data";

  export const load: Load = async () => {
    // showContextBar.set(true);
    return {};
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import ChartsContainer from "$components/Data/Charts/ChartsContainer.svelte";
  import GlobalMapOfInvestments from "$components/Data/Charts/GlobalMapOfInvestments.svelte";
</script>

<svelte:head>
  <title>{$_("Global Map of Investments | Land Matrix")}</title>
</svelte:head>

<GlobalMapOfInvestments />
