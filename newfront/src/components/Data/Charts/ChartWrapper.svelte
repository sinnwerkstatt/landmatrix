<script lang="ts">
  import { createEventDispatcher } from "svelte"

  import { browser } from "$app/environment"

  import { loading } from "$lib/stores"

  import type { FileType } from "$components/Data/Charts/utils"
  import FileCodeIcon from "$components/icons/FileCodeIcon.svelte"
  import FileImageIcon from "$components/icons/FileImageIcon.svelte"
  import LoadingPulse from "$components/LoadingPulse.svelte"

  export let title: string
  export let wrapperClasses = ""

  const dispatch = createEventDispatcher<{ download: FileType }>()
  $: isChrome = browser && /Google Inc/.test(navigator.vendor)
</script>

<div
  class="mx-4 my-12 flex flex-col flex-nowrap bg-orange-50 p-1 drop-shadow {wrapperClasses}"
>
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
    <button on:click={() => dispatch("download", "svg")} class="px-3 pb-1">
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
        on:click={() => dispatch("download", "png")}
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
        on:click={() => dispatch("download", "webp")}
      >
        <FileImageIcon /> WebP
      </button>
    </span>

    <span style="margin: 2rem 0">|</span>
    <button class="px-3 pb-1" on:click={() => dispatch("download", "json")}>
      <FileCodeIcon />
      JSON
    </button>
    <button class="px-3 pb-1" on:click={() => dispatch("download", "csv")}>
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
