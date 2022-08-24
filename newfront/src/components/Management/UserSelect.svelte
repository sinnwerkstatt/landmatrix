<script lang="ts">
  import { gql } from "@urql/svelte";
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import VirtualList from "svelte-tiny-virtual-list";
  import { writable } from "svelte/store";
  import { page } from "$app/stores";
  import type { User } from "$lib/types/user";

  export let value: User | number;

  let users = writable<User[]>(undefined);

  async function fetchUsers() {
    if ($users !== undefined) return;
    const { data } = await $page.data.urqlClient
      .query<{ users: User[] }>(
        gql`
          {
            users {
              id
              full_name
              username
            }
          }
        `
      )
      .toPromise();
    await users.set(
      [...data.users].sort((a, b) => a.full_name.localeCompare(b.full_name))
    );

    if (typeof value === "number") value = data.users.find((u) => u.id === value);
  }
  onMount(fetchUsers);
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
  {VirtualList}
/>
