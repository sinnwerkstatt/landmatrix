<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { client } from "$lib/apolloClient";
  import type { Investor } from "$lib/types/investor";
  import { investor_gql_query } from "./queries";

  export const load: Load = async ({ params }) => {
    const variables = {
      id: +params.id,
      includeDeals: true,
    };
    const { data } = await client.query<{ investor: Investor }>({
      query: investor_gql_query,
      variables,
    });
    console.log(JSON.stringify(data.investor, undefined, 2));

    return { props: { investor: data.investor } };
  };
</script>

<script lang="ts">
  import { page } from "$app/stores";

  export let investor: Investor;
  const investorID = $page.params.id;
</script>

Investor {investorID}

<pre>{JSON.stringify(investor, null, 2)}</pre>
