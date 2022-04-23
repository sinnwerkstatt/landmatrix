import { request } from "graphql-request";
import { derived } from "svelte/store";
import type { Readable } from "svelte/store";
import { data_deal_query_gql } from "../routes/list/query";
import { filters, publicOnly } from "./filters";
import { GQLEndpoint } from "./index";
import { user } from "./stores";
import type { Deal } from "./types/deal";

export const deals: Readable<Deal[]> = derived(
  [filters, publicOnly, user],
  ([$filters, $publicOnly, $user], set) => {
    // set([]); // setting "initial" value here.
    const variables = {
      limit: 0,
      filters: $filters.toGQLFilterArray(),
      subset: $user?.is_authenticated ? ($publicOnly ? "PUBLIC" : "ACTIVE") : "PUBLIC",
    };
    request(GQLEndpoint, data_deal_query_gql, variables).then((ret) =>
      set(ret.deals as Deal[])
    );
  }
);
