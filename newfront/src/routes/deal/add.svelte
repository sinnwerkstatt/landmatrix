<script lang="ts" context="module">
  import type { Load } from "@sveltejs/kit";

  export const load: Load = async ({ stuff }) => {
    if (!stuff.user) return { status: 403, error: "Permission denied" };
    return {};
  };
</script>

<script lang="ts">
  import DealEditForm from "$views/DealEditForm.svelte";
  import type { Deal } from "$lib/types/deal";

  let deal: Deal = { id: -1, contracts: [], datasources: [], locations: [] } as Deal;
  let dealID;
  let dealVersion;
</script>

<DealEditForm bind:deal bind:dealID bind:dealVersion />
