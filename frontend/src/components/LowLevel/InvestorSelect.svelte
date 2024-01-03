<script lang="ts">
  import { _ } from "svelte-i18n"

  import VirtualListSelect from "./VirtualListSelect.svelte"

  interface InvestorItem {
    id?: number
    name: string
    created?: boolean
  }
  export let investors: InvestorItem[] = []
  export let value: InvestorItem | null | undefined = undefined
  export let required = false
  export let disabled = false
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
  {disabled}
>
  <svelte:fragment slot="selection" let:selection>
    {#if selection.created}
      <div class="font-semibold italic">[new investor]</div>
    {:else}
      {selection.name} (#{selection.id})
    {/if}
  </svelte:fragment>
  <svelte:fragment slot="item" let:item>
    {#if item.created}
      {$_("Create")}: {item.name}
    {:else}
      #{item.id}: {item.name}
    {/if}
  </svelte:fragment>
</VirtualListSelect>
