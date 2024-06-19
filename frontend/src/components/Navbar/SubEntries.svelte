<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { slide } from "svelte/transition"

  import { afterNavigate } from "$app/navigation"
  import { page } from "$app/stores"

  import { clickOutside } from "$lib/helpers"

  interface NavLink {
    title: string
    href: string
  }

  export let subEntries: NavLink[] = []
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

<li class="group py-1">
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
      class="nav-link-main"
      {title}
      on:click={() => (isOpen = !isOpen)}
      class:active={subEntries.find(subEntry => isActive(subEntry))}
    >
      {title}
    </button>

    {#if isOpen || isHover}
      <ul
        transition:slide={{ duration: 200 }}
        class="hidden flex-wrap justify-around bg-white group-focus-within:flex
       lg:absolute lg:z-50 lg:whitespace-nowrap lg:bg-white lg:shadow-2xl lg:group-focus-within:hidden lg:group-hover:block
       dark:bg-gray-900 dark:lg:border dark:lg:border-orange dark:lg:bg-gray-900 dark:lg:shadow-none"
      >
        {#each subEntries as subEntry}
          <li>
            <a
              class="nav-link-secondary"
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
</li>
