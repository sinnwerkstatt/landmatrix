<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import type { Deal } from "$lib/types/deal";
  import { deal_gql_query } from "../../queries";

  export const load: Load = async ({ params, stuff }) => {
    let [dealID] = params.IDs.split("/").map((x) => (x ? +x : undefined));
    if (!dealID) return { status: 404, error: `Deal not found` };

    let [versionFrom, versionTo] = params.versions
      .split("/")
      .map((x) => (x ? +x : undefined));

    if (!stuff.secureApolloClient) return {};

    const vFrom = await stuff.secureApolloClient.query<Deal>({
      query: deal_gql_query,
      variables: { id: dealID, version: +versionFrom, subset: "UNFILTERED" },
      fetchPolicy: "no-cache",
    });
    const vTo = await stuff.secureApolloClient.query<Deal>({
      query: deal_gql_query,
      variables: { id: dealID, version: +versionTo, subset: "UNFILTERED" },
      fetchPolicy: "no-cache",
    });
    console.log(vFrom);

    return {
      props: {
        dealID,
        versionFrom,
        versionTo,
        dealFrom: vFrom.data.deal,
        dealTo: vTo.data.deal,
      },
    };
    // if (!dealID) return { status: 404, error: `Deal not found` };
    //
    // if (!stuff.secureApolloClient) return {};
    // try {
    //   const { data } = await stuff.secureApolloClient.query<{ deal: Deal }>({
    //     query: deal_gql_query,
    //     variables: { id: dealID, version: dealVersion, subset: "UNFILTERED" },
    //   });
    //   return { props: { dealID, dealVersion, deal: data.deal } };
    // } catch (e) {
    //   if (e.graphQLErrors[0].message === "deal not found")
    //     return { status: 404, error: `Deal not found` };
    //   console.log(JSON.stringify(e));
    //   return { status: 500, error: e };
    // }
  };
</script>

<script lang="ts">
  import { _ } from "svelte-i18n";
  import PageTitle from "$components/PageTitle.svelte";

  export let versionFrom;
  export let versionTo;
  export let dealID: number;
  export let dealFrom: Deal;
  export let dealTo: Deal;
</script>

<svelte:head>
  <title>
    {$_("Comparing Deal")}
    #{dealID} @{versionFrom} - @{versionTo}
  </title>
</svelte:head>

<PageTitle>
  {$_("Comparing Deal")}
  #{dealID} @{versionFrom} &mdash; @{versionTo}</PageTitle
>

<div class="grid grid-cols-2">
  <div>{JSON.stringify(dealFrom)}</div>
  <div>{JSON.stringify(dealTo)}</div>
</div>
