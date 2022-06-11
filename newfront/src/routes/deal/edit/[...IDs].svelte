<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { get } from "svelte/store";
  import { client } from "$lib/apolloClient";
  import type { Deal } from "$lib/types/deal";
  import { deal_gql_query } from "../queries";

  export const load: Load = async ({ params }) => {
    let [dealID, dealVersion] = params.IDs.split("/").map((x) => (x ? +x : undefined));

    const { data } = await get(client).query<{ deal: Deal[] }>({
      query: deal_gql_query,
      variables: { id: +dealID, version: dealVersion },
    });
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
