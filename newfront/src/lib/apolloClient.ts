import { ApolloClient, HttpLink, InMemoryCache } from "@apollo/client/core";
import type { NormalizedCacheObject } from "@apollo/client/core";

class Client {
  private static _instance: Client;
  // this is okay, because we know we create a singleton in the constructor()
  client: ApolloClient<NormalizedCacheObject>;

  constructor() {
    if (Client._instance) return Client._instance;
    Client._instance = this;
    this.client = this.setupClient();
  }

  setupClient() {
    return new ApolloClient({
      // link: new HttpLink({ uri: "http://localhost:3000/graphql/", fetch }),
      link: new HttpLink({ uri: "http://localhost:3000/graphql/" }),
      cache: new InMemoryCache(),
    });
  }
}

export const client = new Client().client;
