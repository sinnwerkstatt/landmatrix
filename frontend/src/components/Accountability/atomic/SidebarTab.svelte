<script lang="ts">
  import { page } from "$app/state"

  import { allProjects, bookmarkIds } from "$lib/accountability/projects"
  import { me } from "$lib/accountability/stores"

  import IconEllipsis from "../icons/IconEllipsis.svelte"
  import IconMove from "../icons/IconMove.svelte"
  import DropdownMenu from "./DropdownMenu.svelte"
  import DropdownMenuItem from "./DropdownMenuItem.svelte"

  let box: HTMLElement = $state()
  let visibleMenu = $state(false)
  let position = $state("bottom")

  interface Props {
    id: number;
    label?: string;
    status?: string;
    menu?: boolean;
    handle?: boolean;
    menuPosition?: string;
    onBookmark?: (id:number, action:string) => void;
    onEdit?: (id:number) => void;
    onDelete?: (id:number) => void;
  }

  let {
    id,
    label = "label",
    status = "default",
    menu = false,
    handle = false,
    menuPosition = "auto",
    onBookmark,
    onEdit,
    onDelete,
  }: Props = $props();

  const project = $allProjects.find(p => p.id == id)

  let action = $derived($bookmarkIds.includes(id) ? "remove" : "add")

  function showMenu() {
    if (menuPosition == "auto") {
      const y = box.getBoundingClientRect().y
      const height = box.getBoundingClientRect().height
      const center = y + height / 2
      position = center < window.innerHeight * 0.6 ? "bottom" : "top"
    } else {
      position = menuPosition
    }
    visibleMenu = true
  }

  function handleBookmark() {
    onBookmark(id, action)
    visibleMenu = false
  }

  function handleEdit() {
    onEdit(id)
    visibleMenu = false
  }

  function handleDelete() {
    onDelete(id)
    visibleMenu = false
  }

  function writePath(id) {
    if (id) {
      return `/accountability/deals/${id}/`
    } else {
      return `/accountability/deals/0/`
    }
  }

  let path = $derived(writePath(id))
</script>

<div class="relative">
  <div
    class="wrapper {status}"
    class:active={page.url.pathname.startsWith(path)}
    bind:this={box}
  >
    <div class="flex h-full w-full items-center gap-2">
      {#if handle}
        <span class="shrink-0 cursor-move" draggable="true"><IconMove /></span>
      {/if}
      <a
        class="grid h-full w-full items-center !text-a-sm !text-a-gray-900"
        href={path}
      >
        {label}
      </a>
    </div>
    {#if menu}
      <button class="text-a-gray-400" onclick={showMenu}><IconEllipsis /></button>
    {/if}
  </div>

  <div class="menu absolute {position} right-0 z-20">
    <DropdownMenu bind:visible={visibleMenu}>
      <DropdownMenuItem icon="bookmark" on:click={handleBookmark}>
        <span class="text-left">
          {#if action == "add"}
            Bookmark
          {:else if action == "remove"}
            Unbookmark
          {/if}
        </span>
      </DropdownMenuItem>
      <DropdownMenuItem icon="check" on:click={handleEdit}>Edit</DropdownMenuItem>
      {#if (project && project.owner == $me.id) || (project && project.editors.includes($me.id))}
        <DropdownMenuItem icon="trashcan" on:click={handleDelete}>
          Delete
        </DropdownMenuItem>
      {/if}
    </DropdownMenu>
  </div>
</div>

<style>
  .wrapper {
    @apply flex items-center justify-between gap-2;
    @apply px-4;
    @apply h-14 w-full;
    @apply shrink-0;
    @apply text-left text-a-sm font-medium;
    @apply bg-white;
    @apply border-b-2 border-a-gray-200;
  }
  .wrapper:hover,
  .wrapper.active {
    @apply bg-a-gray-100;
    @apply rounded-lg border-transparent;
  }

  .menu.top {
    @apply -top-[4rem];
  }

  .menu.bottom {
    @apply top-12;
  }
</style>
