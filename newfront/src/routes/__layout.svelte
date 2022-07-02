<script context="module" lang="ts">
  import { InMemoryCache } from "@apollo/client/cache/inmemory/inMemoryCache.js";
  import { ApolloClient } from "@apollo/client/core/ApolloClient.js";
  import { HttpLink } from "@apollo/client/link/http/HttpLink.js";
  import type { Load } from "@sveltejs/kit";
  import { gql } from "graphql-tag";
  import Cookies from "js-cookie";
  import { get } from "svelte/store";
  import { client } from "$lib/apolloClient";
  import { i18nload } from "$lib/i18n/i18n";
  import { fetchBasis } from "$lib/stores";
  import type { User } from "$lib/types/user";

  function getApolloClient(session) {
    if (!session.cookie) {
      return get(client);
    }
    const uri = "http://localhost:3000/graphql/";
    return new ApolloClient({
      link: new HttpLink({
        uri,
        credentials: "include",
        headers: { cookie: session.cookie },
      }),
      cache: new InMemoryCache(),
    });
  }
  async function fetchMe(apolloClient) {
    const { data } = await apolloClient.query<{ me: User }>({
      query: gql`
        query {
          me {
            id
            full_name
            username
            initials
            is_authenticated
            is_impersonate
            role
            userregionalinfo {
              country {
                id
                name
              }
              region {
                id
                name
              }
            }
            groups {
              id
              name
            }
          }
        }
      `,
    });
    return data.me;
  }

  export const load: Load = async ({ params, session }) => {
    const secureApolloClient = getApolloClient(session);
    const user = await fetchMe(secureApolloClient);
    const lang = Cookies.get("django_language") ?? "en";
    await fetchBasis(lang);
    await i18nload(params);
    return { stuff: { secureApolloClient, user } };
  };
</script>

<script>
  import "../app.css";
  import Footer from "$components/Footer.svelte";
  import Navbar from "$components/Navbar.svelte";
  import NavigationLoader from "$components/NavigationLoader.svelte";
</script>

<NavigationLoader />
<Navbar />
<div class="h-[calc(100vh-58px-32px)] overflow-x-auto">
  <slot />
</div>
<Footer />
