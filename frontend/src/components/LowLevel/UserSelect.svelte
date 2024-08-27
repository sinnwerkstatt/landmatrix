<script lang="ts">
  import { allUsers } from "$lib/stores"
  import { UserRole, type LeanUser } from "$lib/types/data"
  import { hasRoleOrAbove } from "$lib/utils/permissions"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  export let value: number | null = null
  export let required = false

  export let minimumRole: UserRole = UserRole.ANYBODY
  export let userIDs: Set<number> | undefined = undefined

  $: items = $allUsers.length
    ? $allUsers.filter(u => {
        if (!u.is_active) return false

        if (u.id === value) return true

        if (userIDs) return userIDs!.has(u.id)
        if (minimumRole > UserRole.ANYBODY) return hasRoleOrAbove(minimumRole)(u)

        return true
      })
    : []

  const itemFilter = (_label: string, filterText: string, user: LeanUser) => {
    const filterTextLower = filterText.toLowerCase()
    return (
      user.full_name.toLowerCase().includes(filterTextLower) ||
      user.username.toLowerCase().includes(filterTextLower)
    )
  }
</script>

{#if items.length}
  <VirtualListSelect
    value={$allUsers.find(u => u.id === value) ?? null}
    {items}
    label="username"
    {required}
    {itemFilter}
    on:input={e => (value = e.detail?.id ?? null)}
  >
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
