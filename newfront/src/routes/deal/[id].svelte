<script context="module" lang="ts">
  import { request } from "graphql-request";
  import type { Load } from "@sveltejs/kit";
  import { deal_gql_query } from "./queries";
  import { GQLEndpoint } from "$lib";

  export const load: Load = async ({ params }) => {
    const variables = {
      id: +params.id,
    };
    const deal = await request(GQLEndpoint, deal_gql_query, variables);
    console.log(JSON.stringify(deal, undefined, 2));

    return { props: { deal } };
  };
</script>

<script lang="ts">
  import { page } from "$app/stores";

  export let deal;
  const dealID = $page.params.id;
</script>

Deal {dealID}

<pre>{JSON.stringify(deal, null, 2)}</pre>
