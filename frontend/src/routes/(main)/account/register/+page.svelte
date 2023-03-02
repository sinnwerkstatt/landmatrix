<script lang="ts">
  import type { Client } from "@urql/svelte"
  import { gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

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
    console.log(token)
  }

  async function register() {
    const ret = await ($page.data.urqlClient as Client)
      .mutation<{ register: { ok: boolean; code: string } }>(
        gql`
          mutation Register(
            $username: String!
            $first_name: String!
            $last_name: String!
            $email: String!
            $phone: String
            $information: String!
            $password: String!
            $token: String!
          ) {
            register(
              username: $username
              first_name: $first_name
              last_name: $last_name
              email: $email
              phone: $phone
              information: $information
              password: $password
              token: $token
            ) {
              ok
              code
            }
          }
        `,
        { ...user, token },
      )
      .toPromise()
    if (ret.data?.register?.ok) {
      registration_successful = true
    } else {
      register_failed_message = ret.data?.register?.code || ret.error.toString()
    }
  }
</script>

<PageTitle>{$_("Register")}</PageTitle>
{#if registration_successful}
  <div class="mb-4 flex h-full w-full items-center justify-center">
    {$_(
      "Registration successful. You can now close this window and check your emails.",
    )}
  </div>
{:else}
  {$_(
    "Your contact information will help our researchers get in touch with you for additional information. We respect and protect your privacy and anonymity, and will never share or publish your personal information. You can also write us directly at data@landmatrix.org.",
  )}

  <form class="my-6 grid gap-4 md:grid-cols-2" on:submit|preventDefault={register}>
    <label>
      {$_("Username")}
      <input
        bind:value={user.username}
        autocomplete="username"
        class="inpt"
        placeholder={$_("Username")}
        type="text"
        required
      />
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
