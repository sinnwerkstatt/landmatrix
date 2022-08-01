<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import type { Investor } from "$lib/types/investor";
  import { investor_gql_query } from "../queries";

  export const load: Load = async ({ params, stuff }) => {
    if (!stuff.user) return { status: 403, error: "Permission denied" };

    let [investorID, investorVersion] = params.IDs.split("/").map((x) =>
      x ? +x : undefined
    );
    const { data } = await stuff.secureApolloClient.query<{ investor: Investor[] }>({
      query: investor_gql_query,
      variables: {
        id: investorID,
        version: investorVersion,
        subset: "UNFILTERED",
        depth: 0,
        includeDeals: false,
      },
    });
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
