<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { User } from "$lib/types/user.js"
  import { getCsrfToken } from "$lib/utils"

  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  let user: User | null
  $: user = $page.data.user

  let roles: { [key: number]: string }
  $: roles = {
    1: $_("Reporter"),
    2: $_("Editor"),
    3: $_("Administrator"),
  }

  const logout = async () => {
    const ret = await fetch("/api/user/logout/", {
      method: "POST",
      credentials: "include",
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    if (ret.ok) location.reload()
    else console.log(await ret.json())
  }
</script>

{#if user}
  <div class="flex">
    <NavDropDown>
      <svelte:fragment slot="title">
        <div
          class="heading5 mx-auto my-auto flex h-10 w-10 items-center justify-center rounded-full bg-pelorous font-bold uppercase text-black md:h-12 md:w-12"
        >
          {user.full_name
            ? user.full_name
                .split(" ")
                .map(x => x[0])
                .join("")
            : user.username.substring(0, 2)}
        </div>
      </svelte:fragment>

      <div class="divide-y divide-solid bg-white shadow-lg dark:bg-gray-900">
        <p class="m-0 whitespace-nowrap p-2 leading-5 text-gray-400">
          {user.full_name}
          <br />
          <small>{user.role ? roles[user.role] : ""}</small>
        </p>

        {#if user.is_impersonate}
          <ul>
            <li>
              <a
                class="nav-link hover:bg-pelorous-100"
                href="/impersonate/stop/?next=/dashboard/"
              >
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
              href="/management/case_statistics"
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
    <button
      type="button"
      class="button1 hidden w-full text-left text-gray-900 transition hover:text-orange sm:mx-3 xl:block dark:text-white"
      on:click|preventDefault={logout}
    >
      {$_("Logout")}
    </button>
  </div>
{:else}
  <div>
    <a
      class="button1 w-fit rounded bg-orange px-3 py-1 text-white transition hover:bg-orange-600 hover:text-white sm:mx-3 sm:px-6 sm:py-2 lg:px-10"
      href="/account/login/?next={$page.url.pathname}"
      title={$_("Login/Register")}
    >
      Log in
    </a>
  </div>
{/if}
