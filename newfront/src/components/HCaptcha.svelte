<script lang="ts">
  import { createEventDispatcher, onDestroy, onMount } from "svelte";
  import { browser } from "$app/env";

  const dispatch = createEventDispatcher();

  export let sitekey = "10000000-ffff-ffff-ffff-000000000001";
  export let hl = "";
  export let size: "normal" | "compact" | "invisible" = "normal";

  export const reset = () => {
    if (mounted && loaded && widgetID) hcaptcha.reset(widgetID);
  };

  let mounted = false;
  let loaded = false;
  let widgetID;

  onMount(() => {
    if (browser)
      window.hcaptchaOnLoad = () => {
        // consumers can attach custom on:load handlers
        dispatch("load");
        loaded = true;
      };

    dispatch("mount");
    mounted = true;
  });
  onDestroy(() => {
    if (browser) {
      window.hcaptchaOnLoad = null;
    }
    // guard against script loading race conditions
    // i.e. if component is destroyed before hcaptcha reference is loaded
    if (loaded) hcaptcha = null;
  });

  $: if (mounted && loaded) {
    widgetID = hcaptcha.render(targetDiv, {
      sitekey,
      hl, // force a specific localisation
      theme: "light",
      callback: (token) => dispatch("success", { token }),
      "error-callback": () => dispatch("error"),
      "close-callback": () => dispatch("close"),
      "expired-callback": () => dispatch("expired"),
      size,
    });
  }
  let targetDiv: HTMLDivElement;
</script>

<svelte:head>
  {#if mounted && !window?.hcaptcha}
    <script
      src="https://js.hcaptcha.com/1/api.js?onload=hcaptchaOnLoad&render=explicit"
      async
      defer></script>
  {/if}
</svelte:head>

<div class={$$props.class} bind:this={targetDiv} />
