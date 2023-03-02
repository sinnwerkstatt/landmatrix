<script lang="ts">
  import { Client, gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import HCaptcha from "$components/HCaptcha.svelte"
  import PageTitle from "$components/PageTitle.svelte"

  let email = ""
  let form_submitted = false

  const submit = async () => {
    const res = await ($page.data.urqlClient as Client)
      .mutation(
        gql`
          mutation ($email: String!, $token: String!) {
            password_reset(email: $email, token: $token)
          }
        `,
        { email, token },
      )
      .toPromise()

    if (res.error) {
      console.error(res.error.message)
    } else {
      if (res.data.password_reset) {
        form_submitted = true
      }
    }
  }
  let token: string
  let disabled = true
  function captchaVerified(e: CustomEvent<{ token: string }>) {
    token = e.detail.token
    disabled = false
    console.log(token)
  }
</script>

<PageTitle>{$_("Reset password")}</PageTitle>
{#if form_submitted}
  <div class="text-center">
    {$_(
      "If your email-address is registered with Land Matrix you should receive an email shortly.",
    )}
  </div>
{:else}
  <form on:submit|preventDefault={submit}>
    <label class="mb-4 block">
      {$_("Email")}
      <input
        bind:value={email}
        autocomplete="email"
        class="inpt block"
        placeholder={$_("Email")}
        required
        type="email"
      />
    </label>
    <div class="grid grid-cols-2 gap-4">
      <HCaptcha class="flex w-full justify-center" on:success={captchaVerified} />
      <div class="flex items-center justify-center">
        <button class="btn btn-primary w-full" type="submit" {disabled}>
          {$_("Reset password")}
        </button>
      </div>
    </div>
  </form>
{/if}
