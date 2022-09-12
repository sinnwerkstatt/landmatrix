import { error } from "@sveltejs/kit"
import type { Client } from "@urql/svelte"
import { gql } from "@urql/svelte"

import type { User } from "$lib/types/user"
import { UserLevel } from "$lib/types/user"

export async function dispatchLogin(
  username: string,
  password: string,
  urqlClient: Client,
) {
  const { data } = await urqlClient
    .mutation<{ login: { status: string; error: string; user: User } }>(
      gql`
        mutation Login($username: String!, $password: String!) {
          login(username: $username, password: $password) {
            status
            error
            user {
              id
              full_name
              username
              initials
              is_authenticated
              is_impersonate
              level
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
        }
      `,
      { username, password },
    )
    .toPromise()
  const login = data?.login
  if (!login) throw error(500, "weird login problems")
  return login
}

export async function dispatchLogout(urqlClient: Client) {
  const { data } = await urqlClient
    .mutation(
      gql`
        mutation {
          logout
        }
      `,
      {},
    )
    .toPromise()
  return data.logout
}
