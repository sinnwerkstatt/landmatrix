<script lang="ts">
  import VirtualList from "svelte-tiny-virtual-list"
  import { tick } from "svelte"
  import Select from "svelte-select"

  // we assume all items have an id field
  interface Item {
    id: number | string | null
    created?: boolean
  }

  export type FilterFn<T> = (label: string, filterText: string, option: T) => boolean

  export const itemId = "id"

  export let items: Item[] = []
  export let value: Item | undefined = undefined
  export let label = "label"
  export let required = false
  export let disabled = false
  export let creatable = false
  export let placeholder = undefined
  export let itemFilter: FilterFn<Item> | undefined = undefined
  export let name: string | undefined = undefined

  let focused

  // bind value for keyboard navigation but also set on click virtual list item
  let listOpen = false
  let filterText = ""
  const setValue = (item: Item) => {
    value = { ...item }
    filterText = ""
    listOpen = false
  }

  const onFilter = (filteredItems: Item[]) => {
    const filterActive = filterText.length > 0
    const noItemsLefts = filteredItems.filter(i => !i.created).length === 0
    const notCreatedAlready = !filteredItems.find(i => i[label] === filterText)

    if (creatable && filterActive && noItemsLefts && notCreatedAlready) {
      // aware MuTaTiOn
      items = [
        ...items.filter(i => !i.created),
        { id: null, [label]: filterText, created: true },
      ]
    }
  }

  // bind to svelte-select for visualizing a11y keyboard navigation
  let hoverItemIndex = 0
  const setHoverIndex = (index: number) => {
    hoverItemIndex = index
  }

  // a hacky way of telling the list to scroll to active index on opening
  const handleListOpen = async () => {
    const activeIndex = items.findIndex(item => item.id === value?.id)

    await tick()
    setHoverIndex(0)
    await tick()
    setHoverIndex(activeIndex)
  }

  $: if (listOpen) handleListOpen()
</script>

<Select
  bind:value
  bind:listOpen
  bind:filterText
  bind:hoverItemIndex
  bind:focused
  {itemId}
  {items}
  {itemFilter}
  {label}
  {required}
  {disabled}
  {placeholder}
  {name}
  showChevron
  hasError={required && !value && !focused}
  on:input
  on:filter={e => onFilter(e.detail)}
>
  <svelte:fragment slot="selection" let:selection>
    <slot name="selection" {selection}>
      {selection[label]}
    </slot>
  </svelte:fragment>
  <svelte:fragment slot="list" let:filteredItems>
    {#if filteredItems.length > 0}
      <!--prevent any pointerdown propagation to not destroy focus of svelte-select-->
      <div on:pointerdown|stopPropagation>
        <VirtualList
          width="100%"
          height={152}
          itemCount={filteredItems.length}
          itemSize={38}
          scrollToIndex={hoverItemIndex}
        >
          <div
            slot="item"
            class="block h-[38px] cursor-default overflow-clip text-ellipsis whitespace-nowrap px-3 align-middle leading-[38px] dark:text-black"
            title={filteredItems[index][label]}
            class:item-active={filteredItems[index].id === value?.id}
            class:item-hover={index === hoverItemIndex}
            let:index
            let:style
            {style}
            on:click|stopPropagation={() => setValue(filteredItems[index])}
            on:keydown|stopPropagation
            on:mouseover={() => setHoverIndex(index)}
            on:focus={() => setHoverIndex(index)}
          >
            <slot name="item" item={filteredItems[index]}>
              {filteredItems[index][label]}
            </slot>
          </div>
        </VirtualList>
      </div>
    {/if}
  </svelte:fragment>
</Select>

<style>
  .item-hover {
    background: var(--item-hover-bg, lightgrey);
  }

  .item-active {
    background: var(--item-is-active-bg, orange);
    color: var(--item-is-active-color, black);
  }
</style>
