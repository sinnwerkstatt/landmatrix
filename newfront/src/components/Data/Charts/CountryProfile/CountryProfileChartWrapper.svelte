<script lang="ts">
  import { createEventDispatcher } from "svelte"

  import { browser } from "$app/environment"

  import { loading } from "$lib/stores"

  import FileCodeIcon from "$components/icons/FileCodeIcon.svelte"
  import FileImageIcon from "$components/icons/FileImageIcon.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  import { chart_download, fileName } from "../utils"

  export let title: string
  export let svgID: string

  const dispatch = createEventDispatcher()
  $: isChrome = browser && /Google Inc/.test(navigator.vendor)

  function downloadImage(filetype: string) {
    chart_download(
      document.getElementById(svgID),
      `image/${filetype}`,
      fileName(title, `.${filetype}`),
    )
  }
</script>

<div class="mx-4 my-12 flex flex-col flex-nowrap bg-orange-50 p-1 drop-shadow">
  <slot name="heading">
    <h2>{title}</h2>
  </slot>
  <div
    class="svg-wrapper flex max-w-full flex-auto items-center justify-center	bg-white"
  >
    {#if $loading}
      <div class="absolute">
        <LoadingPulse />
      </div>
    {/if}
    <slot />
  </div>
  <div class="bg-[#2d2d2d] text-sm text-lm-light">
    <button on:click={() => downloadImage("svg")} class="px-3 pb-1">
      <FileImageIcon />
      SVG
    </button>
    <span
      id="download-png"
      title={isChrome ? "" : "At the moment, downloading PNG does not work in Firefox."}
    >
      <button
        class="px-3 pb-1"
        class:use-chrome={!isChrome}
        on:click={() => downloadImage("png")}
      >
        <FileImageIcon />
        PNG
      </button>
    </span>

    <span
      id="download-webp"
      title={isChrome
        ? ""
        : "At the moment, downloading WebP does not work in Firefox."}
    >
      <button
        class="px-3 pb-1"
        class:use-chrome={!isChrome}
        on:click={() => downloadImage("webp")}
      >
        <FileImageIcon /> WebP
      </button>
    </span>

    <span style="margin: 2rem 0">|</span>
    <button class="px-3 pb-1" on:click={() => dispatch("downloadJSON")}>
      <FileCodeIcon />
      JSON
    </button>
    <button class="px-3 pb-1" on:click={() => dispatch("downloadCSV")}>
      <FileCodeIcon />
      CSV
    </button>
  </div>
  <div class="flex-shrink-0 p-2">
    <slot name="legend" />
  </div>
</div>

<style>
  .use-chrome {
    opacity: 0.7;
    pointer-events: none;
  }
</style>
