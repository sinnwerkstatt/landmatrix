<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { dispatchLogin } from "$lib/user"

  import PageTitle from "$components/PageTitle.svelte"

  let username = ""
  let password = ""
  let login_failed_message = ""

  let logged_in = false
  let next = $page.url.searchParams.get("next") || "/"

  async function login() {
    const res = await dispatchLogin(username, password, $page.data.urqlClient)
    if (res.status) {
      login_failed_message = ""
      logged_in = true
      await setTimeout(() => (window.location.href = next), 100)
      // can't do this, because it's hard to populate "user" back to layout:
      // setTimeout(() => goto(next), 100);
    } else {
      login_failed_message = res.error
    }
  }
</script>

<PageTitle class="">{$_("Login")}</PageTitle>
{#if logged_in}
  <p class="mt-3 text-green-500">
    {$_("Login successful.")}
  </p>
{:else}
  <p class="mt-3 text-red-500">
    {login_failed_message}
  </p>
{/if}
<form on:submit|preventDefault={login}>
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
