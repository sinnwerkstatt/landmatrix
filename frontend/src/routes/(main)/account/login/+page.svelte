<script lang="ts">
  import { gql } from "@urql/svelte"
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import type { User } from "$lib/types/user"

  import PageTitle from "$components/PageTitle.svelte"

  let username = ""
  let password = ""
  let login_failed_message = ""

  let logged_in = false
  let next = $page.url.searchParams.get("next") || "/"

  async function login() {
    const ret = await $page.data.urqlClient
      .mutation<{ login: { status: string; error: string; user: User } }>(
        gql`
          mutation Login($username: String!, $password: String!) {
            login(username: $username, password: $password) {
              status
              error
              user {
                id
                username
                full_name
                is_authenticated
                is_impersonate
                role
                country {
                  id
                  name
                }
                region {
                  id
                  name
                }
                groups {
                  id
                  name
                }
              }
            }
          }
        `,
        { username, password },
      )
      .toPromise()
    if (ret.error) {
      return toast.push(`Unknown Problem: ${ret.error}`, { classes: ["error"] })
    }
    if (!ret.data) {
      return toast.push(`Unknown Problem: ${ret.error}`, { classes: ["error"] })
    }

    if (ret.data.login.status) {
      login_failed_message = ""
      logged_in = true
      setTimeout(() => (window.location.href = next), 100)
      // can't do this, because it's hard to populate "user" back to layout:
      // setTimeout(() => goto(next), 100);
    } else {
      login_failed_message = ret.data.login.error
    }
  }
</script>

<PageTitle class="">{$_("Login")}</PageTitle>

{#if logged_in}
  <p class="mt-3 text-green-700">
    {$_("Login successful.")}
  </p>
{:else}
  <p class="mt-3 text-red-500">
    {login_failed_message}
  </p>
{/if}

<form class="text-gray-700 dark:text-white" on:submit|preventDefault={login}>
  <label class="mb-6 block">
    {$_("Username")}
    <input
      bind:value={username}
      autocomplete="username"
      class="inpt"
      placeholder={$_("Username")}
      type="text"
    />
  </label>
  <label class="mb-6 block">
    {$_("Password")}
    <input
      bind:value={password}
      autocomplete="current-password"
      class="inpt"
      placeholder={$_("Password")}
      type="password"
    />
  </label>
  <div class="-mt-5 mb-6 whitespace-nowrap text-right text-sm">
    <a href="/account/password_reset/">
      {$_("Forgot password?")}
    </a>
  </div>
  <button class="btn btn-primary w-full" type="submit">
    {$_("Login")}
  </button>
</form>
<div class="mt-12 text-right">
  <a href="/account/register/">
    {$_("New around here? Sign up")}
  </a>
</div>
