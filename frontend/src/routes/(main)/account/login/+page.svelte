<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  import { getCsrfToken } from "$lib/utils"

  import PageTitle from "$components/PageTitle.svelte"

  let username = ""
  let password = ""
  let login_failed_message = ""

  let logged_in = false
  let next = $page.url.searchParams.get("next") || "/"

  async function login() {
    const ret = await fetch("/api/user/login/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({ username, password }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    const retJson = await ret.json()
    console.log(retJson)
    if (!ret.ok) {
      return toast.push(`Unknown Problem: ${retJson}`, { classes: ["error"] })
    }
    if (!retJson.ok) {
      login_failed_message = retJson.error
      return
    }

    login_failed_message = ""
    logged_in = true

    await goto(next, { invalidateAll: true })
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
