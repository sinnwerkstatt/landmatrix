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
    subEntries?: {
      title: string
      href: string
    }[]
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
    "bg-white dark:bg-lm-black",
    "py-1 shadow-lg",
  )}
>
  <div
    class="container mx-auto flex h-full w-full flex-wrap items-center justify-between align-middle"
  >
    <!--   LOGO   -->
    <a class="order-first mr-3 self-center xl:mr-10" href="/" on:click={resetMenu}>
      <img
        alt="Land Matrix"
        class="hidden h-[36px] w-[144px] min-w-[144px] max-w-[144px] md:block"
        src={$isDarkMode ? "/images/lm-logo-dark.png" : "/images/lm-logo.png"}
      />
      <img
        alt="Land Matrix"
        class="mx-3 h-[48px] max-w-[144px] md:hidden"
        src={$isDarkMode
          ? "/images/lm-logo-mobile-dark.png"
          : "/images/lm-logo-mobile.png"}
      />
    </a>

    <!--   MOBILE MENU   -->
    <ul id="menu-mobile" class="order-last flex flex-grow items-center justify-end">
      <li class="hidden sm:block">
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
          <BurgerMenuIcon
            class="mx-3 inline h-7 w-7 text-black dark:text-lm-lightgray"
          />
        </button>
      </li>
    </ul>

    <!--   MENU   -->
    <div
      id="menu"
      class={cn(
        menuHidden ? "hidden xl:block" : "",
        "absolute xl:static",
        "left-0 top-[58px] z-50 w-full xl:w-auto",
        "bg-white dark:bg-gray-800",
        "shadow-lg xl:shadow-none",
      )}
      use:clickOutside
      on:outClick={resetMenu}
    >
      <ul
        class={cn(
          "divide-y divide-solid px-4",
          "gap-y-6 p-6 dark:bg-lm-black lg:flex lg:flex-wrap lg:items-center lg:justify-center lg:gap-y-0 lg:gap-x-12 lg:divide-transparent lg:p-0 xl:justify-between xl:gap-x-0",
        )}
      >
        {#each menuEntries as entry}
          <li class="group xl:relative">
            {#if entry.subEntries}
              <button
                class="button1 w-full truncate py-2 text-center text-black hover:text-orange dark:text-white xl:p-2"
                title={entry.title}
              >
                {entry.title}
              </button>
              <ul
                class={cn(
                  "hidden flex-wrap justify-around",
                  "bg-lm-lightgray dark:bg-lm-black lg:bg-white dark:lg:bg-lm-black",
                  "lg:absolute lg:z-50 lg:whitespace-nowrap",
                  "border-t py-3 lg:border-none lg:shadow-2xl",
                  "group-focus-within:flex lg:group-focus-within:hidden lg:group-hover:block",
                )}
              >
                {#each entry.subEntries as subEntry}
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
            {:else}
              <a
                class="nav-link button1 truncate text-center hover:bg-white hover:text-orange dark:hover:bg-lm-black xl:max-w-[120px]"
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
    @apply lg:hover:bg-orange-100 lg:hover:text-black;
    /*@apply active:bg-orange active:text-white;*/
  }

  :global(.nav-link.active) {
    @apply font-bold text-orange;
  }
</style>
