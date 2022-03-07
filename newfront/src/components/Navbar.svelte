<script lang="ts">
  import { _ } from "svelte-i18n";
  import Cookies from "js-cookie";
  import {
    aboutPages,
    blogCategories,
    dispatchLogin,
    dispatchLogout,
    observatoryPages,
    user,
  } from "$lib/stores";
  import type { ObservatoryPage } from "$lib/types/wagtail";
  import UserAstronautSolid from "$components/icons/UserAstronautSolid.svelte";
  import UserNurseSolid from "$components/icons/UserNurseSolid.svelte";
  import UserSecretSolid from "$components/icons/UserSecretSolid.svelte";
  import { computePosition } from "@floating-ui/dom";
  import UserRegular from "$components/icons/UserRegular.svelte";
  import TranslateIcon from "$components/icons/TranslateIcon.svelte";

  const language = Cookies.get("django_language") ?? "en";
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

  function switchLanguage(locale: string) {}

  function showDropdown(e) {
    const referenceElement = e.currentTarget;
    const dropdownMenu = e.currentTarget.parentNode.querySelector(".dropdown-menu");

    function applyStyles({ x = 0, y = 0 }) {
      Object.assign(dropdownMenu.style, {
        display: "block",
        left: `${x}px`,
        top: `${y}px`,
      });
    }

    computePosition(referenceElement, dropdownMenu, {
      placement: "bottom",
    }).then(applyStyles);

    dropdownMenu.style.display = "block";

    const closeMenuClick = (e) => {
      if (e.target === dropdownMenu || dropdownMenu.contains(e.target)) return;
      dropdownMenu.style.display = "none";
      document.removeEventListener("click", closeMenuClick, true);
    };
    setTimeout(() => document.addEventListener("click", closeMenuClick, true), 100);
  }

  let username = "";
  let password = "";
  let login_failed_message = "";
  async function login() {
    const xx = await dispatchLogin(username, password);
    if (xx.status === true) await location.reload();
  }
  async function logout() {
    if (await dispatchLogout()) location.reload();
  }
  function closeMenu() {}
</script>

<nav class="sticky top-0 z-[1030] bg-white border-b-8 border-orange flex px-2">
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
        <li class="nav-item dropdown">
          <a class="nav-link" on:click={showDropdown} role="button">
            {$_("Data")}
          </a>
          <div class="dropdown-menu">
            {#each dataLinks as { name, href }}
              <a {href} on:click={closeMenu}>
                {$_(name)}
              </a>
            {/each}
          </div>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link" on:click={showDropdown} role="button">
            {$_("Observatories")}
          </a>
          <div class="dropdown-menu divide-y divide-solid">
            {#each Object.values(observatoriesGroups) as obs}
              <div>
                {#each obs as observatory}
                  <a href="/observatory/{observatory.meta.slug}" on:click={closeMenu}>
                    {observatory.title}
                  </a>
                {/each}
              </div>
            {/each}
          </div>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link" on:click={showDropdown} role="button">
            {$_("Resources")}
          </a>
          <div class="dropdown-menu">
            {#each $blogCategories as cat}
              <a href="/resources/?category={cat.slug}" on:click={closeMenu}>
                {$_(cat.name)}
              </a>
            {/each}
          </div>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link" on:click={showDropdown} role="button">
            {$_("About")}
          </a>
          <div class="dropdown-menu">
            {#each $aboutPages as { title, meta }}
              <a href="/about/{meta.slug}/" on:click={closeMenu}>
                {$_(title)}
              </a>
            {/each}
          </div>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/faq/" on:click={closeMenu}>
            {$_("FAQ")}
          </a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/contribute/" on:click={closeMenu}>
            {$_("Contribute")}
          </a>
        </li>
      </ul>
      <ul class="flex items-center ml-auto">
        <!--          <NavbarSearch />-->
        <li class="nav-item dropdown">
          <a class="nav-link" on:click={showDropdown} role="button">
            <TranslateIcon class="h-4 w-4 inline" />
            {languages[language]}
          </a>
          <div class="dropdown-menu">
            {#each Object.entries(languages) as [lcode, lingo]}
              <a
                class:active={lcode === language}
                on:click={() => switchLanguage(lcode)}
              >
                {lingo} ({lcode})
              </a>
            {/each}
          </div>
        </li>
        {#if $user}
          <li class="nav-item dropdown">
            <a on:click={showDropdown} class="nav-link flex items-center" role="button">
              {$user.initials}
              {#if $user.role === "ADMINISTRATOR"}
                <UserAstronautSolid class="h-4 w-4 inline" />
                <i class="fas fa-user-astronaut" />
              {:else if $user.role === "EDITOR"}
                <UserNurseSolid class="h-4 w-4 inline" />
                <i class="fas fa-user-nurse" />
              {:else if $user.is_impersonate}
                <UserSecretSolid class="h-4 w-4 inline" />
                <i class="fa fa-user-secret" />
              {:else}
                <i class="fa fa-user" />
              {/if}
            </a>
            <div aria-labelledby="#navbarDropdown" class="dropdown-menu ">
              <p class="pt-2 pl-4 text-gray-400 leading-5 mb-2">
                {$user.full_name}
                <br />
                <small>{$_($user.bigrole)}</small>
              </p>
              <hr />
              <!--suppress HtmlUnknownTarget -->
              {#if $user.is_impersonate}
                <a href="/impersonate/stop/?next=/dashboard/">
                  {$_("Stop impersonation")}
                </a>
                <hr />
              {/if}

              <a href="/manager/">
                {$_("Manage")}
              </a>
              <a href="/case_statistics/">
                {$_("Case statistics")}
              </a>
              <hr />
              <a href="/deal/add">
                {$_("Add a deal")}
              </a>
              <a on:click|preventDefault={logout}>
                {$_("Logout")}
              </a>
            </div>
          </li>
        {:else}
          <li class="nav-item dropdown">
            <a
              on:click={showDropdown}
              class="nav-link"
              role="button"
              title="Login/Register"
            >
              <UserRegular class="h-4 w-4 inline mx-1" />
            </a>
            <div class="dropdown-menu right-0">
              <form on:submit|preventDefault={login} class="px-4 pt-3">
                <div class="form-group">
                  <input
                    autocomplete="username"
                    class="inpt"
                    id="username"
                    placeholder="Username"
                    type="text"
                    bind:value={username}
                  />
                </div>
                <div class="form-group">
                  <input
                    autocomplete="current-password"
                    class="inpt"
                    id="password"
                    placeholder="Password"
                    type="password"
                    bind:value={password}
                  />
                </div>
                <button class="btn btn-secondary" type="submit">
                  {$_("Login")}
                </button>
                <p class="mt-3 text-danger small">{login_failed_message}</p>
              </form>
              <hr />
              <a href="/account/register/">
                {$_("New around here? Sign up")}
              </a>
              <a href="/account/password_reset/">
                {$_("Forgot password?")}
              </a>
            </div>
          </li>
        {/if}
      </ul>
    </div>
  </div>
</nav>

<style>
  .dropdown-menu {
    @apply absolute border border-orange bg-white hidden absolute;
    /*background-clip: padding-box;*/
    /*color: #212529;*/
    /*float: left;*/
    /*left: 0;*/
    /*list-style: none;*/
    /*margin: 0.125rem 0 0;*/
    /*min-width: 10rem;*/

    /*text-align: left;*/
    /*top: 100%;*/
    /*z-index: 1000;*/
  }

  .dropdown-menu a {
    @apply px-4 py-2 block text-black;
    @apply hover:bg-gray-200;
    @apply active:bg-orange active:text-white;
  }

  .nav-link {
    @apply text-black py-2 px-5 hover:text-orange;
  }

  .nav-item {
    @apply whitespace-nowrap;
  }

  /*.nav-item.dropdown {*/
  /*  @apply relative;*/
  /*}*/

  .nav-item.dropdown > a {
    @apply relative pr-[20px];
    @apply hover:text-orange;
  }

  .nav-item.dropdown > a::after {
    @apply inline-block;
    content: url("data:image/svg+xml; utf8, <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='none' viewBox='0 0 24 24' stroke='currentColor'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 12l-8 8-8-8' /></svg>");
  }

  .nav-item.dropdown > a:hover::after {
    content: url("data:image/svg+xml; utf8, <svg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='none' viewBox='0 0 24 24' stroke='%23fc941f'><path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 12l-8 8-8-8' /></svg>");
  }

  ul .a-exact-active {
    @apply bg-orange text-white;
  }
</style>
