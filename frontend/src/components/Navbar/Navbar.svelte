<script lang="ts">
  import { toggleDarkMode } from "$lib/stores/basics"

  import BurgerMenuIcon from "$components/icons/BurgerMenuIcon.svelte"
  import MoonSolidIcon from "$components/icons/MoonSolidIcon.svelte"
  import SearchIcon from "$components/icons/SearchIcon.svelte"
  import SunSolidIcon from "$components/icons/SunSolidIcon.svelte"
  import Modal from "$components/Modal.svelte"
  import LanguageSwitch from "$components/Navbar/LanguageSwitch.svelte"
  import LoginSection from "$components/Navbar/LoginSection.svelte"
  import NavbarLinks from "$components/Navbar/NavbarLinks.svelte"
  import NavbarSearch from "$components/Navbar/NavbarSearch.svelte"

  let showMenu = false

  let showSearch = false
</script>

<!--https://blog.logrocket.com/building-responsive-navbar-tailwind-css/-->
<nav
  class="sticky top-0 z-50 min-h-16 bg-white shadow-lg dark:border-b dark:border-orange dark:bg-gray-900 dark:text-white"
>
  <div class="float-left ml-3 flex h-16 items-center">
    <a class="order-first self-center" href="/" on:click={() => (showMenu = false)}>
      <img
        alt="Land Matrix"
        class="hidden h-[36px] md:block dark:md:hidden"
        src="/images/lm-logo.png"
      />
      <img
        alt="Land Matrix"
        class=" hidden h-[36px] md:hidden dark:md:inline-block"
        src="/images/lm-logo-dark.png"
      />
      <img
        alt="Land Matrix"
        class="h-[48px] sm:mr-3 md:hidden dark:hidden"
        src="/images/lm-logo-mobile.png"
      />
      <img
        alt="Land Matrix"
        class="hidden h-[48px] sm:mr-3 md:hidden dark:inline-block dark:md:hidden"
        src="/images/lm-logo-mobile-dark.png"
      />
    </a>
  </div>

  <ul class="float-right mr-3 flex h-16 items-center justify-end gap-1">
    <li>
      <div class="navbar-search md:hidden">
        <button class="flex items-center" on:click={() => (showSearch = true)}>
          <SearchIcon class="h-6 w-6" />
        </button>
        <Modal
          bind:open={showSearch}
          class="h-[80vh] w-[clamp(300px,90%,800px)]"
          dismissible
        >
          <NavbarSearch on:enter={() => (showSearch = false)} />
        </Modal>
      </div>
      <div class="navbar-search hidden w-48 md:block">
        <NavbarSearch />
      </div>
    </li>
    <li>
      <LanguageSwitch />
    </li>
    <li class="flex items-center">
      <button on:click={toggleDarkMode}>
        <SunSolidIcon class="h-6 w-6 dark:hidden" />
        <MoonSolidIcon class="hidden h-6 w-6 dark:block" />
      </button>
    </li>
    <li>
      <LoginSection />
    </li>
    <li class="lg:hidden">
      <button class="h-full" on:click|stopPropagation={() => (showMenu = !showMenu)}>
        <BurgerMenuIcon class="mx-1 inline h-7 w-7 text-black dark:text-gray-50" />
      </button>
    </li>
  </ul>

  <span
    class="absolute inset-x-0 top-full clear-both w-full max-w-full bg-white shadow-nav
     lg:static lg:h-16 lg:w-auto lg:px-3 lg:shadow-none 2xl:px-6
     dark:border-b-2 dark:border-orange dark:bg-gray-900 dark:lg:border-b-0
     {showMenu ? 'block lg:inline-block' : 'hidden lg:inline-block'}"
  >
    <NavbarLinks bind:showMenu />
  </span>
</nav>
