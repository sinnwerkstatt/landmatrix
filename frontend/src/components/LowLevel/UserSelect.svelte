<script lang="ts">
  import type { components } from "$lib/openAPI"
  import { allUsers } from "$lib/stores"
  import { UserRole } from "$lib/types/newtypes"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let value: components["schemas"]["LeanUser"] | number | null = null
  export let required = false

  export let minimumRole: UserRole = UserRole.ANYBODY
  export let userIDs: Set<number> | undefined = undefined

  let items: components["schemas"]["LeanUser"][] = []

  async function initialize(users: components["schemas"]["LeanUser"][]) {
    if (!users.length) return

    if (typeof value === "number") value = users.find(u => u.id === value) ?? null
    if (userIDs) items = users.filter(u => userIDs!.has(u.id))
    else
      items = minimumRole ? users.filter(u => u.role && u.role >= minimumRole) : users
  }

  $: initialize($allUsers.filter(u => u.is_active))

  const itemFilter = (
    label: string,
    filterText: string,
    user: components["schemas"]["LeanUser"],
  ) => {
    const filterTextLower = filterText.toLowerCase()
    return (
      user.full_name!.toLowerCase().includes(filterTextLower) ||
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
