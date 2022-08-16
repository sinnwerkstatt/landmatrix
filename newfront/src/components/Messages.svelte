<script lang="ts">
  import Cookies from "js-cookie";
  import { _ } from "svelte-i18n";
  import { browser } from "$app/env";
  import Overlay from "$components/Overlay.svelte";

  async function getMessages() {
    if (!browser) return [];
    if (
      document.referrer?.startsWith(
        window.location.protocol + "//" + window.location.hostname
      )
    )
      return [];
    const res = await fetch(`/api/newdeal_legacy/messages/`);
    if (res.ok) return (await res.json()).messages;
    else throw new Error(await res.text());
  }
  let messages = getMessages();

  let acknowledgedMessages: number[] = JSON.parse(
    Cookies.get("acknowledgedMessages") || "[]"
  );
  const ackMsg = (id) => {
    acknowledgedMessages.push(id);
    Cookies.set("acknowledgedMessages", JSON.stringify(acknowledgedMessages), {
      sameSite: "lax",
      expires: 365,
    });
  };
  const levelClasses = {
    error: "border-red-600 border-2",
    warning: "border-orange border-2",
    info: "border-orange border",
  };
</script>

{#await messages then msgs}
  {#each msgs.filter((m) => !m.allow_users_to_hide || !acknowledgedMessages.includes(m.id)) as msg}
    <Overlay
      visible
      title={msg.title}
      class={levelClasses[msg.level]}
      closeButtonText={$_("OK")}
    >
      {@html msg.text}

      {#if msg.allow_users_to_hide}
        <label class="block">
          <input type="checkbox" on:click={() => ackMsg(msg.id)} />
          {$_("Don't show this message again")}
        </label>
      {/if}
    </Overlay>
  {/each}
  <Overlay />
{/await}
