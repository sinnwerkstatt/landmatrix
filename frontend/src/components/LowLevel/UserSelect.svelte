<script lang="ts">
  import type { User } from "$lib/types/user"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let users: User[] = []
  export let value: User | null = null
  export let required = false

  const itemFilter = (label: string, filterText: string, user: User) => {
    const filterTextLower = filterText.toLowerCase()
    return (
      user.full_name.toLowerCase().includes(filterTextLower) ||
      user.username.toLowerCase().includes(filterTextLower)
    )
  }
</script>

<VirtualListSelect bind:value items={users} label="username" {required} {itemFilter}>
  <svelte:fragment slot="selection" let:selection>
    {selection.full_name} (
    <b>{selection.username}</b>
    )
  </svelte:fragment>
  <svelte:fragment slot="item" let:item>
    {item.full_name} (
    <b>{item.username}</b>
    )
  </svelte:fragment>
</VirtualListSelect>
