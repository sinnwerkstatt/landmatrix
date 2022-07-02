import { ApolloClient } from "@apollo/client/core/ApolloClient.js";
import { HttpLink } from "@apollo/client/link/http/HttpLink.js";
import { InMemoryCache } from "@apollo/client/cache/inmemory/inMemoryCache.js";
import type { NormalizedCacheObject } from "@apollo/client/core";
import { writable, type Writable } from "svelte/store";

interface WritableApolloClient extends Writable<ApolloClient<NormalizedCacheObject>> {
  resetClient?(this: void, cookie: string): void;
}

function createApolloClient(): WritableApolloClient {
  const clnt = new ApolloClient({
    link: new HttpLink({ uri: import.meta.env.VITE_GRAPHQL_URL, credentials: "include" }),
    cache: new InMemoryCache(),
  });
  const { subscribe, set, update } = writable<ApolloClient<NormalizedCacheObject>>(clnt);

  return {
    subscribe,
    set,
    update,
    // resetClient: (cookie: string) => {
    //    const lnk = new HttpLink({ uri, credentials: "include", headers: { cookie } });
    //   update((clnt) => {
    //     clnt.setLink(lnk);
    //     return clnt;
    //   });
    // },
  };
}

export const client = createApolloClient();


// export async function checkUserAuthentication(cookie:string) {
//   // link: new HttpLink({ uri: import.meta.env.VITE_GRAPHQL_URL, fetch }),
//   const clnt = new ApolloClient({
//     link: new HttpLink({ uri: import.meta.env.VITE_GRAPHQL_URL, credentials: "include", headers: { cookie } }),
//     cache: new InMemoryCache(),
//   });
//   const {data } = await clnt.query({query: gql`
//       query {
//         me {
//           id
//           full_name
//           username
//           initials
//           is_authenticated
//           is_impersonate
//           role
//           userregionalinfo {
//             country {
//               id
//               name
//             }
//             region {
//               id
//               name
//             }
//           }
//           groups {
//             id
//             name
//           }
//         }
//       }`} );
//   return data.me;
// }
