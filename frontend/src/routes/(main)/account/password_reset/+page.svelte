<script lang="ts">
  import { Client, gql } from "@urql/svelte"
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import HCaptcha from "$components/HCaptcha.svelte"
  import PageTitle from "$components/PageTitle.svelte"

  let email = ""
  let form_submitted = false

  const submit = async () => {
    const urql: Client = $page.data.urqlClient
    const res = await urql
      .mutation<{ password_reset: { ok: boolean; code: string } }>(
        gql`
          mutation ($email: String!, $token: String!) {
            password_reset(email: $email, token: $token) {
              ok
              code
            }
          }
        `,
        { email, token },
      )
      .toPromise()

    if (res.error) {
      // graphql error
      toast.push(`GraphQL Error: ${res.error.message}`)
    } else if (res.data?.password_reset.ok) {
      form_submitted = true
    } else {
      toast.push(`Server Error: ${res.data?.password_reset.code}`)
    }
  }
  let token: string
  let disabled = true
  function captchaVerified(e: CustomEvent<{ token: string }>) {
    token = e.detail.token
    disabled = false
  }
</script>

<PageTitle>{$_("Reset password")}</PageTitle>
{#if form_submitted}
  <div class="text-center text-lm-dark dark:text-white">
    {@html $_(
      "If your email-address is registered <b>and active</b> you should receive an email shortly.",
    )}
  </div>
{:else}
  <form class="text-lm-dark dark:text-white" on:submit|preventDefault={submit}>
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
