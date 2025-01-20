<script lang="ts">
  import * as staticEnv from "$env/static/public"
  import { onDestroy, onMount } from "svelte"

  import { browser } from "$app/environment"

  interface Props {
    hl?: string
    size?: "normal" | "compact" | "invisible"
    class?: string
    onsuccess?: (token: string) => void
  }

  let { hl = "", size = "normal", class: className = "", onsuccess }: Props = $props()

  // https://docs.hcaptcha.com/#integration-testing-test-keys
  export const sitekey =
    staticEnv.PUBLIC_HCAPTCHA_SITEKEY ?? "10000000-ffff-ffff-ffff-000000000001"

  export const reset = () => {
    if (mounted && loaded && widgetID) {
      window.hcaptcha.reset(widgetID)
    }
  }

  let mounted = $state(false)
  let loaded = $state(false)
  let widgetID: string | undefined = $state()

  onMount(() => {
    if (browser)
      window.hcaptchaOnLoad = () => {
        // dispatch("load")
        loaded = true
      }

    // dispatch("mount")
    mounted = true
  })
  onDestroy(() => {
    if (browser) {
      window.hcaptchaOnLoad = null
    }
    // guard against script loading race conditions
    // i.e. if component is destroyed before hcaptcha reference is loaded
    if (loaded) {
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      window.hcaptcha = null
    }
  })

  let targetDiv: HTMLDivElement | undefined = $state()
  $effect(() => {
    if (browser && mounted && loaded && targetDiv) {
      widgetID = window.hcaptcha.render(targetDiv, {
        sitekey,
        hl, // force a specific localisation
        theme: "light",
        callback: token => onsuccess?.(token),
        // "error-callback": () => dispatch("error"),
        // "close-callback": () => dispatch("close"),
        // "expired-callback": () => dispatch("expired"),
        size,
      })
    }
  })
</script>

<svelte:head>
  {#if browser && mounted && !window.hcaptcha}
    <script
      src="https://js.hcaptcha.com/1/api.js?onload=hcaptchaOnLoad&render=explicit"
      async
      defer
    ></script>
  {/if}
</svelte:head>

<div class={className} bind:this={targetDiv}></div>
