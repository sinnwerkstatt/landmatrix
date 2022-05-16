import { derived } from "svelte/store";
import type { Readable } from "svelte/store";
import { client } from "$lib/apolloClient";
import { filters, publicOnly } from "$lib/filters";
import { user } from "$lib/stores";
import type { Deal } from "$lib/types/deal";
import { data_deal_query_gql } from "../routes/list/query";

let debounceTimeOut: NodeJS.Timeout;

export const deals: Readable<Deal[]> = derived(
  [filters, publicOnly, user],
  ([$filters, $publicOnly, $user], set) => {
    // set([]); // setting "initial" value here.
    const variables = {
      limit: 0,
      filters: $filters.toGQLFilterArray(),
      subset: $user?.is_authenticated ? ($publicOnly ? "PUBLIC" : "ACTIVE") : "PUBLIC",
    };
    if (debounceTimeOut) clearTimeout(debounceTimeOut);
    debounceTimeOut = setTimeout(() => {
      client
        .query<{ deals: Deal[] }>({ query: data_deal_query_gql, variables })
        .then(({ data }) => set(data.deals));
    }, 300);
  }
);
