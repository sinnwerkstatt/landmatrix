<script lang="ts">
  import { slide } from "svelte/transition"

  import { afterNavigate } from "$app/navigation"
  import { page } from "$app/state"

  import { clickOutside } from "$lib/helpers"

  interface NavLink {
    title: string
    href: string
  }

  interface Props {
    subEntries?: NavLink[]
    title: string
    class?: string
    onCloseMenu?: () => void
  }

  let { subEntries = [], title, class: className = "", onCloseMenu }: Props = $props()

  let isActive = $derived((subEntry: NavLink): boolean => {
    const pathname = page.url.pathname
    return pathname.startsWith("/resources/")
      ? pathname + page.url.search === subEntry.href
      : pathname.startsWith(subEntry.href)
  })

  let isOpen = $state(false)
  let isHover = $state(false)

  afterNavigate(() => (isOpen = false))
</script>

<li class="group py-1">
  <div
    role="menu"
    tabindex="-1"
    class="relative {className}"
    use:clickOutside
    onoutClick={() => (isOpen = false)}
    onmouseenter={() => (isHover = true)}
    onmouseleave={() => {
      isHover = false
      isOpen = false
    }}
  >
    <button
      class="nav-link-main"
      {title}
      onclick={() => (isOpen = !isOpen)}
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
              onclick={onCloseMenu}
            >
              {subEntry.title}
            </a>
          </li>
        {/each}
      </ul>
    {/if}
  </div>
</li>
