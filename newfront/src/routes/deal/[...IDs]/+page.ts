import { error, redirect } from "@sveltejs/kit";
import type { CombinedError } from "@urql/svelte";
import { deal_gql_query } from "$lib/deal_queries";
import type { Deal } from "$lib/types/deal";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  const { urqlClient } = await parent();
  const [dealID, dealVersion] = params.IDs.split("/").map((x) => (x ? +x : undefined));

  if (!dealID) throw error(404, "Deal not found");

  let res;
  try {
    res = (
      await urqlClient
        .query<{ deal: Deal }>(deal_gql_query, { id: dealID, version: dealVersion })
        .toPromise()
    ).data;
  } catch (e) {
    if ((e as CombinedError).graphQLErrors[0].message === "deal not found")
      throw error(404, "Deal not found");
    throw error(500, `${e}`);
  }
  if (!res?.deal) throw error(404, "Deal not found");
  if (res.deal.status === 1 && !dealVersion) {
    const dealVersion = res.deal.versions?.[0]?.id;
    throw redirect(301, `/deal/${dealID}/${dealVersion}`);
  }
  return { dealID, dealVersion, deal: res.deal };
};
