import { gql } from "graphql-tag";
import { derived, get, writable } from "svelte/store";
import type { Readable } from "svelte/store";
import { client } from "$lib/apolloClient";
import { data_deal_query_gql } from "$lib/deal_query";
import { filters, publicOnly } from "$lib/filters";
import type { Deal } from "$lib/types/deal";
import type { GQLFilter } from "$lib/types/filters";
import type { Investor } from "$lib/types/investor";

let dealsDebounceTimeout: NodeJS.Timeout;
let investorsDebounceTimeout: NodeJS.Timeout;

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
    if (dealsDebounceTimeout) clearTimeout(dealsDebounceTimeout);
    dealsDebounceTimeout = setTimeout(() => {
      get(client)
        .query<{ deals: Deal[] }>({ query: data_deal_query_gql, variables })
        .then(({ data }) => {
          loading.set(false);
          set(data.deals);
        });
    }, 300);
  }
);

export const investors: Readable<Investor[]> = derived(
  [deals, filters],
  ([$deals, $filters], set) => {
    if (!$deals) {
      set([]);
      return;
    }

    loading.set(true);

    const dealIDs = $deals.map((d) => d.id);
    const tooManyDealsHack = $deals.length > 2500;
    const filters: GQLFilter[] = tooManyDealsHack
      ? []
      : [{ field: "child_deals.id", operation: "IN", value: dealIDs }];

    if ($filters.investor) filters.push({ field: "id", value: $filters.investor.id });

    if ($filters.investor_country_id)
      filters.push({ field: "country_id", value: $filters.investor_country_id });

    const query = gql`
      query Investors($filters: [Filter]) {
        investors(limit: 0, filters: $filters) {
          id
          name
          country {
            id
            name
          }
          classification
          homepage
          opencorporates
          comment
          deals {
            id
          }
          status
          draft_status
          created_at
          modified_at
          is_actually_unknown
        }
      }
    `;
    const variables = { filters };
    if (investorsDebounceTimeout) clearTimeout(investorsDebounceTimeout);

    investorsDebounceTimeout = setTimeout(() => {
      get(client)
        .query<{ investors: Investor[] }>({ query, variables })
        .then(({ data }) => {
          set(
            data.investors.filter((investor, index, self) => {
              // remove duplicates
              if (self.indexOf(investor) !== index) return false;
              // filter for deals
              if (tooManyDealsHack) {
                return investor.deals?.some((d) => dealIDs.includes(d.id));
              }
              return true;
            })
          );
          loading.set(false);
        });
    }, 300);
  }
);
