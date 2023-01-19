import type { Client } from "@urql/core"
import { createClient, gql } from "@urql/svelte"

import { i18nload } from "$lib/i18n/i18n"
import { fetchBasis } from "$lib/stores"
import type { User } from "$lib/types/user"

import type { LayoutLoad } from "./$types"

export const ssr = false

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
  const urqlClient = await createClient({
    url: "/graphql/",
    fetch,
    fetchOptions: () => ({ credentials: "include" }),
  })

  const user = await fetchMe(urqlClient)
  const lang = data?.locale ?? "en"
  await Promise.all([fetchBasis(lang, fetch, urqlClient), i18nload(lang)])

  return { urqlClient, user }
}
