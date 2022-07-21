import { gql } from "graphql-tag";
import { derived, get, writable } from "svelte/store";
import type { Readable } from "svelte/store";
import { client } from "$lib/apolloClient";
import { data_deal_query_gql } from "$lib/deal_query";
import { filters, publicOnly } from "$lib/filters";
import type { Deal } from "$lib/types/deal";
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

// investorFilters() {
//   if (this.fetchAllInvestors) {
//     return [];
//   } else {
//     /** @type GQLFilter[] */
//     let filters = [
//       {
//         field: "child_deals.id",
//         operation: "IN",
//         value: this.deals.map((d) => d.id.toString()),
//       },
//     ];
//
//     let store_state_filters = this.$store.state.filters;
//     if (store_state_filters.investor) {
//       filters.push({
//         field: "id",
//         value: store_state_filters.investor.id.toString(),
//       });
//     }
//     if (store_state_filters.investor_country_id) {
//       filters.push({
//         field: "country_id",
//         value: store_state_filters.investor_country_id.toString(),
//       });
//     }
//     return filters;
//   }
// }

export const investors: Readable<Investor[]> = derived([filters], ([$filters], set) => {
  loading.set(true);
  const query = gql`
    query Investors($limit: Int!, $filters: [Filter]) {
      investors(limit: $limit, filters: $filters) {
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
        #involvements
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
  const variables = { limit: 0, filters: $filters.toGQLFilterArray() };
  if (investorsDebounceTimeout) clearTimeout(investorsDebounceTimeout);

  investorsDebounceTimeout = setTimeout(() => {
    get(client)
      .query<{ investors: Investor[] }>({ query, variables })
      .then(({ data }) => {
        console.log("EAVL INVESTORS THEN");
        loading.set(false);
        console.log(data.investors);
        set(data.investors);
      })
      .catch(() => {
        console.log("CATRROR");
      })
      .finally(() => {
        console.log("FINALLY");
      });
  }, 300);
});
