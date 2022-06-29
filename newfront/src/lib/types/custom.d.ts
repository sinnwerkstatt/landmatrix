import type { ApolloClient, NormalizedCacheObject } from "@apollo/client/core";

export interface BlockImage {
  image?: { url: string };
  url: string;
  caption?: string;
  external?: boolean;
}

export type SecureApolloClient = ApolloClient<NormalizedCacheObject>;
