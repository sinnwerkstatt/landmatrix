<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { investor_gql_query } from "$lib/investor_queries";
  import type { Investor } from "$lib/types/investor";

  export const load: Load = async ({ params, stuff }) => {
    if (!stuff.user) return { status: 403, error: "Permission denied" };

    let [investorID, investorVersion] = params.IDs.split("/").map((x) =>
      x ? +x : undefined
    );
    const { data } = await stuff.urqlClient
      .query<{ investor: Investor[] }>(investor_gql_query, {
        id: investorID,
        version: investorVersion,
        depth: 0,
        includeDeals: false,
      })
      .toPromise();
    if (data.investor === null)
      return {
        status: 404,
        error: investorVersion ? "Investor version not found" : "Investor not found",
      };

    return {
      props: {
        investorID,
        investorVersion,
        investor: JSON.parse(JSON.stringify(data.investor)),
      },
    };
  };
</script>

<script lang="ts">
  import InvestorEditForm from "$views/InvestorEditForm.svelte";

  export let investor: Investor;
  export let investorID: number;
  export let investorVersion: number;
</script>

<InvestorEditForm bind:investor bind:investorID bind:investorVersion />
