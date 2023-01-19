<script lang="ts">
  import { Client, gql } from "@urql/svelte"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import PageTitle from "$components/PageTitle.svelte"

  let ret = undefined
  async function register_confirm() {
    ret = await ($page.data.urqlClient as Client)
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
    {$_("Your email address is confirmed. You can log in now.")}
    <div class="text-right">
      <a href="/account/login" class="btn btn-primary">{$_("Login")}</a>
    </div>
  {:else if ret.data.register_confirm.code === "already_activated"}
    {$_("This account has already been activated. You can probably log in now.")}
    <div class="text-right">
      <a href="/account/login" class="btn btn-primary">{$_("Login")}</a>
    </div>
  {:else}
    {ret.data.register_confirm.code}
  {/if}
{/if}
