<script lang="ts">
  import { createEventDispatcher } from "svelte"

  import { browser } from "$app/environment"

  import type { FileType } from "$components/Data/Charts/utils"
  import FileCodeIcon from "$components/icons/FileCodeIcon.svelte"
  import FileImageIcon from "$components/icons/FileImageIcon.svelte"

  export let title: string
  export let wrapperClasses = ""
  export let disableCSV = false
  export let disableSVG = false

  const dispatch = createEventDispatcher<{ download: FileType }>()

  $: isChrome = browser && /Google Inc/.test(navigator.vendor)
</script>

<div id="${title}_wrapper" class="flex flex-col flex-nowrap px-5 {wrapperClasses}">
  <slot name="heading">
    {#if title}
      <h2>{title}</h2>
    {/if}
  </slot>
  <div class="svg-wrapper flex items-center justify-center">
    <slot />
  </div>
  <div class="flex-shrink-0">
    <slot name="legend" />
  </div>
  <ul
    class="my-2 mx-auto flex w-fit bg-white p-1 font-oswald text-sm text-lm-dark dark:bg-gray-800 dark:text-white"
  >
    <li id="download-svg">
      <button
        class="px-3 pb-1 hover:text-orange-200"
        class:grey-out={disableSVG}
        on:click={() => dispatch("download", "svg")}
      >
        <FileImageIcon />
        SVG
      </button>
    </li>

    <li
      id="download-png"
      title={isChrome ? "" : "At the moment, downloading PNG does not work in Firefox."}
    >
      <button
        class="px-3 pb-1 hover:text-orange-200"
        class:grey-out={!isChrome}
        on:click={() => dispatch("download", "png")}
      >
        <FileImageIcon />
        PNG
      </button>
    </li>

    <li
      id="download-webp"
      title={isChrome
        ? ""
        : "At the moment, downloading WebP does not work in Firefox."}
    >
      <button
        class="px-3 pb-1 hover:text-orange-200"
        class:grey-out={!isChrome}
        on:click={() => dispatch("download", "webp")}
      >
        <FileImageIcon /> WebP
      </button>
    </li>

    <span>|</span>

    <li id="download-json">
      <button
        class="px-3 pb-1 hover:text-orange-200"
        on:click={() => dispatch("download", "json")}
      >
        <FileCodeIcon />
        JSON
      </button>
    </li>

    <li id="download-csv">
      <button
        class="px-3 pb-1 hover:text-orange-200"
        class:grey-out={disableCSV}
        on:click={() => dispatch("download", "csv")}
      >
        <FileCodeIcon />
        CSV
      </button>
    </li>
  </ul>
</div>

<style>
  .grey-out {
    opacity: 0.7;
    pointer-events: none;
  }
</style>
