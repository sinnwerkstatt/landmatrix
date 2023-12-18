<script lang="ts">
  import { _ } from "svelte-i18n"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  interface InvestorItem {
    id: number | null
    name: string
    created?: boolean
  }
  export let investors: InvestorItem[] = []
  export let value: InvestorItem | undefined = undefined
  export let required = false
  export let creatable = false
  export let name: string | undefined = undefined

  const itemFilter = (label: string, filterText: string, option: InvestorItem) => {
    const filterTextLower = filterText.toLowerCase()
    return option.name.toLowerCase().includes(filterTextLower)
  }
</script>

<VirtualListSelect
  bind:value
  items={investors}
  label="name"
  {creatable}
  {required}
  {name}
  {itemFilter}
  on:input
>
  <svelte:fragment slot="selection" let:selection>
    {selection.name}
    (#{selection.id})
  </svelte:fragment>
  <svelte:fragment slot="item" let:item>
    {#if item.created}
      {$_("Create")}{":"}
      {item.name}
    {:else}
      #{item.id}: {item.name}
    {/if}
  </svelte:fragment>
</VirtualListSelect>
