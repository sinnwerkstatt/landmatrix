<script lang="ts" module>
  export interface Item {
    id: number | string | null
    created?: boolean
  }
  export type FilterFn<Option> = (
    label: string,
    filterText: string,
    option: Option,
  ) => boolean
</script>

<script lang="ts" generics="T extends Item">
  import { tick, type Snippet } from "svelte"
  import { _ } from "svelte-i18n"
  import Select from "svelte-select"
  import VirtualList from "svelte-tiny-virtual-list"

  export const itemId = "id"

  interface Props {
    items?: T[]
    itemFilter?: FilterFn<T> | undefined
    value?: Item | null
    label?: string
    id?: string | null
    required?: boolean
    disabled?: boolean
    creatable?: boolean
    heightInPx?: number
    placeholder?: string
    name?: string | undefined
    selectionSlot?: Snippet<[T]>
    itemSlot?: Snippet<[T]>
    oninput?: (e: CustomEvent) => void
    onclear?: (e: CustomEvent) => void
  }

  let {
    items = [],
    itemFilter = undefined,
    value,
    label = "label",
    id = null,
    required = false,
    disabled = false,
    creatable = false,
    heightInPx = 228,
    placeholder = $_("Please select"),
    name = undefined,
    selectionSlot,
    itemSlot,
    oninput,
    onclear,
  }: Props = $props()

  let focused: boolean = $state(false)

  // bind value for keyboard navigation but also set on click virtual list item
  let listOpen = $state(false)
  let filterText = $state("")

  const setValue = (item: Item) => {
    value = { ...item }
    filterText = ""
    listOpen = false
  }

  // bind to svelte-select for visualizing a11y keyboard navigation
  let hoverItemIndex = $state(0)
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

  $effect(() => {
    if (listOpen) handleListOpen()
  })
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
  {id}
  showChevron
  hasError={required && !value && !focused}
  on:input={e => oninput?.(e)}
  on:clear={e => onclear?.(e)}
>
  <svelte:fragment slot="selection" let:selection>
    {#if selectionSlot}
      {@render selectionSlot(selection)}
    {:else}
      {selection[label]}
    {/if}
  </svelte:fragment>

  <svelte:fragment slot="list" let:filteredItems>
    {@const patchedItems =
      filteredItems.length === 0
        ? creatable
          ? [{ id: null, [label]: filterText, created: true }]
          : []
        : filteredItems}

    <div onpointerdown={e => e.stopPropagation()}>
      <VirtualList
        width="100%"
        height={heightInPx}
        itemCount={patchedItems.length}
        itemSize={38}
        scrollToIndex={patchedItems.length > 0 ? hoverItemIndex : undefined}
      >
        <div
          role="presentation"
          slot="item"
          class="block h-[38px] cursor-default overflow-clip text-ellipsis whitespace-nowrap px-3 align-middle leading-[38px] dark:text-white"
          title={patchedItems[index][label]}
          class:item-active={patchedItems[index].id === value?.id}
          class:item-hover={index === hoverItemIndex}
          let:index
          let:style
          {style}
          onclick={e => {
            e.stopPropagation()
            setValue(patchedItems[index])
          }}
          onkeydown={e => e.stopPropagation()}
          onmouseover={() => setHoverIndex(index)}
          onfocus={() => setHoverIndex(index)}
        >
          {#if itemSlot}
            {@render itemSlot(patchedItems[index])}
          {:else}
            {patchedItems[index][label]}
          {/if}
        </div>
      </VirtualList>
    </div>
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
