<script context="module" lang="ts">
  import type { Load } from "@sveltejs/kit";
  import type { Client } from "@urql/core";
  import { createClient, gql } from "@urql/svelte";
  import Cookies from "js-cookie";
  import { i18nload } from "$lib/i18n/i18n";
  import { fetchBasis } from "$lib/stores";
  import type { User } from "$lib/types/user";
  import { userWithLevel } from "$lib/user";

  async function fetchMe(urqlClient: Client) {
    const { data } = await urqlClient
      .query<{ me: User }>(
        gql`
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
        `
      )
      .toPromise();
    return userWithLevel(data.me);
  }

  export const load: Load = async ({ params, fetch }) => {
    const urqlClient = await createClient({
      url: import.meta.env.VITE_BASE_URL + "/graphql/",
      fetch,
      fetchOptions: () => ({ credentials: "include" }),
    });

    const user = await fetchMe(urqlClient);
    const lang = Cookies.get("django_language") ?? "en";
    await fetchBasis(lang, urqlClient);
    await i18nload(params);

    return { stuff: { urqlClient, user } };
  };
</script>

<script lang="ts">
  import Footer from "$components/Footer.svelte";
  import Navbar from "$components/Navbar.svelte";
  import NavigationLoader from "$components/NavigationLoader.svelte";
  import "../app.css";
</script>

<NavigationLoader />
<Navbar />
<div class="h-[calc(100vh-58px-32px)] overflow-x-auto">
  <slot />
</div>
<Footer />
