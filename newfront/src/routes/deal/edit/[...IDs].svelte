<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { deal_gql_query } from "$lib/deal_queries";
  import type { Deal } from "$lib/types/deal";

  export const load: Load = async ({ params, stuff }) => {
    if (!stuff.user) return { status: 403, error: "Permission denied" };

    let [dealID, dealVersion] = params.IDs.split("/").map((x) => (x ? +x : undefined));
    const { data } = await stuff.urqlClient
      .query<{ deal: Deal[] }>(deal_gql_query, { id: dealID, version: dealVersion })
      .toPromise();
    if (data.deal === null)
      return {
        status: 404,
        error: dealVersion ? "Deal version not found" : "Deal not found",
      };

    return {
      props: { dealID, dealVersion, deal: JSON.parse(JSON.stringify(data.deal)) },
    };
  };
</script>

<script lang="ts">
  import DealEditForm from "$views/DealEditForm.svelte";

  export let deal: Deal;
  export let dealID: number;
  export let dealVersion: number;
</script>

<DealEditForm bind:deal bind:dealID bind:dealVersion />
