<script lang="ts">
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  import { allUsers } from "$lib/stores"
  import type { User } from "$lib/types/user"
  import { UserRole } from "$lib/types/user"

  export let value: User | number
  export let required = false
  export let extraUserIDs: number[] = []

  onMount(async () => {
    if (typeof value === "number") value = $allUsers.find(u => u.id === value) ?? -1
  })

  const createUserLabel = (user: User) => `${user.full_name} (<b>${user.username}</b>)`
</script>

<Select
  {VirtualList}
  bind:value
  getOptionLabel={createUserLabel}
  getSelectionLabel={createUserLabel}
  items={$allUsers.filter(
    u => extraUserIDs.includes(u.id) || u.role > UserRole.REPORTER,
  )}
  optionIdentifier="id"
  placeholder={$_("User")}
  showChevron
  inputAttributes={{ required: required && !value }}
/>
