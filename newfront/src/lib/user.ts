import { gql } from "graphql-tag";
import { get } from "svelte/store";
import type { User } from "$lib/types/user";
import { UserLevel } from "$lib/types/user";
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
  return userWithLevel(data.login);
}
export function userWithLevel(user: User): User {
  const me = { ...user };
  const levelmap: { [key: string]: UserLevel } = {
    Administrators: UserLevel.ADMINISTRATOR,
    Editors: UserLevel.EDITOR,
    Reporters: UserLevel.REPORTER,
  };

  let level = UserLevel.ANYBODY;
  if (me.groups)
    me.groups?.forEach((g) => {
      level = Math.max(UserLevel.ANYBODY, levelmap[g.name]);
    });
  me.level = level;

  return me;
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
