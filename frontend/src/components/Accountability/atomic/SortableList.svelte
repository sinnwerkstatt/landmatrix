<script lang="ts">
  // A component to create sortable lists of SidebarTab elements based
  // on an array of objects containing at least id, name and position information
  import SidebarTab from "./SidebarTab.svelte"

  let container: HTMLElement = $state()

  const placeholder = [
    { id: 2, name: "Element 2" },
    { id: 3, name: "Element 3" },
    { id: 1, name: "Element 1" },
  ]

  interface Props {
    items?: { id: number; name: string }[]
    onReorder?: () => void
    onEdit?: (id: number) => void
    onBookmark?: (id: number, action: string) => void
    onDelete?: (id: number) => void
  }

  let {
    items = $bindable(placeholder),
    onReorder,
    onEdit,
    onBookmark,
    onDelete,
  }: Props = $props()

  let refs: [HTMLElement] | [] = $state([])

  let draggedItem: HTMLElement | null = null

  function handleDragstart(e, i) {
    refs[i].style.opacity = "0.4"
    draggedItem = refs[i]
  }

  function handleDragend(e, i) {
    refs[i].style.opacity = "1"
    draggedItem = null
    updatePosition(container)
    onReorder?.()
  }

  function preventDefault(handler) {
    return e => {
      e.preventDefault()
      handler(e)
    }
  }

  function handleDragover(e, container: HTMLElement) {
    const afterElement = getDragAfterElement(container, e.clientY)
    if (afterElement == null) {
      container.appendChild(draggedItem)
    } else {
      container.insertBefore(draggedItem, afterElement)
    }
  }

  function getDragAfterElement(container, y) {
    const draggableElements = refs
      .filter(ref => ref !== draggedItem)
      .filter(ref => ref.parentElement == container)

    return draggableElements.reduce(
      (closest, child) => {
        const box = child.getBoundingClientRect()
        const offset = y - box.top - box.height / 2
        if (offset < 0 && offset > closest.offset) {
          return { offset: offset, element: child }
        } else {
          return closest
        }
      },
      { offset: Number.NEGATIVE_INFINITY },
    ).element
  }

  function updatePosition(container: HTMLElement) {
    const elements = [...container.querySelectorAll("li")]
    const ids = elements.map(e => Number(e.id))

    let reordered: { id: number; name: string }[] = []

    ids.forEach(id => {
      const item = items.find(e => e.id === id)
      reordered.push(item)
    })

    items = reordered
  }
</script>

<ul
  class="flex flex-col gap-2"
  ondragover={e => preventDefault(handleDragover(e, container))}
  bind:this={container}
>
  {#each items as { id, name }, index (id)}
    {@const imax = items.length}
    {@const menuPosition = imax - 1 > index ? "bottom" : "top"}
    <li
      bind:this={refs[index]}
      {id}
      class="select-none"
      style="opacity: 1;"
      draggable="false"
      ondragstart={e => {
        handleDragstart(e, index)
      }}
      ondragend={e => {
        handleDragend(e, index)
      }}
    >
      <SidebarTab
        {id}
        label={name}
        handle={true}
        menu={true}
        {menuPosition}
        {onEdit}
        {onBookmark}
        {onDelete}
      />
    </li>
  {/each}
</ul>
