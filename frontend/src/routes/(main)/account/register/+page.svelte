<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { getCsrfToken, slugify } from "$lib/utils"

  import HCaptcha from "$components/HCaptcha.svelte"
  import PageTitle from "$components/PageTitle.svelte"

  let user = {
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    information: "",
    password: "",
    password_confirm: "",
  }
  let token = ""
  let disabled = true
  let register_failed_message = ""
  let registration_successful = false

  function captchaVerified(e: CustomEvent<{ token: string }>) {
    token = e.detail.token
    disabled = false
  }

  function usernameChange() {
    user = { ...user, username: slugify(user.username) }
  }

  async function register() {
    const ret = await fetch("/api/user/register/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({ ...user, token }),
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
      register_failed_message = retJson.error
      return
    }
    registration_successful = true
  }
</script>

<PageTitle>{$_("Register")}</PageTitle>

{#if registration_successful}
  <div
    class="mb-4 flex h-full w-full items-center justify-center text-gray-700 dark:text-white"
  >
    {$_(
      "Registration successful. You can now close this window and check your emails.",
    )}
  </div>
{:else}
  <div
    class="mb-4 flex h-full w-full items-center justify-center text-gray-700 dark:text-white"
  >
    {$_(
      "Your contact information will help our researchers get in touch with you for additional information. We respect and protect your privacy and anonymity, and will never share or publish your personal information. You can also write us directly at data@landmatrix.org.",
    )}
  </div>

  <form
    class="my-6 grid gap-4 text-gray-700 md:grid-cols-2 dark:text-white"
    on:submit|preventDefault={register}
  >
    <label>
      {$_("Username")}
      <input
        bind:value={user.username}
        autocomplete="username"
        class="inpt"
        placeholder={$_("Username")}
        type="text"
        required
        pattern="[@_+.a-zA-Z0-9 \-]+"
        on:input={usernameChange}
      />
      <span class="text-xs">{$_("Letters, digits and @/./+/-/_ only.")}</span>
    </label>
    <label>
      {$_("Email")}
      <input
        bind:value={user.email}
        class="inpt"
        autocomplete="email"
        placeholder={$_("Email")}
        type="email"
        required
      />
    </label>
    <label>
      {$_("First name")}
      <input
        bind:value={user.first_name}
        class="inpt"
        placeholder={$_("First name")}
        type="text"
        required
      />
    </label>
    <label>
      {$_("Last name")}
      <input
        bind:value={user.last_name}
        class="inpt"
        placeholder={$_("Last name")}
        type="text"
        required
      />
    </label>

    <label>
      {$_("Phone")}
      <input
        bind:value={user.phone}
        class="inpt"
        placeholder={$_("Phone")}
        type="text"
      />
    </label>
    <label>
      {$_("User information")}
      <textarea
        bind:value={user.information}
        class="inpt"
        placeholder={$_(
          "Write something about yourself and your company. This won't be published.",
        )}
        type="text"
      />
    </label>

    <label>
      {$_("Password")}
      <input
        bind:value={user.password}
        class="inpt"
        autocomplete="new-password"
        placeholder={$_("Password")}
        type="password"
      />
    </label>
    <label>
      {$_("Password confirmation")}
      <input
        bind:value={user.password_confirm}
        class="inpt"
        autocomplete="new-password"
        placeholder={$_("Password confirmation")}
        type="password"
      />
    </label>
    <HCaptcha class="flex w-full justify-center" on:success={captchaVerified} />
    <div class="flex items-center justify-center">
      <button class="btn btn-primary w-full" type="submit" {disabled}>
        {$_("Register")}
      </button>
    </div>
    <p class="text-danger small mt-3">{register_failed_message}</p>
  </form>
{/if}
