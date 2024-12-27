<script lang="ts">
  import { _ } from "svelte-i18n"

  import { page } from "$app/state"

  import { getCsrfToken } from "$lib/utils"

  import PageTitle from "$components/PageTitle.svelte"

  let new_password1 = $state("")
  let new_password2 = $state("")
  let form_submitted = $state(false)

  async function onsubmit(e: SubmitEvent) {
    e.preventDefault()
    await fetch("/api/user/password_reset_confirm/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({
        uidb64: page.params.uidb64,
        token: page.params.token,
        new_password1: new_password1,
        new_password2: new_password2,
      }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    // const retJson = await ret.json()
    form_submitted = true
  }
</script>

<PageTitle>{$_("Change password")}</PageTitle>
{#if form_submitted}
  <div class="text-gray-700 dark:text-white">
    {$_("Password successfully updated.")}

    <div class="text-right">
      <a href="/account/login" class="btn btn-primary">{$_("Login")}</a>
    </div>
  </div>
{:else}
  <form class="text-gray-700 dark:text-white" {onsubmit}>
    <label class="block">
      {$_("Password")}
      <input
        bind:value={new_password1}
        class="inpt"
        autocomplete="new-password"
        placeholder={$_("Password")}
        type="password"
      />
    </label>
    <label class="block">
      {$_("Password confirmation")}
      <input
        bind:value={new_password2}
        class="inpt"
        autocomplete="new-password"
        placeholder={$_("Password confirmation")}
        type="password"
      />
    </label>
    <button class="btn btn-primary block" type="submit">
      {$_("Set password")}
    </button>
  </form>
{/if}
