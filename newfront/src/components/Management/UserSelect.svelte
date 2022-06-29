<script lang="ts">
  import { gql } from "@apollo/client/core";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import { writable } from "svelte/store";
  import { page } from "$app/stores";
  import type { User } from "$lib/types/user";

  export let value;

  let users = writable<User[]>(undefined);

  async function fetchUsers() {
    if ($users !== undefined) return;
    const { data } = await $page.stuff.secureApolloClient.query<{ users: User[] }>({
      query: gql`
        {
          users {
            id
            full_name
            username
          }
        }
      `,
    });
    users.set([...data.users].sort((a, b) => a.full_name.localeCompare(b.full_name)));
  }
  fetchUsers();
</script>

<Select
  {...$$props}
  items={$users}
  bind:value
  placeholder={$_("User")}
  optionIdentifier="id"
  getOptionLabel={(o) => `${o.full_name} (<b>${o.username}</b>)`}
  getSelectionLabel={(o) => `${o.full_name} (<b>${o.username}</b>)`}
  showChevron
/>
