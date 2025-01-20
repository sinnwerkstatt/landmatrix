<script lang="ts">
  import { type Snippet } from "svelte"

  import { browser } from "$app/environment"

  import type { FileType } from "$components/Data/Charts/utils"
  import FileCodeIcon from "$components/icons/FileCodeIcon.svelte"
  import FileImageIcon from "$components/icons/FileImageIcon.svelte"

  interface Props {
    title: string
    wrapperClasses?: string
    disableCSV?: boolean
    disableSVG?: boolean
    heading?: Snippet
    children?: Snippet
    legend?: Snippet
    ondownload?: (format: FileType) => void
  }

  let {
    title,
    wrapperClasses = "",
    disableCSV = false,
    disableSVG = false,
    heading,
    children,
    legend,
    ondownload,
  }: Props = $props()

  let isChrome = $derived(browser && /Google Inc/.test(navigator.vendor))
</script>

<div id="{title}_wrapper" class="flex flex-col flex-nowrap {wrapperClasses}">
  {#if heading}
    {@render heading()}
  {:else if title}
    <h2 class="heading3 mt-0 text-gray-700 dark:text-gray-50">{title}</h2>
  {/if}
  <div class="svg-wrapper flex items-center justify-center">
    {@render children?.()}
  </div>
  <div class="flex-shrink-0">
    {@render legend?.()}
  </div>
  <ul
    class="mx-auto my-2 flex w-fit bg-white p-1 text-sm text-gray-700 dark:bg-gray-800 dark:text-white"
  >
    <li id="download-svg">
      <button
        class="px-3 pb-1 hover:text-orange-200"
        class:grey-out={disableSVG}
        onclick={() => ondownload?.("svg")}
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
        onclick={() => ondownload?.("png")}
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
        onclick={() => ondownload?.("webp")}
      >
        <FileImageIcon /> WebP
      </button>
    </li>

    <span>|</span>

    <li id="download-json">
      <button
        class="px-3 pb-1 hover:text-orange-200"
        onclick={() => ondownload?.("json")}
      >
        <FileCodeIcon />
        JSON
      </button>
    </li>

    <li id="download-csv">
      <button
        class="px-3 pb-1 hover:text-orange-200"
        class:grey-out={disableCSV}
        onclick={() => ondownload?.("csv")}
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
