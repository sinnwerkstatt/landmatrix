<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { page } from "$app/stores"

  import { getCsrfToken } from "$lib/utils"

  import PageTitle from "$components/PageTitle.svelte"

  let retJson: { ok: boolean; code?: string } | undefined
  async function register_confirm() {
    const ret = await fetch("/api/user/register_confirm/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({ activation_key: $page.params.activation_key }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    retJson = await ret.json()

    if (!ret.ok) {
      return toast.push(`Unknown Problem: ${retJson}`, { classes: ["error"] })
    }
  }

  onMount(register_confirm)
</script>

{#if retJson}
  {#if retJson.ok}
    <PageTitle>{$_("Account confirmed")}</PageTitle>
    {$_(
      "Your email address is confirmed. Your account awaits activation by an admin. If this does not happen within the next 24 hours, please contact the following address:",
    )}
    <a href="mailto:data@landmatrix.org">data@landmatrix.org</a>
  {:else if retJson.code === "already_activated"}
    <PageTitle>{$_("Account activated")}</PageTitle>
    {$_("Your account has been activated. You can log in now.")}
    <div class="text-right">
      <a href="/account/login" class="btn btn-primary">{$_("Login")}</a>
    </div>
  {:else}
    <PageTitle>{$_("Error")}</PageTitle>
    {retJson.code}
  {/if}
{/if}
