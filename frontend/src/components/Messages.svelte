<script lang="ts">
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"
  import { page } from "$app/state"

  import type { components } from "$lib/openAPI"

  import Overlay from "$components/Overlay.svelte"

  type Message = components["schemas"]["Message"]

  async function getMessages(): Promise<Message[]> {
    const isSameSiteReferrer = document.referrer?.startsWith(
      window.location.protocol + "//" + window.location.hostname,
    )
    if (isSameSiteReferrer) {
      return []
    }

    const res = await fetch(`/api/messages/`)
    if (!res.ok) {
      throw new Error(await res.text())
    }

    return await res.json()
  }

  let storage: Storage | { acknowledgedMessages?: number[] } = {}

  if (browser) {
    try {
      storage = window.localStorage || {}
    } catch {
      // sessionStorage disabled due to private browsing
      // https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API#private_browsing_incognito_modes
    }
  }

  let acknowledgedMessages: number[] =
    JSON.parse(storage["acknowledgedMessages"] ?? null) || []

  const ackMsg = (id: number) => {
    acknowledgedMessages.push(id)
    storage["acknowledgedMessages"] = JSON.stringify(acknowledgedMessages)
  }

  const levelClasses: { [key in Message["level"]]: string } = {
    error: "border-red-600 border-2",
    warning: "border-orange border-2",
    info: "border-orange border",
    debug: "border-gray-600 border-2",
    success: "border-green-600 border-2",
  }
</script>

{#await getMessages() then msgs}
  {#each msgs
    .filter(m => !m.allow_users_to_hide || !acknowledgedMessages.includes(m.id))
    .filter(m => (m.logged_in_only ? !!page.data.user : true)) as msg}
    <Overlay
      visible
      title={msg.title}
      class={levelClasses[msg.level]}
      closeButtonText={$_("OK")}
      onclose={() => {
        const checkbox = document.getElementById(`do-not-show-again-${msg.id}`)
        // typescript support for templates comes with svelte5:
        // https://github.com/sveltejs/svelte/issues/4701
        // https://github.com/sveltejs/svelte/pull/9482
        if (checkbox && checkbox.checked) {
          ackMsg(msg.id)
        }
      }}
    >
      {@html msg.text}

      {#if msg.allow_users_to_hide}
        <label class="block">
          <input id={`do-not-show-again-${msg.id}`} type="checkbox" />
          {$_("Don't show this message again")}
        </label>
      {/if}
    </Overlay>
  {/each}
{/await}
