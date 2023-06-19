<script lang="ts">
  import { _ } from "svelte-i18n"
  import cn from "classnames"

  import { page } from "$app/stores"

  import { blogCategories, aboutPages, observatoryPages, isDarkMode } from "$lib/stores"
  import { clickOutside } from "$lib/helpers"

  import BurgerMenuIcon from "$components/icons/BurgerMenuIcon.svelte"
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte"
  import NavbarSearch from "$components/Navbar/NavbarSearch.svelte"
  import LanguageSwitch from "$components/Navbar/LanguageSwitch.svelte"
  import LoginSection from "$components/Navbar/LoginSection.svelte"

  interface MenuEntry {
    title: string
    subEntries?: { title: string; href: string }[]
    href?: string
  }

  let menuEntries: MenuEntry[]
  $: menuEntries = [
    {
      title: $_("Data"),
      subEntries: [
        { title: $_("Map"), href: "/map/" },
        { title: $_("Deals"), href: "/list/deals/" },
        { title: $_("Investors"), href: "/list/investors/" },
        { title: $_("Charts"), href: "/charts/" },
      ],
    },
    {
      title: $_("Observatories"),
      subEntries: $observatoryPages.map(page => ({
        title: $_(page.title),
        href: `/observatory/${page.meta.slug}`,
      })),
    },
    {
      title: $_("Resources"),
      subEntries: $blogCategories.map(cat => ({
        title: $_(cat.name),
        href: `/resources/?category=${cat.slug}`,
      })),
    },
    {
      title: $_("About"),
      subEntries: $aboutPages.map(page => ({
        title: $_(page.title),
        href: `/about/${page.meta.slug}`,
      })),
    },
    { title: $_("FAQ"), href: "/faq/" },
    { title: $_("Contribute"), href: "/contribute/" },
  ]
  let menuHidden = true

  const resetMenu = () => {
    menuHidden = true
  }
</script>

<!--https://blog.logrocket.com/building-responsive-navbar-tailwind-css/-->
<nav
  class={cn(
    "h-full w-full p-1",
    "text-lg text-gray-700 dark:text-white",
    "bg-white dark:bg-gray-800",
    "border-b-8 border-b-orange",
  )}
>
  <div
    class="container mx-auto flex h-full w-full flex-wrap items-center justify-between align-middle"
  >
    <!--   LOGO   -->
    <a class="order-first mr-3 self-center lg:mr-10" href="/" on:click={resetMenu}>
      <img
        alt="Land Matrix"
        class="h-[36px] w-[144px] min-w-[144px] max-w-[144px]"
        src={$isDarkMode ? "/images/lm-logo-dark.png" : "/images/lm-logo.png"}
      />
    </a>

    <!--   MOBILE MENU   -->
    <ul id="menu-mobile" class="order-last flex flex-grow items-center justify-end">
      <li class="hidden xl:block">
        <NavbarSearch />
      </li>
      <li>
        <LanguageSwitch />
      </li>
      <li>
        <LoginSection />
      </li>
      <li class="xl:hidden">
        <button
          class="h-full p-2"
          on:click|stopPropagation={() => {
            menuHidden = !menuHidden
          }}
        >
          <BurgerMenuIcon class="inline h-7 w-7 text-lm-dark dark:text-lm-lightgray" />
        </button>
      </li>
    </ul>

    <!--   MENU   -->
    <div
      id="menu"
      class={cn(
        menuHidden ? "hidden xl:block" : "",
        "absolute xl:static",
        "top-[58px] left-0 z-50 w-full xl:w-auto",
        "bg-white dark:bg-gray-800",
        "border-b-8 border-orange xl:border-0",
      )}
      use:clickOutside
      on:outClick={resetMenu}
    >
      <ul
        class={cn(
          "divide-y divide-solid px-4",
          "xl:flex xl:items-center xl:justify-between xl:divide-transparent",
        )}
      >
        {#each menuEntries as entry, index}
          <li class="group xl:relative">
            {#if entry.subEntries}
              <button
                class="w-full truncate py-2 text-center text-black hover:text-orange dark:text-white xl:p-2"
                title={entry.title}
              >
                {entry.title}
                <ChevronDownIcon
                  class={cn("inline h-5 w-5", "group-hover:rotate-180")}
                />
              </button>
              <ul
                class={cn(
                  "hidden flex-wrap justify-around",
                  "bg-lm-lightgray dark:bg-gray-700 xl:bg-white dark:xl:bg-gray-800",
                  "xl:absolute xl:z-50 xl:whitespace-nowrap",
                  "border-t xl:border-2 xl:border-orange",
                  "group-focus-within:flex xl:group-focus-within:hidden xl:group-hover:block",
                )}
              >
                {#each entry.subEntries as subEntry, subIndex}
                  <li class="mx-7 xl:mx-0">
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
            {:else}
              <a
                class="nav-link truncate text-center xl:max-w-[120px]"
                title={entry.title}
                href={entry.href}
                on:click={resetMenu}
              >
                {entry.title}
              </a>
            {/if}
          </li>
        {/each}
      </ul>
    </div>
  </div>
</nav>

<style lang="postcss">
  :global(.nav-link) {
    @apply block p-2 text-black dark:text-white;
    @apply hover:bg-gray-200 hover:text-orange dark:hover:bg-gray-700;
    @apply active:bg-orange active:text-white;
  }

  :global(.nav-link.active) {
    @apply bg-orange text-white;
  }
</style>
