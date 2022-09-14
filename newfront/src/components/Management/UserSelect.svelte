<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  import { page } from "$app/stores"

  import { allUsers } from "$lib/stores"
  import type { User } from "$lib/types/user"
  import { UserRole } from "$lib/types/user"

  export let value: User | number
  export let required = false
  export let extraUserIDs: number[] = []

  onMount(async () => {
    if (typeof value === "number") value = $allUsers.find(u => u.id === value) ?? -1
  })

  let showEverybody = false
</script>

<Select
  {VirtualList}
  bind:value
  getOptionLabel={(o, ftxt) =>
    $page.data.user.role === !showEverybody && UserRole.ADMINISTRATOR && o.isCreator
      ? `Fetch all users, to find <b>"${ftxt}"</b>..`
      : o.username
      ? `${o.full_name} (<b>${o.username}</b>)`
      : `Can't find <b>"${ftxt}"</b>..`}
  getSelectionLabel={o => `${o.full_name} (<b>${o.username}</b>)`}
  items={$allUsers.filter(
    u =>
      showEverybody ||
      extraUserIDs.includes(u.id) ||
      u.groups?.some(g => ["Administrators", "Editors"].includes(g.name)),
  )}
  optionIdentifier="id"
  placeholder={$_("User")}
  showChevron
  inputAttributes={{ required: required && !value }}
  isCreatable
  on:itemCreated={() => (showEverybody = true)}
/>
