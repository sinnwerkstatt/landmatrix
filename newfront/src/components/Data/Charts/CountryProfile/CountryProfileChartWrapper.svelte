<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { browser } from "$app/env";
  import { deals } from "$lib/data";
  import FileCodeIcon from "$components/icons/FileCodeIcon.svelte";
  import FileImageIcon from "$components/icons/FileImageIcon.svelte";
  import LoadingPulse from "$components/LoadingPulse.svelte";
  import { chart_download, fileName } from "../utils";

  export let title: string;
  export let svgID: string;

  const dispatch = createEventDispatcher();
  $: isChrome = browser && /Google Inc/.test(navigator.vendor);

  function downloadImage(filetype: string) {
    chart_download(
      document.getElementById(svgID),
      `image/${filetype}`,
      fileName(title, `.${filetype}`)
    );
  }
</script>

<div class="drop-shadow mx-4 my-12 p-1 flex flex-col flex-nowrap bg-orange-50">
  <slot name="heading">
    <h2 class="text-lg font-bold my-3">{title}</h2>
  </slot>
  <div
    class="max-w-full bg-white flex justify-center items-center flex-auto	svg-wrapper"
  >
    {#if !$deals} <div class="absolute"><LoadingPulse /></div> {/if}
    <slot />
  </div>
  <div class="bg-[#2d2d2d] text-lm-light text-sm">
    <button on:click={() => downloadImage("svg")} class="pb-1 px-3">
      <FileImageIcon /> SVG
    </button>
    <span
      id="download-png"
      title={isChrome ? "" : "At the moment, downloading PNG does not work in Firefox."}
    >
      <button
        class="pb-1 px-3"
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
        class="pb-1 px-3"
        class:use-chrome={!isChrome}
        on:click={() => downloadImage("webp")}
      >
        <FileImageIcon /> WebP
      </button>
    </span>

    <span style="margin: 2rem 0">|</span>
    <button class="pb-1 px-3" on:click={() => dispatch("downloadJSON")}>
      <FileCodeIcon /> JSON
    </button>
    <button class="pb-1 px-3" on:click={() => dispatch("downloadCSV")}>
      <FileCodeIcon /> CSV
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
