import { error } from "@sveltejs/kit";
import { deal_gql_query } from "$lib/deal_queries";
import type { Deal } from "$lib/types/deal";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  const { user, urqlClient } = await parent();
  if (!user) return { status: 403, error: "Permission denied" };

  const [dealID, dealVersion] = params.IDs.split("/").map((x) => (x ? +x : undefined));
  const { data } = await urqlClient
    .query<{ deal: Deal[] }>(deal_gql_query, { id: dealID, version: dealVersion })
    .toPromise();
  if (!data?.deal)
    throw error(404, dealVersion ? "Deal version not found" : "Deal not found");

  return { dealID, dealVersion, deal: data.deal };
};
