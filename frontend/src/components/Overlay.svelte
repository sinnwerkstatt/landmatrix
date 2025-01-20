<script lang="ts">
  import type { Snippet } from "svelte"
  import { _ } from "svelte-i18n"
  import type { EventHandler } from "svelte/elements"
  import { fade, slide } from "svelte/transition"

  import { browser } from "$app/environment"

  interface Props {
    visible?: boolean
    hideable?: boolean
    title?: string | null
    showSubmit?: boolean
    gotoLink?: { href: string; title: string; className?: string } | null
    submitTitle?: string | null
    submitDisabled?: boolean
    closeButtonText?: string
    class?: string
    header?: Snippet
    children?: Snippet
    onclose?: () => void
    onsubmit?: EventHandler<SubmitEvent, HTMLFormElement>
  }

  let {
    visible = $bindable(false),
    hideable = true,
    title = null,
    showSubmit = false,
    gotoLink = null,
    submitTitle = null,
    submitDisabled = false,
    closeButtonText = $_("Cancel"),
    class: className = "",
    header,
    children,
    onclose,
    onsubmit,
  }: Props = $props()

  function close() {
    if (hideable) {
      onclose?.()
      visible = false
    }
  }

  function escape_key(e: KeyboardEvent) {
    if (e.key === "Escape") close()
  }

  $effect(() => {
    if (browser) {
      if (visible) document.addEventListener("keydown", escape_key)
      else document.removeEventListener("keydown", escape_key)
    }
  })
</script>

{#if visible}
  <div
    role="none"
    transition:fade={{ duration: 100 }}
    class="fixed inset-0 z-[100] flex h-screen max-h-screen w-screen items-center justify-center bg-[rgba(0,0,0,0.3)] backdrop-blur-sm"
    onclick={function (e) {
      // TODO check if this is correct
      console.log(e.target)
      console.log(this)
      if (e.target === this) close?.()
    }}
  >
    <div
      transition:slide={{ duration: 150 }}
      class="max-h-[99vh] w-[clamp(300px,70vw,800px)] overflow-y-auto border bg-white text-black shadow-xl dark:bg-gray-700 dark:text-white {className}"
    >
      <form {onsubmit}>
        {#if header || title}
          <div class="border-b px-7 py-5">
            {#if header}
              {@render header()}
            {:else}
              <span class="font-bold">
                {title}
              </span>
            {/if}
          </div>
        {/if}
        <div class="p-7">
          {@render children?.()}
        </div>

        <div class="border-t px-7 py-5 text-right">
          <button type="button" class="btn btn-cancel mx-2" onclick={close}>
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
