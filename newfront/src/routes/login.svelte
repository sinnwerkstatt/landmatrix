<script lang="ts">
  import { dispatchLogin, user } from "$lib/stores";
  import { _ } from "svelte-i18n";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  let username = "";
  let password = "";
  let login_failed_message = "";

  onMount(() => {
    const next = $page.url.searchParams.get("next");
    if ($user?.is_authenticated && next) {
      goto(next);
    }
  });
  async function login() {
    const res = await dispatchLogin(username, password);
    console.log(res);
    if (res.status === true) {
      console.log("juchu!");
    } else {
      login_failed_message = res.error;
    }
  }
</script>

<div class=" h-4/6 flex justify-center items-center">
  <div class="w-80 bg-neutral-600 text-white rounded p-4">
    <form on:submit|preventDefault={login}>
      <label class="block mb-4">
        Username
        <input
          bind:value={username}
          autocomplete="username"
          class="form-control"
          placeholder="Username"
          type="text"
        />
      </label>
      <label class="block mb-4">
        Password
        <input
          bind:value={password}
          autocomplete="current-password"
          class="form-control"
          placeholder="Password"
          type="password"
        />
      </label>
      <button class="btn btn-primary" type="submit">
        {$_("Login")}
      </button>
      <p class="mt-3 text-danger small">{login_failed_message}</p>
    </form>
  </div>
</div>
