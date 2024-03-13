<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import { _ } from "svelte-i18n"
  import { fade, slide } from "svelte/transition"

  import { browser } from "$app/environment"

  const dispatch = createEventDispatcher()

  export let visible = false
  export let hideable = true
  export let title: string | null = null

  export let showSubmit = false
  export let gotoLink: { href: string; title: string; className?: string } | null = null
  export let submitTitle: string | null = null
  export let submitDisabled = false

  export let closeButtonText = $_("Cancel")

  function close() {
    if (hideable) {
      dispatch("close")
      visible = false
    }
  }

  function escape_key(e: KeyboardEvent) {
    if (e.key === "Escape") close()
  }

  $: if (browser) {
    if (visible) document.addEventListener("keydown", escape_key)
    else document.removeEventListener("keydown", escape_key)
  }
</script>

{#if visible}
  <div
    role="none"
    transition:fade={{ duration: 100 }}
    class="fixed inset-0 z-[100] flex h-screen max-h-screen w-screen items-center justify-center bg-[rgba(0,0,0,0.3)] backdrop-blur-sm"
    on:click|self={close}
    on:keyup|self={close}
  >
    <div
      transition:slide={{ duration: 150 }}
      class="max-h-[99vh] w-[clamp(300px,70vw,800px)] overflow-y-auto border bg-white text-black shadow-xl dark:bg-gray-700 dark:text-white {$$props.class ??
        ''}"
    >
      <form on:submit|preventDefault>
        {#if $$slots.header || title}
          <div class="border-b px-7 py-5">
            <slot name="header"><span class="font-bold">{title}</span></slot>
          </div>
        {/if}
        <div class="p-7">
          <slot />
        </div>

        <div class="border-t px-7 py-5 text-right">
          <button type="button" class="btn btn-cancel mx-2" on:click={close}>
            {closeButtonText}
          </button>
          {#if showSubmit}
            <button disabled={submitDisabled} type="submit" class="btn btn-primary">
              {submitTitle ?? title}
            </button>
          {/if}
          {#if gotoLink}
            <a
              href={gotoLink.href}
              target="_blank"
              class="btn btn-primary {gotoLink.className}"
            >
              {gotoLink.title}
            </a>
          {/if}
        </div>
      </form>
    </div>
  </div>
{/if}
