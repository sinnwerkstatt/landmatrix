import { derived, get, writable } from "svelte/store";
import type { Readable } from "svelte/store";
import { client } from "$lib/apolloClient";
import { data_deal_query_gql } from "$lib/deal_query";
import { filters, publicOnly } from "$lib/filters";
import type { Deal } from "$lib/types/deal";

let debounceTimeOut: NodeJS.Timeout;

export const loading = writable(false);

export const deals: Readable<Deal[]> = derived(
  [filters, publicOnly],
  ([$filters, $publicOnly], set) => {
    // set([]); // setting "initial" value here.
    loading.set(true);
    const variables = {
      limit: 0,
      filters: $filters.toGQLFilterArray(),
      subset: $publicOnly ? "PUBLIC" : "ACTIVE",
    };
    if (debounceTimeOut) clearTimeout(debounceTimeOut);
    debounceTimeOut = setTimeout(() => {
      get(client)
        .query<{ deals: Deal[] }>({ query: data_deal_query_gql, variables })
        .then(({ data }) => {
          loading.set(false);
          set(data.deals);
        });
    }, 300);
  }
);
