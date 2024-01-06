<script lang="ts">
  import { toast } from "@zerodevx/svelte-toast"
  import { _ } from "svelte-i18n"

  import { getCsrfToken } from "$lib/utils"

  import HCaptcha from "$components/HCaptcha.svelte"
  import PageTitle from "$components/PageTitle.svelte"

  let email = ""
  let form_submitted = false

  const submit = async () => {
    const ret = await fetch("/api/user/password_reset/", {
      method: "POST",
      credentials: "include",
      body: JSON.stringify({ email, token }),
      headers: {
        "X-CSRFToken": await getCsrfToken(),
        "Content-Type": "application/json",
      },
    })
    const retJson = await ret.json()

    if (!ret.ok) {
      // graphql error
      toast.push(`Error: ${retJson}`)
    } else if (retJson.ok) {
      form_submitted = true
    } else {
      toast.push(`Server Error: ${retJson.code}`)
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
  <div class="text-center text-gray-700 dark:text-white">
    {@html $_(
      "If your email-address is registered <b>and active</b> you should receive an email shortly.",
    )}
  </div>
{:else}
  <form class="text-gray-700 dark:text-white" on:submit|preventDefault={submit}>
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
