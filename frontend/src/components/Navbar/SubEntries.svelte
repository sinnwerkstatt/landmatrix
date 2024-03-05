<script lang="ts">
  import cn from "classnames"
  import { createEventDispatcher } from "svelte"
  import { slide } from "svelte/transition"

  import { afterNavigate } from "$app/navigation"
  import { page } from "$app/stores"

  import { clickOutside } from "$lib/helpers"

  import type { NavLink } from "./navbar"

  export let subEntries: NavLink[]
  export let title: string

  $: isActive = (subEntry: NavLink): boolean => {
    const pathname = $page.url.pathname
    return pathname.startsWith("/resources/")
      ? pathname + $page.url.search === subEntry.href
      : pathname.startsWith(subEntry.href)
  }

  let isOpen = false
  let isHover = false

  const dispatch = createEventDispatcher()

  const resetMenu = (): void => {
    dispatch("close")
  }

  afterNavigate(() => (isOpen = false))
</script>

<div
  role="menu"
  tabindex="-1"
  class="relative {$$props.class}"
  use:clickOutside
  on:outClick={() => (isOpen = false)}
  on:mouseenter={() => (isHover = true)}
  on:mouseleave={() => {
    isHover = false
    isOpen = false
  }}
>
  <button
    class="button1 w-full truncate py-2 text-center text-black xl:p-2 dark:text-white"
    {title}
    on:click={() => (isOpen = !isOpen)}
  >
    {title}
  </button>
  {#if isOpen || isHover}
    <ul
      transition:slide={{ duration: 200 }}
      class={cn(
        "hidden flex-wrap justify-around",
        "bg-gray-50 lg:bg-white dark:bg-gray-700 dark:lg:bg-gray-700",
        "lg:absolute lg:z-50 lg:whitespace-nowrap",
        "border-t py-1 lg:border-none lg:py-3 lg:shadow-2xl",
        "group-focus-within:flex lg:group-focus-within:hidden lg:group-hover:block",
      )}
    >
      {#each subEntries as subEntry}
        <li class="mx-3 lg:mx-0 lg:px-6 lg:hover:bg-orange-100">
          <a
            class="nav-link"
            class:active={isActive(subEntry)}
            href={subEntry.href}
            on:click={resetMenu}
          >
            {subEntry.title}
          </a>
        </li>
      {/each}
    </ul>
  {/if}
</div>
