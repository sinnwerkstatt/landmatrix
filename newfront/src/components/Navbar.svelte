<script lang="ts">
  import Cookies from "js-cookie";
  import { _, locale } from "svelte-i18n";
  import { page } from "$app/stores";
  import {
    aboutPages,
    blogCategories,
    fetchBasis,
    observatoryPages,
  } from "$lib/stores";
  import { UserLevel } from "$lib/types/user";
  import type { ObservatoryPage } from "$lib/types/wagtail";
  import { dispatchLogin, dispatchLogout } from "$lib/user";
  import TranslateIcon from "$components/icons/TranslateIcon.svelte";
  import UserAstronautSolid from "$components/icons/UserAstronautSolid.svelte";
  import UserNurseSolid from "$components/icons/UserNurseSolid.svelte";
  import UserRegular from "$components/icons/UserRegular.svelte";
  import UserSecretSolid from "$components/icons/UserSecretSolid.svelte";
  import NavDropDown from "./LowLevel/NavDropDown.svelte";
  import NavbarSearch from "./NavbarSearch.svelte";

  let language = Cookies.get("django_language") ?? "en";
  const languages = { en: "English", es: "Español", fr: "Français", ru: "Русский" };
  const dataLinks = [
    { name: "Map", href: "/map" },
    { name: "Deals", href: "/list/deals" },
    { name: "Investors", href: "/list/investors" },
    { name: "Charts", href: "/charts" },
  ];

  let observatoriesGroups = { global: [], regions: [], countries: [] };
  $observatoryPages.forEach((op: ObservatoryPage) => {
    if (op.country) observatoriesGroups.countries.push(op);
    else if (op.region) observatoriesGroups.regions.push(op);
    else observatoriesGroups.global.push(op);
  });

  async function switchLanguage(lang: string) {
    language = lang;
    Cookies.set("django_language", lang);
    await locale.set(lang);
    await fetchBasis(lang, $page.data.urqlClient);
  }

  let username = "";
  let password = "";
  let login_failed_message = "";

  $: user = $page.data.user;

  async function login() {
    const res = await dispatchLogin(username, password, $page.data.urqlClient);
    if (res.status === true) await location.reload();
  }

  async function logout() {
    if (await dispatchLogout($page.data.urqlClient)) location.reload();
  }
</script>

<nav
  class="sticky top-0 z-[1030] bg-white dark:bg-gray-800 border-b-8 border-orange flex px-2"
>
  <div class="mx-6 w-full lg:container lg:mx-auto flex justify-between p-1">
    <a class="mt-1 mr-6" href="/">
      <img
        alt="Land Matrix"
        class="h-[38px] w-[144px] min-w-[144px] max-w-[144px]"
        src="/images/lm-logo.png"
      />
    </a>
    <button
      class="inline-block py-1 px-3 leading-none bg-transparent border border-transparent rounded text-gray-500 border-gray-600 lg:hidden"
      data-target="#navbarCollapse"
      data-toggle="collapse"
      type="button"
    >
      <svg
        class="inline-block w-6 h-6 align-middle bg-center bg-no-repeat"
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
                  {$_(name)}
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
                  {$_(title)}
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
      <ul class="flex items-center ml-auto">
        <NavbarSearch />

        <NavDropDown placement="right-0">
          <div slot="title" class="whitespace-nowrap flex items-center gap-1">
            <TranslateIcon class="h-4 w-4 inline" />
            {languages[language]}
          </div>

          <ul class="border border-orange bg-white dark:bg-gray-800">
            {#each Object.entries(languages) as [lcode, lingo]}
              <li class="whitespace-nowrap">
                <a
                  class="nav-link"
                  class:active={lcode === language}
                  on:click={() => switchLanguage(lcode)}
                >
                  {lingo} ({lcode})
                </a>
              </li>
            {/each}
          </ul>
        </NavDropDown>

        {#if user}
          <NavDropDown placement="right-0">
            <div slot="title" class="whitespace-nowrap flex items-center gap-1">
              {user.initials}
              {#if user.level === UserLevel.ADMINISTRATOR}
                <UserAstronautSolid class="h-4 w-4 inline" />
              {:else if user.level === UserLevel.EDITOR}
                <UserNurseSolid class="h-4 w-4 inline" />
              {:else if user.is_impersonate}
                <UserSecretSolid class="h-4 w-4 inline" />
              {:else}
                <UserRegular class="h-4 w-4 inline" />
              {/if}
            </div>

            <div
              class="divide-y divide-solid border border-orange bg-white dark:bg-gray-800"
            >
              <p class="pt-2 pl-2 text-gray-400 leading-5 mb-2 whitespace-nowrap">
                {user.full_name}
                <br />
                <small>{user?.role ? $_(user?.role) : ""}</small>
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
                  <a class="nav-link" href="/case_statistics/">
                    {$_("Case statistics")}
                  </a>
                </li>
              </ul>
              <ul>
                <li>
                  <a class="nav-link" href="/deal/add">{$_("Add a deal")}</a>
                </li>
                <li>
                  <a class="nav-link" on:click|preventDefault={logout}>
                    {$_("Logout")}
                  </a>
                </li>
              </ul>
            </div>
          </NavDropDown>
        {:else}
          <NavDropDown placement="right-0">
            <div slot="title" class="whitespace-nowrap" title="Login/Register">
              <UserRegular class="h-4 w-4 inline mx-1" />
            </div>
            <div
              class="divide-y divide-solid border border-orange bg-white dark:bg-gray-800"
            >
              <form on:submit|preventDefault={login} class="px-4 pt-3 space-y-2">
                <input
                  autocomplete="username"
                  class="inpt"
                  id="username"
                  placeholder="Username"
                  type="text"
                  bind:value={username}
                />
                <input
                  autocomplete="current-password"
                  class="inpt"
                  id="password"
                  placeholder="Password"
                  type="password"
                  bind:value={password}
                />
                <button class="btn btn-secondary" type="submit">
                  {$_("Login")}
                </button>
                <p class="mt-3 text-danger small">{login_failed_message}</p>
              </form>
              <ul>
                <li class="whitespace-nowrap">
                  <a class="nav-link" href="/account/register/">
                    {$_("New around here? Sign up")}
                  </a>
                </li>
                <li class="whitespace-nowrap">
                  <a class="nav-link" href="/account/password_reset/">
                    {$_("Forgot password?")}
                  </a>
                </li>
              </ul>
            </div>
          </NavDropDown>
        {/if}
      </ul>
    </div>
  </div>
</nav>

<style>
  :global(.nav-link) {
    @apply px-4 py-2 block text-black dark:text-white;
    @apply hover:bg-gray-200 dark:hover:bg-gray-600;
    @apply active:bg-orange active:text-white;
  }

  :global(.nav-link.active) {
    @apply bg-orange text-white;
  }
</style>
