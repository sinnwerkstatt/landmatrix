import { InMemoryCache } from "apollo-cache-inmemory";
import ApolloClient from "apollo-client";
import { createHttpLink } from "apollo-link-http";

export const apolloClient = new ApolloClient({
  link: createHttpLink({ uri: "/graphql/" }),
  cache: new InMemoryCache(),
});
