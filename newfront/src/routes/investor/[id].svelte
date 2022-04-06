<script context="module" lang="ts">
  import { request } from "graphql-request";
  import type { Load } from "@sveltejs/kit";
  import { investor_gql_query } from "./queries";
  import { GQLEndpoint } from "$lib";

  export const load: Load = async ({ params }) => {
    const variables = {
      id: +params.id,
    };
    const deal = await request(GQLEndpoint, investor_gql_query, variables);
    console.log(JSON.stringify(deal, undefined, 2));

    return { props: { deal } };
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
