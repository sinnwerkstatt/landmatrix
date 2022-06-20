import { gql } from "@apollo/client/core";
import { get, writable } from "svelte/store";
import type { User } from "$lib/types/user";
import { client } from "./apolloClient";

export const user = writable<User>(undefined);

export async function getMe() {
  console.log("getMe");
  const { data } = await get(client).query({
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
  await user.set(data.me);
}

export async function dispatchLogin(username: string, password: string) {
  const mutation = gql`
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
    }
  `;
  const variables = { username, password };
  const { data } = await get(client).mutate({ mutation, variables });
  if (data.login.status === true) {
    user.set(data.login.user);
  }
  return data.login;
}

export async function dispatchLogout() {
  const { data } = await get(client).mutate({
    mutation: gql`
      mutation {
        logout
      }
    `,
  });
  return data.logout;
}
