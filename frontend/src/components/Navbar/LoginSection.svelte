<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { showContextHelp } from "$lib/stores"
  import { UserRole } from "$lib/types/data"
  import { getCsrfToken } from "$lib/utils"

  import CheckboxSwitch from "$components/LowLevel/CheckboxSwitch.svelte"
  import NavDropDown from "$components/Navbar/NavDropDown.svelte"

  const user = $derived(page.data.user)

  const userRolesMap: { [role in UserRole]: string } = $derived({
    [UserRole.ANYBODY]: $_("Anybody"),
    [UserRole.REPORTER]: $_("Reporter"),
    [UserRole.EDITOR]: $_("Editor"),
    [UserRole.ADMINISTRATOR]: $_("Administrator"),
  })

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
  <div>
    <NavDropDown placement="right-0">
      {#snippet title()}
        <div
          class="heading5 m-2 flex h-10 w-10 items-center justify-center rounded-full bg-pelorous font-bold uppercase text-black md:h-12 md:w-12"
        >
          {user.full_name
            ? user.full_name
                .split(" ")
                .map(x => x[0])
                .join("")
            : user.username.substring(0, 2)}
        </div>
      {/snippet}

      <div class="divide-y divide-solid bg-white shadow-lg dark:bg-gray-900">
        <p class="m-0 whitespace-nowrap p-2 leading-5 text-gray-400">
          {user.full_name ?? user.username}
          <br />
          <small>{userRolesMap[user.role]}</small>
        </p>

        <ul>
          <li>
            <a class="nav-link-secondary" href="/management/">
              {$_("Manage")}
            </a>
          </li>
          <li class="whitespace-nowrap">
            <a class="nav-link-secondary" href="/statistics/">
              {$_("Data Statistics")}
            </a>
          </li>
          {#if page.data.user?.is_contexthelp_editor}
            <li class="whitespace-nowrap">
              <CheckboxSwitch
                class="nav-link-secondary"
                id="default"
                checked={$showContextHelp}
                onchange={() => showContextHelp.toggle()}
              >
                {$_("Context help")}
              </CheckboxSwitch>
            </li>
          {/if}
        </ul>
        <ul>
          <li>
            <a class="nav-link-secondary" href="/deal/add/">{$_("Add a deal")}</a>
          </li>
          <li>
            <a
              class="nav-link-secondary"
              target="_blank"
              href="https://doc.landmatrix.org"
            >
              {$_("Documentation")}
            </a>
          </li>
          <li>
            <a class="nav-link-secondary" href="/accountability/">
              {$_("VGGTs scoring")}
            </a>
          </li>
          <li>
            <button type="button" class="nav-link-secondary text-left" onclick={logout}>
              {$_("Logout")}
            </button>
          </li>
        </ul>
      </div>
    </NavDropDown>
  </div>
{:else}
  <div>
    <a
      class="btn btn-primary mx-1 w-fit px-3 py-1 sm:mx-3 sm:px-6 sm:py-2 lg:px-10"
      href="/account/login/?next={page.url.pathname}"
      title={$_("Login/Register")}
    >
      {$_("Login")}
    </a>
  </div>
{/if}
