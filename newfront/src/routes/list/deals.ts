import type { RequestHandler } from "@sveltejs/kit";
import { request } from "graphql-request";
import { GQLEndpoint } from "$lib";
import { FilterValues } from "$lib/filters";
import { data_deal_query_gql } from "./query";

export const get: RequestHandler = async () => {
  const variables = {
    limit: 100,
    filters: new FilterValues().default().toGQLFilterArray(),
    subset: "PUBLIC",
  };

  const ret = await request(GQLEndpoint, data_deal_query_gql, variables);
  const deals = ret.deals;

  if (deals) {
    return {
      body: { deals },
    };
  }

  return {
    status: 404,
  };
};
