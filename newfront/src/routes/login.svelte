<script lang="ts">
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { dispatchLogin, user } from "$lib/stores";

  let username = "";
  let password = "";
  let login_failed_message = "";
  let login_success_message = $_("You are logged in.");

  $: logged_in = $user?.is_authenticated || false;

  onMount(() => {
    const next = $page.url.searchParams.get("next") || "/";

    if (logged_in) {
      goto(next);
    }
  });

  async function login() {
    const res = await dispatchLogin(username, password);
    if (res.status) {
      login_failed_message = "";
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
