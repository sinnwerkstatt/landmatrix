<script lang="ts">
  import { allUsers } from "$lib/stores"
  import { UserRole, type User } from "$lib/types/user"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let value: User | number | null = null
  export let required = false

  export let minimumRole: UserRole = UserRole.ANYBODY
  export let userIDs: Set<number> | undefined = undefined

  let items: User[] = []

  async function initialize(users: User[]) {
    if (!users.length) return

    if (typeof value === "number") value = users.find(u => u.id === value) ?? null
    if (userIDs) items = $allUsers.filter(u => userIDs!.has(u.id))
    else items = minimumRole ? users.filter(u => u.role >= minimumRole) : users
  }

  $: initialize($allUsers)

  const itemFilter = (label: string, filterText: string, user: User) => {
    const filterTextLower = filterText.toLowerCase()
    return (
      user.full_name.toLowerCase().includes(filterTextLower) ||
      user.username.toLowerCase().includes(filterTextLower)
    )
  }
</script>

{#if items.length}
  <VirtualListSelect bind:value {items} label="username" {required} {itemFilter}>
    <svelte:fragment slot="selection" let:selection>
      {#if selection.full_name}
        {selection.full_name} (
        <b>{selection.username}</b>
        )
      {:else}
        <b>{selection.username}</b>
      {/if}
    </svelte:fragment>
    <svelte:fragment slot="item" let:item>
      {#if item.full_name}
        {item.full_name} (
        <b>{item.username}</b>
        )
      {:else}
        <b>{item.username}</b>
      {/if}
    </svelte:fragment>
  </VirtualListSelect>
{/if}
