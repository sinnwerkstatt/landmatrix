import { InMemoryCache } from "apollo-cache-inmemory";
import ApolloClient from "apollo-client";
import { createHttpLink } from "apollo-link-http";

export const cache = new InMemoryCache();
export const apolloClient = new ApolloClient({
  // Note: One should use an absolute URL here (really though?)
  link: createHttpLink({
    uri: "/graphql/",
    // fetchOptions: { method: "GET" }
  }),
  cache: cache,
});
