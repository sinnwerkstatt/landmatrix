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
  <NavDropDown>
    <svelte:fragment slot="title">
      <span class="pr-1">
        {user.full_name
          ? user.full_name
              .split(" ")
              .map(x => x[0])
              .join("")
          : user.username.substring(0, 2)}
      </span>
      {#if user.role === UserRole.ADMINISTRATOR}
        <UserAstronautSolid class="inline h-4 w-4" />
      {:else if user.role === UserRole.EDITOR}
        <UserNurseSolid class="inline h-4 w-4" />
      {:else if user.is_impersonate}
        <UserSecretSolid class="inline h-4 w-4" />
      {:else}
        <UserRegular class="inline h-4 w-4" />
      {/if}
    </svelte:fragment>

    <div class="divide-y divide-solid border-2 border-orange bg-white dark:bg-gray-800">
      <p class="m-0 whitespace-nowrap p-2 leading-5 text-gray-400">
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
          <a class="nav-link" href="/management/case_statistics" data-sveltekit-reload>
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
  <div class="transition hover:scale-[105%]">
    <a
      class="button1 mx-3 w-fit rounded bg-orange py-2 px-10 text-white hover:text-white"
      href="/account/login/?next={$page.url.pathname}"
      title={$_("Login/Register")}
    >
      Log in
    </a>
  </div>
{/if}
