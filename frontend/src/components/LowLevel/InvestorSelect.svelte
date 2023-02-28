<script lang="ts">
  import VirtualListSelect from "./VirtualListSelect.svelte"

  interface InvestorItem {
    id: number
    name: string
  }
  export let investors: InvestorItem[] = []
  export let value: InvestorItem | undefined = undefined
  export let required = false

  export let name = undefined

  const itemFilter = (label: string, filterText: string, option: InvestorItem) => {
    const filterTextLower = filterText.toLowerCase()
    return (
      option.name.toLowerCase().includes(filterTextLower) ||
      option.id.toString().includes(filterTextLower)
    )
  }
</script>

<VirtualListSelect
  bind:value
  items={investors}
  label="name"
  {required}
  {name}
  {itemFilter}
  on:filter
  on:input
>
  <svelte:fragment slot="selection" let:selection>
    {selection.name} (#{selection.id})
  </svelte:fragment>
  <svelte:fragment slot="item" let:item>
    {item.name} (#{item.id})
  </svelte:fragment>
</VirtualListSelect>
