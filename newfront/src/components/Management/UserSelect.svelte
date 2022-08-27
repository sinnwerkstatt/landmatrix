<script lang="ts">
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import Select from "svelte-select";
  import VirtualList from "svelte-tiny-virtual-list";
  import type { Writable } from "svelte/store";
  import { page } from "$app/stores";
  import { getUsers } from "$lib/stores";
  import type { User } from "$lib/types/user";

  export let value: User | number;

  let users: Writable<User[]>;

  onMount(async () => {
    users = await getUsers($page.data.urqlClient);
    if (typeof value === "number") value = $users.find((u) => u.id === value);
  });
</script>

<Select
  {...$$props}
  {VirtualList}
  bind:value
  getOptionLabel={(o) => `${o.full_name} (<b>${o.username}</b>)`}
  getSelectionLabel={(o) => `${o.full_name} (<b>${o.username}</b>)`}
  items={$users}
  optionIdentifier="id"
  placeholder={$_("User")}
  showChevron
/>
