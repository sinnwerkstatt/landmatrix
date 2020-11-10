import ApolloClient from "apollo-client";
import { createHttpLink } from "apollo-link-http";
import { InMemoryCache } from "apollo-cache-inmemory";

export const apolloClient = new ApolloClient({
  // TODO You should use an absolute URL here (really though?)
  link: createHttpLink({ uri: "/graphql/", fetchOptions: { method: "GET" } }),
  cache: new InMemoryCache(),
});
