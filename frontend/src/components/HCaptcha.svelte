<script lang="ts">
  import { env } from "$env/dynamic/public"
  import { createEventDispatcher, onDestroy, onMount } from "svelte"

  import { browser } from "$app/environment"

  const dispatch = createEventDispatcher()

  export let hl = ""
  export let size: "normal" | "compact" | "invisible" = "normal"

  // https://docs.hcaptcha.com/#integration-testing-test-keys
  export const sitekey =
    env.PUBLI_HCAPTCHA_SITEKEY || "10000000-ffff-ffff-ffff-000000000001"

  export const reset = () => {
    if (mounted && loaded && widgetID) {
      window.hcaptcha.reset(widgetID)
    }
  }

  let mounted = false
  let loaded = false
  let widgetID

  onMount(() => {
    if (browser)
      window.hcaptchaOnLoad = () => {
        dispatch("load")
        loaded = true
      }

    dispatch("mount")
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

  $: if (browser && mounted && loaded) {
    widgetID = window.hcaptcha.render(targetDiv, {
      sitekey,
      hl, // force a specific localisation
      theme: "light",
      callback: token => dispatch("success", { token }),
      "error-callback": () => dispatch("error"),
      "close-callback": () => dispatch("close"),
      "expired-callback": () => dispatch("expired"),
      size,
    })
  }
  let targetDiv: HTMLDivElement
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

<div class={$$props.class} bind:this={targetDiv} />
