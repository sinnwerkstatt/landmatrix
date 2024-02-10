<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { slide } from "svelte/transition"

  import { afterNavigate } from "$app/navigation"
  import { page } from "$app/stores"

  import { clickOutside } from "$lib/helpers"

  const dispatch = createEventDispatcher()
  export let subEntries: {
    title: string
    href: string
  }[]
  export let title: string
  export let href: string

  let isOpen = false
  let isHover = false
  afterNavigate(() => (isOpen = false))

  const resetMenu = () => dispatch("close")
</script>

<li class="group xl:relative">
  {#if subEntries}
    <div
      class="relative {$$props.class}"
      use:clickOutside
      on:outClick={() => (isOpen = false)}
      on:mouseenter={() => (isHover = true)}
      on:mouseleave={() => {
        isHover = false
        isOpen = false
      }}
      role="navigation"
    >
      <button
        class="button1 w-full truncate py-2 text-center text-black xl:p-2 dark:text-white"
        {title}
        on:click={() => (isOpen = !isOpen)}
      >
        {#if title === "Resources"}<a
            class="text-gray-900 hover:text-orange"
            href="/resources/"
          >
            {title}
          </a>{:else}
          {title}{/if}
      </button>
      {#if isOpen || isHover}
        <ul
          transition:slide={{ duration: 200 }}
          class="hidden flex-wrap justify-around border-t bg-gray-50 py-3 group-focus-within:flex lg:absolute lg:z-50 lg:whitespace-nowrap lg:border-none lg:bg-white lg:shadow-nav lg:group-focus-within:hidden lg:group-hover:block dark:bg-gray-900 dark:lg:bg-gray-900"
        >
          {#each subEntries as subEntry}
            <li class="mx-7 lg:mx-0 lg:px-6 lg:hover:bg-orange-100">
              <a
                class="nav-link"
                class:active={$page.url.pathname.startsWith(subEntry.href)}
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
  {:else}
    <a
      class="nav-link button1 truncate text-center hover:bg-white hover:text-orange xl:max-w-[120px] dark:hover:bg-gray-900"
      {title}
      href={title === "Resources" ? "/resources/" : href}
      on:click={resetMenu}
    >
      {title}
    </a>
  {/if}
</li>
