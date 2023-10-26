<script lang="ts">
  import { _ } from "svelte-i18n"
  import { Client, gql } from "@urql/svelte"

  import { page } from "$app/stores"

  import { UserRole } from "$lib/types/user.js"
  import type { User } from "$lib/types/user.js"

  import UserSecretSolid from "$components/icons/UserSecretSolid.svelte"
  import UserRegular from "$components/icons/UserRegular.svelte"
  import NavDropDown from "$components/Navbar/NavDropDown.svelte"
  import UserNurseSolid from "$components/icons/UserNurseSolid.svelte"
  import UserAstronautSolid from "$components/icons/UserAstronautSolid.svelte"

  let user: User | null
  $: user = $page.data.user

  let roles: { [key: number]: string }
  $: roles = {
    1: $_("Reporter"),
    2: $_("Editor"),
    3: $_("Administrator"),
  }

  const logout = async () => {
    const { error, data } = await ($page.data.urqlClient as Client)
      .mutation<{ logout: boolean }>(
        gql`
          mutation {
            logout
          }
        `,
        {},
      )
      .toPromise()

    if (error || !data) {
      console.error(error)
      return
    }
    if (data.logout) {
      location.reload()
    }
  }
</script>

{#if user}
  <div class="flex">
    <NavDropDown>
      <svelte:fragment slot="title">
        <div
          class="heading5 mx-auto my-auto flex h-fit w-fit content-center justify-center rounded-full bg-pelorous p-1.5 font-bold uppercase text-black"
        >
          {user.full_name
            ? user.full_name
                .split(" ")
                .map(x => x[0])
                .join("")
            : user.username.substring(0, 2)}
        </div>
      </svelte:fragment>

      <div class="divide-y divide-solid bg-white shadow-lg dark:bg-lm-black">
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
      class="button1 mx-3 hidden w-full text-left text-lm-black transition hover:text-orange dark:text-white xl:block"
      on:click|preventDefault={logout}
    >
      {$_("Logout")}
    </button>
  </div>
{:else}
  <div>
    <a
      class="button1 mx-3 w-fit rounded bg-orange py-2 px-10 text-white transition hover:bg-orange-600 hover:text-white"
      href="/account/login/?next={$page.url.pathname}"
      title={$_("Login/Register")}
    >
      Log in
    </a>
  </div>
{/if}
