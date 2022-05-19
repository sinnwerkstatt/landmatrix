import { ApolloClient, HttpLink, InMemoryCache } from "@apollo/client/core";
import type { NormalizedCacheObject } from "@apollo/client/core";
import { writable, type Writable } from "svelte/store";

interface WritableApolloClient extends Writable<ApolloClient<NormalizedCacheObject>> {
  resetClient(this: void, cookie: string): void;
}

// TODO: only reset on cookie.session change
// const cookie = writable<string>("");

function createApolloClient(): WritableApolloClient {
  const cache = new InMemoryCache();
  const uri = "http://localhost:3000/graphql/";
  // link: new HttpLink({ uri: "http://localhost:3000/graphql/", fetch }),
  const clnt = new ApolloClient({
    link: new HttpLink({ uri, credentials: "include" }),
    cache,
  });
  const { subscribe, set, update } = writable<ApolloClient<NormalizedCacheObject>>(clnt);

  return {
    subscribe,
    set,
    update,
    resetClient: (cookie: string) => {
      const clnt = new ApolloClient({
        link: new HttpLink({ uri, credentials: "include", headers: { cookie } }),
        cache,
      });
      set(clnt);
    },
  };
}

export const client = createApolloClient();
