<script lang="ts">
  import cn from "classnames"
  import { _ } from "svelte-i18n"

  import { clickOutside } from "$lib/helpers"
  import { aboutPages, blogCategories, isDarkMode, observatoryPages } from "$lib/stores"

  import BurgerMenuIcon from "$components/icons/BurgerMenuIcon.svelte"
  import LanguageSwitch from "$components/Navbar/LanguageSwitch.svelte"
  import LoginSection from "$components/Navbar/LoginSection.svelte"
  import NavbarSearch from "$components/Navbar/NavbarSearch.svelte"
  import SubEntries from "$components/Navbar/SubEntries.svelte"

  import { isSubMenu } from "./navbar"
  import type { MenuEntry } from "./navbar"

  let menuEntries: MenuEntry[]
  $: menuEntries = [
    {
      title: $_("Data"),
      subEntries: [
        { title: $_("Map"), href: "/map/" },
        { title: $_("Tables"), href: "/list/" },
        { title: $_("Charts"), href: "/charts/" },
      ],
    },
    {
      title: $_("Observatories"),
      subEntries: $observatoryPages.map(page => ({
        title: $_(page.title),
        href: `/observatory/${page.meta.slug}/`,
      })),
    },
    {
      title: $_("Resources"),
      subEntries: [
        {
          title: $_("All"),
          href: "/resources/",
        },
        ...$blogCategories.map(cat => ({
          title: $_(cat.name),
          href: `/resources/?category=${cat.slug}`,
        })),
      ],
    },
    {
      title: $_("About"),
      subEntries: $aboutPages.map(page => ({
        title: $_(page.title),
        href: `/about/${page.meta.slug}/`,
      })),
    },
    { title: $_("FAQ"), href: "/faq/" },
    { title: $_("Contribute"), href: "/contribute/" },
  ]

  let menuHidden = true

  const resetMenu = () => {
    menuHidden = true
  }
  const closeMenu = () => {
    menuHidden = true
  }
</script>

<!--https://blog.logrocket.com/building-responsive-navbar-tailwind-css/-->
<nav
  class="h-full w-full bg-white p-1 py-1 text-lg text-gray-700 shadow-lg dark:bg-gray-700 dark:text-white"
>
  <div class="mx-auto flex h-full w-full items-center justify-between align-middle">
    <!--   LOGO   -->
    <a class="order-first mr-3 self-center xl:mr-10" href="/" on:click={resetMenu}>
      <img
        alt="Land Matrix"
        class="ml-3 hidden h-[36px] w-[144px] min-w-[144px] max-w-[144px] md:block"
        src={$isDarkMode ? "/images/lm-logo-dark.png" : "/images/lm-logo.png"}
      />
      <img
        alt="Land Matrix"
        class="ml-3 h-[48px] max-w-[144px] sm:mr-3 md:hidden"
        src={$isDarkMode
          ? "/images/lm-logo-mobile-dark.png"
          : "/images/lm-logo-mobile.png"}
      />
    </a>

    <!--   MOBILE MENU   -->
    <ul
      id="menu-mobile"
      class="order-last flex max-w-fit flex-grow items-center justify-end"
    >
      <li>
        <NavbarSearch />
      </li>
      <li>
        <LanguageSwitch />
      </li>
      <li>
        <LoginSection />
      </li>
      <li class="2xl:hidden">
        <button
          class="h-full p-2"
          on:click|stopPropagation={() => {
            menuHidden = !menuHidden
          }}
        >
          <BurgerMenuIcon class="mx-3 inline h-7 w-7 text-black dark:text-gray-50" />
        </button>
      </li>
    </ul>

    <!--   MENU   -->
    <div
      id="menu"
      class={cn(
        menuHidden ? "hidden 2xl:block" : "",
        "absolute xl:static",
        "left-0 top-[65px] z-50 w-full xl:w-auto",
        "bg-white dark:bg-gray-800",
        "shadow-lg xl:shadow-none",
      )}
      use:clickOutside
      on:outClick={resetMenu}
    >
      <ul
        class="gap-y-6 divide-y divide-solid p-6 px-4 lg:flex
         lg:flex-wrap lg:items-center lg:justify-center lg:gap-x-12 lg:gap-y-0 lg:divide-transparent lg:p-0 xl:justify-between
         xl:gap-x-0 dark:bg-gray-700"
      >
        {#each menuEntries as entry}
          <li class="group xl:relative">
            {#if isSubMenu(entry)}
              <SubEntries
                title={entry.title}
                subEntries={entry.subEntries}
                on:close={closeMenu}
              />
            {:else}
              <a
                class="nav-link button1 3xl:max-w-none truncate text-center hover:bg-white hover:text-orange 2xl:max-w-[160px] dark:hover:bg-gray-700"
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
