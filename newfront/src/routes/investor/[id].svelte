<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import { request } from "graphql-request";
  import { GQLEndpoint } from "$lib";
  import { investor_gql_query } from "./queries";

  export const load: Load = async ({ params }) => {
    const variables = {
      id: +params.id,
      includeDeals: true,
    };
    const investor = await request(GQLEndpoint, investor_gql_query, variables);
    console.log(JSON.stringify(investor, undefined, 2));

    return { props: { investor } };
  };
</script>

<script lang="ts">
  import { page } from "$app/stores";
  import type { Investor } from "$lib/types/investor";

  export let investor: Investor;
  const investorID = $page.params.id;
</script>

Investor {investorID}

<pre>{JSON.stringify(investor, null, 2)}</pre>
