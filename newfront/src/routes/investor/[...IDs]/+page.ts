import { error, redirect } from "@sveltejs/kit";
import { investor_gql_query } from "$lib/investor_queries";
import type { Investor } from "$lib/types/investor";
import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, parent }) => {
  const { urqlClient } = await parent();
  const [investorID, investorVersion] = params.IDs.split("/").map((x) =>
    x ? +x : undefined
  );

  if (!investorID) throw error(404, "Investor not found");

  const { data } = await urqlClient
    .query<{ investor: Investor }>(investor_gql_query, {
      id: investorID,
      version: investorVersion,
      includeDeals: true,
      depth: 1,
    })
    .toPromise();
  if (!data?.investor) throw error(404, "Investor not found");
  if (data.investor.status === 1 && !investorVersion) {
    const investorVersion = data.investor.versions?.[0]?.id;
    throw redirect(301, `/investor/${investorID}/${investorVersion}`);
  }

  return { investorID, investorVersion, investor: data.investor };
};
