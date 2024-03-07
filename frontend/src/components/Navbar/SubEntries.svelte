<script lang="ts">
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
  class="relative {$$props.class ?? ''}"
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
      class="hidden flex-wrap justify-around border-t bg-gray-50 py-1 group-focus-within:flex
       lg:absolute lg:z-50 lg:whitespace-nowrap lg:border-none lg:bg-white lg:py-3 lg:shadow-2xl lg:group-focus-within:hidden lg:group-hover:block
       dark:bg-gray-900 dark:shadow dark:shadow-orange dark:lg:bg-gray-900"
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
