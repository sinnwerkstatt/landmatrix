<script lang="ts">
  import VirtualList from "svelte-tiny-virtual-list"
  import { tick } from "svelte"
  import Select from "svelte-select"

  // we assume all items have an id field
  interface Item {
    id: number | string
  }
  export const itemId = "id"

  export let items: Item[] = []
  export let value: Item | undefined = undefined
  export let required = false
  export let label = undefined
  type FilterFn<T> = (label: string, filterText: string, option: T) => boolean
  export let itemFilter: FilterFn<Item> | undefined = undefined

  // bind value for keyboard navigation but also set on click virtual list item
  let listOpen = false
  let filterText = ""
  const setValue = (item: Item) => {
    value = item
    listOpen = false
    filterText = ""
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
  --list-max-height="150px"
  bind:value
  bind:listOpen
  bind:filterText
  bind:hoverItemIndex
  {itemId}
  {items}
  {itemFilter}
  {label}
  {required}
  on:input
>
  <svelte:fragment slot="selection" let:selection>
    <slot name="selection" {selection}>
      {selection[label]}
    </slot>
  </svelte:fragment>
  <svelte:fragment slot="list" let:filteredItems>
    {#if filteredItems.length > 0}
      <VirtualList
        width="100%"
        height={150}
        itemCount={filteredItems.length}
        itemSize={50}
        scrollToIndex={hoverItemIndex}
      >
        <div
          slot="item"
          class="item"
          class:active={filteredItems[index].id === value?.id}
          class:hover={index === hoverItemIndex}
          let:index
          let:style
          {style}
          on:click={() => setValue(filteredItems[index])}
          on:mouseover={() => setHoverIndex(index)}
        >
          <slot name="item" item={filteredItems[index]}>
            {filteredItems[index][label]}
          </slot>
        </div>
      </VirtualList>
    {/if}
  </svelte:fragment>
</Select>

<style>
  .item {
    height: 30px;
    /*line-height: 30px;*/
    display: flex;
    /*text-align: center;*/
    align-items: center;
    padding: 20px;
    cursor: default;
    /*text-overflow: ellipsis;*/
    /*white-space: nowrap;*/
    /*overflow: hidden;*/
  }

  .item.hover {
    background: var(--item-hover-bg, #e7f2ff);
  }

  .item.active {
    background: var(--item-is-active-bg, #007aff);
    color: var(--item-is-active-color, #fff);
  }
</style>
