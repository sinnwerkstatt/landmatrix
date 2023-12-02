<script lang="ts">
  import { gql } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import PageTitle from "$components/PageTitle.svelte"

  let ret = undefined
  async function register_confirm() {
    ret = await $page.data.urqlClient
      .mutation<{ register_confirm: { ok: boolean; code: string } }>(
        gql`
          mutation Register($activation_key: String!) {
            register_confirm(activation_key: $activation_key) {
              ok
              code
            }
          }
        `,
        { activation_key: $page.params.activation_key },
      )
      .toPromise()
  }

  onMount(() => {
    register_confirm()
  })
</script>

{#if ret}
  {#if ret.data.register_confirm.ok}
    <PageTitle>{$_("Account confirmed")}</PageTitle>
    {$_(
      "Your email address is confirmed. Your account awaits activation by an admin. If this does not happen within the next 24 hours, please contact the following address:",
    )}
    <a href="mailto:data@landmatrix.org">data@landmatrix.org</a>
  {:else if ret.data.register_confirm.code === "already_activated"}
    <PageTitle>{$_("Account activated")}</PageTitle>
    {$_("Your account has been activated. You can log in now.")}
    <div class="text-right">
      <a href="/account/login" class="btn btn-primary">{$_("Login")}</a>
    </div>
  {:else}
    <PageTitle>{$_("Error")}</PageTitle>
    {ret.data.register_confirm.code}
  {/if}
{/if}
