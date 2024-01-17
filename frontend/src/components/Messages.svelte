<script lang="ts">
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import Overlay from "$components/Overlay.svelte"

  interface Message {
    id: number
    title: string
    text: string
    level: "debug" | "info" | "success" | "warning" | "error"
    is_active: boolean
    allow_users_to_hide: boolean
  }

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

  let storage: Storage | object = {}

  if (browser) {
    try {
      storage = window.sessionStorage || {}
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
  {#each msgs.filter(m => !m.allow_users_to_hide || !acknowledgedMessages.includes(m.id)) as msg}
    <Overlay
      visible
      title={msg.title}
      class={levelClasses[msg.level]}
      closeButtonText={$_("OK")}
      on:close={() => {
        const checkbox = document.getElementById(`do-not-show-again-${msg.id}`)
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
  <Overlay />
{/await}
