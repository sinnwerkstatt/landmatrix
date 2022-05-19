import type { RequestHandler } from "@sveltejs/kit";
import { get as storeGet } from "svelte/store";
import { client } from "$lib/apolloClient";
import { FilterValues } from "$lib/filters";
import { data_deal_query_gql } from "./query";

export const get: RequestHandler = async () => {
  const { data } = await storeGet(client).query({
    query: data_deal_query_gql,
    variables: {
      limit: 100,
      filters: new FilterValues().default().toGQLFilterArray(),
      subset: "PUBLIC",
    },
  });
  const deals = data.deals;

  if (deals) {
    return {
      body: { deals },
    };
  }

  return {
    status: 404,
  };
};
