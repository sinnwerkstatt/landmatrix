import { Client, cacheExchange, fetchExchange, gql } from "@urql/core"

import { i18nload } from "$lib/i18n/i18n"
import { fetchBasis } from "$lib/stores"
import type { User } from "$lib/types/user"

import type { LayoutLoad } from "./$types"

// ssr turned on by default
// https://kit.svelte.dev/docs/page-options#ssr

async function fetchMe(urqlClient: Client) {
  const { data } = await urqlClient
    .query<{ me: User }>(
      gql`
        query {
          me {
            id
            username
            full_name
            is_authenticated
            is_impersonate
            is_superuser
            role
            country {
              id
              name
            }
            region {
              id
              name
            }
            groups {
              id
              name
            }
          }
        }
      `,
      {},
    )
    .toPromise()
  if (data) return data.me
}

export const load: LayoutLoad = async ({ fetch, data }) => {
  const urqlClient = new Client({
    url: "/graphql/",
    exchanges: [cacheExchange, fetchExchange],
    fetch,
    fetchOptions: () => ({ credentials: "include" }),
  })

  const user: User | undefined = await fetchMe(urqlClient)
  const lang = data?.locale ?? "en"
  await Promise.all([fetchBasis(lang, fetch, urqlClient), i18nload(lang)])

  return { urqlClient, user }
}
