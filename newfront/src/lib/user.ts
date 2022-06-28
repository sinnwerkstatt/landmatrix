import { gql } from "@apollo/client/core";
import { get } from "svelte/store";
import { client } from "./apolloClient";

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
