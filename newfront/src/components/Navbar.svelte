<script lang="ts">
  import Cookies from "js-cookie"
  import { _, locale } from "svelte-i18n"

  import { page } from "$app/stores"

  import { aboutPages, blogCategories, fetchBasis, observatoryPages } from "$lib/stores"
  import { UserRole } from "$lib/types/user"
  import type { ObservatoryPage } from "$lib/types/wagtail"
  import { dispatchLogout } from "$lib/user"

  import TranslateIcon from "$components/icons/TranslateIcon.svelte"
  import UserAstronautSolid from "$components/icons/UserAstronautSolid.svelte"
  import UserNurseSolid from "$components/icons/UserNurseSolid.svelte"
  import UserRegular from "$components/icons/UserRegular.svelte"
  import UserSecretSolid from "$components/icons/UserSecretSolid.svelte"

  import NavDropDown from "./LowLevel/NavDropDown.svelte"
  import NavbarSearch from "./NavbarSearch.svelte"

  const languages = { en: "English", es: "Español", fr: "Français", ru: "Русский" }
  const dataLinks = [
    { name: $_("Map"), href: "/map" },
    { name: $_("Deals"), href: "/list/deals" },
    { name: $_("Investors"), href: "/list/investors" },
    { name: $_("Charts"), href: "/charts" },
  ]
  const roles = { 1: $_("Reporter"), 2: $_("Editor"), 3: $_("Administrator") }

  let observatoriesGroups = { global: [], regions: [], countries: [] }
  $observatoryPages.forEach((op: ObservatoryPage) => {
    if (op.country) observatoriesGroups.countries.push(op)
    else if (op.region) observatoriesGroups.regions.push(op)
    else observatoriesGroups.global.push(op)
  })

  async function switchLanguage(lang: string) {
    Cookies.set("django_language", lang)
    await locale.set(lang)
    await fetchBasis(lang, fetch, $page.data.urqlClient)
  }

  $: user = $page.data.user

  async function logout() {
    if (await dispatchLogout($page.data.urqlClient)) location.reload()
  }
</script>

<nav
  class="sticky top-0 z-[1030] flex border-b-8 border-orange bg-white px-2 dark:bg-gray-800"
>
  <div class="mx-6 flex w-full justify-between p-1 lg:container lg:mx-auto">
    <a class="mt-1 mr-6" href="/">
      <img
        alt="Land Matrix"
        class="h-[38px] w-[144px] min-w-[144px] max-w-[144px]"
        src="/images/lm-logo.png"
      />
    </a>
    <button
      class="inline-block rounded border border-transparent border-gray-600 bg-transparent py-1 px-3 leading-none text-gray-500 lg:hidden"
      data-target="#navbarCollapse"
      data-toggle="collapse"
      type="button"
    >
      <svg
        class="inline-block h-6 w-6 bg-center bg-no-repeat align-middle"
        viewBox="0 0 30 30"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M4 7h22M4 15h22M4 23h22"
          stroke="rgba(0,0,0,0.5)"
          stroke-linecap="round"
          stroke-miterlimit="10"
          stroke-width="2"
        />
      </svg>
    </button>
    <div class="hidden w-full flex-grow items-center lg:flex lg:w-auto">
      <ul class="flex w-full items-center">
        <NavDropDown title={$_("Data")}>
          <ul class="border border-orange bg-white dark:bg-gray-800">
            {#each dataLinks as { name, href }}
              <li class="whitespace-nowrap">
                <a {href} class="nav-link">
                  {name}
                </a>
              </li>
            {/each}
          </ul>
        </NavDropDown>

        <NavDropDown title={$_("Observatories")}>
          <div
            class="divide-y divide-solid border border-orange bg-white dark:bg-gray-800"
          >
            {#each Object.values(observatoriesGroups) as obs}
              <ul>
                {#each obs as observatory}
                  <li class="whitespace-nowrap">
                    <a class="nav-link" href="/observatory/{observatory.meta.slug}">
                      {observatory.title}
                    </a>
                  </li>
                {/each}
              </ul>
            {/each}
          </div>
        </NavDropDown>

        <NavDropDown title={$_("Resources")}>
          <ul class="border border-orange bg-white dark:bg-gray-800">
            {#each $blogCategories as cat}
              <li class="whitespace-nowrap">
                <a class="nav-link" href="/resources/?category={cat.slug}">
                  <!-- TODO: discuss replacing this somehow? comes from DB though -->
                  {$_(cat.name)}
                </a>
              </li>
            {/each}
          </ul>
        </NavDropDown>

        <NavDropDown title={$_("About")}>
          <ul class="border border-orange bg-white dark:bg-gray-800">
            {#each $aboutPages as { title, meta }}
              <li class="whitespace-nowrap">
                <a class="nav-link" href="/about/{meta.slug}/">
                  {title}
                </a>
              </li>
            {/each}
          </ul>
        </NavDropDown>

        <li>
          <a class="nav-link" href="/faq/">
            {$_("FAQ")}
          </a>
        </li>
        <li>
          <a class="nav-link" href="/contribute/">
            {$_("Contribute")}
          </a>
        </li>
      </ul>
      <ul class="ml-auto flex items-center">
        <NavbarSearch />

        <NavDropDown placement="right-0">
          <div slot="title" class="flex items-center gap-1 whitespace-nowrap">
            <TranslateIcon class="inline h-4 w-4" />
            {languages[$locale]}
          </div>

          <ul class="border border-orange bg-white dark:bg-gray-800">
            {#each Object.entries(languages) as [lcode, lingo]}
              <li class="whitespace-nowrap">
                <button
                  type="button"
                  class="nav-link w-full"
                  class:active={lcode === $locale}
                  on:click={() => switchLanguage(lcode)}
                >
                  {lingo} ({lcode})
                </button>
              </li>
            {/each}
          </ul>
        </NavDropDown>

        {#if user}
          <NavDropDown placement="right-0">
            <div slot="title" class="flex items-center gap-1 whitespace-nowrap">
              {user.full_name
                ? user.full_name
                    .split(" ")
                    .map(x => x[0])
                    .join("")
                : user.username.substring(0, 2)}
              {#if user.role === UserRole.ADMINISTRATOR}
                <UserAstronautSolid class="inline h-4 w-4" />
              {:else if user.role === UserRole.EDITOR}
                <UserNurseSolid class="inline h-4 w-4" />
              {:else if user.is_impersonate}
                <UserSecretSolid class="inline h-4 w-4" />
              {:else}
                <UserRegular class="inline h-4 w-4" />
              {/if}
            </div>

            <div
              class="divide-y divide-solid border border-orange bg-white dark:bg-gray-800"
            >
              <p class="mb-2 whitespace-nowrap pt-2 pl-2 leading-5 text-gray-400">
                {user.full_name}
                <br />
                <small>{user.role ? roles[user.role] : ""}</small>
              </p>

              {#if user.is_impersonate}
                <ul>
                  <li>
                    <a class="nav-link" href="/impersonate/stop/?next=/dashboard/">
                      {$_("Stop impersonation")}
                    </a>
                  </li>
                </ul>
              {/if}

              <ul>
                <li>
                  <a class="nav-link" href="/management/">
                    {$_("Manage")}
                  </a>
                </li>
                <li class="whitespace-nowrap">
                  <a
                    class="nav-link"
                    href="/management/case_statistics/"
                    data-sveltekit-reload
                  >
                    {$_("Case statistics")}
                  </a>
                </li>
              </ul>
              <ul>
                <li>
                  <a class="nav-link" href="/deal/add">{$_("Add a deal")}</a>
                </li>
                <li>
                  <button
                    type="button"
                    class="nav-link w-full text-left"
                    on:click|preventDefault={logout}
                  >
                    {$_("Logout")}
                  </button>
                </li>
              </ul>
            </div>
          </NavDropDown>
        {:else}
          <li>
            <a
              class="nav-link hover:bg-gray-100 hover:text-orange-500"
              href="/account/login/?next={$page.url.pathname}"
              title="Login/Register"
            >
              <UserRegular class="h-5 w-5" />
            </a>
          </li>
        {/if}
      </ul>
    </div>
  </div>
</nav>

<style lang="postcss">
  :global(.nav-link) {
    @apply block px-4 py-2 text-black dark:text-white;
    @apply hover:bg-gray-200 hover:text-orange dark:hover:bg-gray-600;
    @apply active:bg-orange active:text-white;
  }

  :global(.nav-link.active) {
    @apply bg-orange text-white;
  }
</style>
