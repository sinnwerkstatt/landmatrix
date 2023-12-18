<script lang="ts">
  import { gql } from "@urql/svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import PageTitle from "$components/PageTitle.svelte"

  let new_password1 = ""
  let new_password2 = ""
  let form_submitted = false

  function submit() {
    $page.data.urqlClient
      .mutation<{ password_reset_confirm: boolean }>(
        gql`
          mutation ($uidb64: String!, $token: String!, $np1: String!, $np2: String!) {
            password_reset_confirm(
              uidb64: $uidb64
              token: $token
              new_password1: $np1
              new_password2: $np2
            )
          }
        `,
        {
          uidb64: $page.params.uidb64,
          token: $page.params.token,
          np1: new_password1,
          np2: new_password2,
        },
      )
      .toPromise()
      .then(({ data }) => {
        if (data?.password_reset_confirm) form_submitted = true
      })
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
  <form class="text-gray-700 dark:text-white" on:submit|preventDefault={() => submit()}>
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
