<script lang="ts">
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { dispatchLogin } from "$lib/user";

  let username = "";
  let password = "";
  let login_failed_message = "";
  let login_success_message = $_("You are logged in.");

  let logged_in = false;
  let next: string;

  onMount(() => {
    next = $page.url.searchParams.get("next") || "/";

    if ($page.data.user?.is_authenticated) {
      window.location.href = next;
    }
  });

  async function login() {
    const res = await dispatchLogin(username, password, $page.data.urqlClient);
    if (res.status) {
      login_failed_message = "";
      logged_in = true;
      await setTimeout(() => (window.location.href = next), 100);
      // can't do this, because it's hard to populate "user" back to layout:
      // setTimeout(() => goto(next), 100);
    } else {
      login_failed_message = res.error;
    }
  }
</script>

<div class="test-login flex h-5/6 items-center justify-center">
  <div class="w-[540px] border border-neutral-600 p-4 text-black">
    <h1 class="mb-10">{$_("Login")}</h1>
    <form on:submit|preventDefault={login}>
      <label class="mb-4 block">
        Username
        <input
          bind:value={username}
          autocomplete="username"
          class="inpt"
          placeholder="Username"
          type="text"
          autofocus
        />
      </label>
      <label class="mb-4 block">
        Password
        <input
          bind:value={password}
          autocomplete="current-password"
          class="inpt"
          placeholder="Password"
          type="password"
        />
      </label>
      <button class="btn btn-primary w-full" type="submit">
        {$_("Login")}
      </button>
      <p class="mt-3">
        {logged_in ? login_success_message : login_failed_message}
      </p>
    </form>
    <div class="mt-12 text-right">
      <a href="/account/register/">
        {$_("New around here? Sign up")}
      </a>
    </div>
  </div>
</div>
