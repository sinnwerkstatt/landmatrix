<script lang="ts">
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { dispatchLogin } from "$lib/user";

  let username = "";
  let password = "";
  let login_failed_message = "";
  let login_success_message = $_("You are logged in.");

  let logged_in;
  let next;

  onMount(() => {
    next = $page.url.searchParams.get("next") || "/";

    if ($page.stuff.user?.is_authenticated) {
      window.location.href = next;
    }
  });

  async function login() {
    const res = await dispatchLogin(username, password);
    if (res.status) {
      login_failed_message = "";
      logged_in = true;
      setTimeout(() => (window.location.href = next), 100);
    } else {
      login_failed_message = res.error;
    }
  }
</script>

<div class="test-login h-4/6 flex justify-center items-center">
  <div class="w-80 bg-neutral-600 text-white rounded p-4">
    <form on:submit|preventDefault={login}>
      <label class="block mb-4">
        Username
        <input
          bind:value={username}
          autocomplete="username"
          class="inpt"
          placeholder="Username"
          type="text"
        />
      </label>
      <label class="block mb-4">
        Password
        <input
          bind:value={password}
          autocomplete="current-password"
          class="inpt"
          placeholder="Password"
          type="password"
        />
      </label>
      <button class="btn btn-primary" type="submit">
        {$_("Login")}
      </button>
      <p class="mt-3 text-danger small">
        {logged_in ? login_success_message : login_failed_message}
      </p>
    </form>
  </div>
</div>
