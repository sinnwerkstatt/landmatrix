<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"
  import type { FormEventHandler } from "svelte/elements"

  import { getCsrfToken, slugify } from "$lib/utils"

  import HCaptcha from "$components/HCaptcha.svelte"
  import PageTitle from "$components/PageTitle.svelte"

  let user = $state({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    information: "",
    password: "",
    password_confirm: "",
  })

  let arePasswordsEqual: boolean = $derived(user.password === user.password_confirm)

  let captchaToken: string | null = $state(null)
  let registrationSuccessful = $state(false)
  let registrationErrorMessage = $state("")

  let errorMessageMap = $derived({
    captcha_problems: $_("Captcha validation failed. Please try again."),
    username_already_exists: $_("Username already taken."),
    unknown_error: $_("Registration failed. Please try again."),
  })

  let submitDisabled = $derived(captchaToken === null)

  const setCaptchaToken = (token: string) => {
    captchaToken = token
  }

  const sanitizeUsername: FormEventHandler<HTMLInputElement> = () => {
    user = { ...user, username: slugify(user.username) }
  }

  const validateConfirmationPassword: FormEventHandler<HTMLInputElement> = event => {
    const inputField = event.currentTarget as HTMLInputElement
    inputField.setCustomValidity(arePasswordsEqual ? "" : $_("Passwords do not match."))
  }

  const register = async (e: SubmitEvent) => {
    e.preventDefault()

    const ret = await fetch("/api/user/register/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({ ...user, token: captchaToken }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })

    if (!ret.ok) {
      toast.push(`Registration failed: ${ret.status}`, { classes: ["error"] })
      return
    }

    const retJson = await ret.json()

    if (retJson.ok) {
      registrationSuccessful = true
    } else {
      registrationErrorMessage = errorMessageMap[retJson.code as never]
    }
  }
</script>

<PageTitle>{$_("Register")}</PageTitle>

{#if registrationSuccessful}
  <div class="mb-4 flex h-full w-full items-center justify-center">
    {$_(
      "Registration successful. You can now close this window and check your emails.",
    )}
  </div>
{:else}
  <div class="mb-4 flex h-full w-full items-center justify-center">
    {$_(
      "Your contact information will help our researchers get in touch with you for additional information. " +
        "We respect and protect your privacy and anonymity, and will never share or publish your personal information. " +
        "You can also write us directly at data@landmatrix.org.",
    )}
  </div>

  <form class="my-6 grid gap-4 md:grid-cols-2" onsubmit={register}>
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
        oninput={sanitizeUsername}
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
        autocomplete="name"
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
        autocomplete="family-name"
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
        type="tel"
        autocomplete="tel"
        placeholder={$_("Phone")}
      />
    </label>

    <label>
      {$_("User information")}
      <textarea
        bind:value={user.information}
        class="inpt"
        autocomplete="off"
        placeholder={$_(
          "Write something about the reasons and motivation why you need a user account.",
        )}
        required
      ></textarea>
    </label>

    <label>
      {$_("Password")}
      <input
        bind:value={user.password}
        class="inpt"
        autocomplete="new-password"
        placeholder={$_("Password")}
        type="password"
        required
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
        oninput={validateConfirmationPassword}
        required
      />
      {#if user.password_confirm && !arePasswordsEqual}
        <span class="text-xs">{$_("Passwords do not match.")}</span>
      {/if}
    </label>

    <HCaptcha class="flex w-full justify-center" onsuccess={setCaptchaToken} />

    <div class="flex items-center justify-center">
      <button class="btn btn-primary w-full" type="submit" disabled={submitDisabled}>
        {$_("Register")}
      </button>
    </div>

    <p class="small mt-3 text-red-500">{registrationErrorMessage}</p>
  </form>
{/if}
