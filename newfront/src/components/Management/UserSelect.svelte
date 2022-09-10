<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  import { page } from "$app/stores"

  import { getUsers } from "$lib/stores"
  import type { User } from "$lib/types/user"
  import { UserLevel } from "$lib/types/user"

  export let value: User | number
  export let required = false
  export let extraUserIDs: number[] = []

  let users: User[] = []

  onMount(async () => {
    users = await getUsers($page.data.urqlClient, extraUserIDs)
    if (typeof value === "number") value = users.find(u => u.id === value)
  })

  async function fetchEverybody() {
    users = await getUsers($page.data.urqlClient, extraUserIDs, true)
    console.log(users.length)
    console.log("grabbing everybody")
  }
</script>

<Select
  {VirtualList}
  bind:value
  getOptionLabel={(o, ftxt) =>
    $page.data.user.level === UserLevel.ADMINISTRATOR && o.isCreator
      ? `Fetch all users, to find <b>"${ftxt}"</b>..`
      : `${o.full_name} (<b>${o.username}</b>)`}
  getSelectionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
  items={users}
  optionIdentifier="id"
  placeholder={$_("User")}
  showChevron
  inputAttributes={{ required: required && !value }}
  isCreatable
  on:itemCreated={fetchEverybody}
/>
