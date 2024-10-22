<script lang="ts">
  import { fade } from "svelte/transition"

  import IconUser from "$components/Accountability/icons/IconUser.svelte"

  import IconXMark from "../icons/IconXMark.svelte"
  import Card from "./Card.svelte"

  export let type: "base" | "assignment" = "base"
  export let size: "sm" | "md" | "lg" | "xl" = "md"
  export let initials = "JD"
  export let label = ""
  export let button = false
  export let buttonOnHover = false
  export let padding = false
  export let extraClass = ""
  export let ring = false
  export let tooltip = true
  export let disabled = false

  // export let surname = "Surname"
  export let name = "Name"
  export let mail = "name@mail.com"
  export let description = "Description"

  let iconSize = {
    sm: "8",
    md: "14",
    lg: "18",
    xl: "32",
  }

  let bubble: HTMLElement
  let popupVisible = false
  let popupTop: number = 0
  let popupLeft: number = 0

  const popupMargin = 20
  const popupGap = 10
  const popupHeight = 183 + popupGap
  const popupWidth = 240 + popupGap

  function showPopup() {
    const windowHeight = window.innerHeight
    const windowWidth = window.innerWidth

    const bubbleLeft = bubble.getBoundingClientRect().x
    const bubbleTop = bubble.getBoundingClientRect().y
    const bubbleHeight = bubble.getBoundingClientRect().height

    // Horizontal positioning
    const deltaLeft = bubbleLeft - popupWidth / 2 - popupMargin
    const deltaRight = bubbleLeft + popupWidth / 2 + popupMargin

    if (popupWidth < windowWidth && deltaLeft < 0) {
      popupLeft = popupMargin
    } else if (popupWidth < windowWidth && deltaRight > windowWidth) {
      popupLeft = windowWidth - popupWidth - popupMargin
    } else {
      popupLeft = bubbleLeft - popupWidth / 2
    }

    // Vertical positioning
    const positionY = bubbleTop > windowHeight / 2 ? "top" : "bottom"
    popupTop = positionY == "top" ? bubbleTop - popupHeight : bubbleTop + bubbleHeight

    popupVisible = true
  }

  function hidePopup() {
    popupVisible = false
  }

  function showButton() {
    if (!button && buttonOnHover) button = true
  }

  function hideButton() {
    if (buttonOnHover) button = false
  }

  function mouseEnter() {
    showButton()
    showPopup()
  }

  function mouseLeave() {
    hideButton()
    hidePopup()
  }
</script>

<div
  class="flex w-full items-center overflow-hidden {extraClass}"
  class:button
  class:padding
  role="tooltip"
  class:disabled
  on:mouseleave={mouseLeave}
  on:mouseenter={mouseEnter}
>
  <div
    class="icon flex shrink-0 items-center justify-center rounded-full {type} {size} select-none"
    class:ring
    role="tooltip"
    bind:this={bubble}
  >
    {#if type == "base"}
      {initials}
    {:else}
      <IconUser size={iconSize[size]} />
    {/if}
  </div>

  {#if label}
    <span
      class="select-none truncate text-nowrap pl-2 text-sm {type == 'assignment'
        ? 'text-a-gray-400'
        : ''}"
    >
      {label}
    </span>
  {/if}

  {#if button}
    <button class="pl-1 text-a-gray-400" on:click {disabled}>
      <IconXMark size="24" />
    </button>
  {/if}

  <!-- Popup with user info -->
  {#if type == "base" && tooltip && popupVisible}
    <div
      class="tooltip-bg fixed z-20 grid place-content-center"
      style="height: {popupHeight}px; width: {popupWidth}px; top: {popupTop}px; left: {popupLeft}px;"
      transition:fade={{ delay: 100, duration: 150 }}
    >
      <Card extraClass="h-[183px] w-60 shadow-a-md">
        <div class="flex h-full w-full flex-col items-center justify-center gap-1">
          <div class="grid h-12 w-12 place-content-center rounded-full bg-a-gray-100">
            {initials}
          </div>
          <div class="text-a-lg font-semibold">
            <span>{name}</span>
            <!-- <span class="uppercase">{surname}</span> -->
          </div>
          <div class="font-normal text-a-gray-500 underline">{mail}</div>
          <div class="font-normal text-a-gray-500">{description}</div>
        </div>
      </Card>
    </div>
  {/if}
</div>

<style>
  /* Type styling */
  .base {
    @apply bg-a-gray-100;
  }
  .assignment {
    @apply text-a-gray-200;
    @apply border-2 border-dashed border-a-gray-200;
  }

  /* Size styling */
  .sm {
    @apply h-[24px] w-[24px];
    @apply text-a-xs;
  }
  .md {
    @apply h-[32px] w-[32px];
    @apply text-a-sm;
  }
  .lg {
    @apply h-[48px] w-[48px];
    @apply text-a-base;
  }
  .xl {
    @apply h-[104px] w-[104px];
    @apply text-a-3xl;
  }

  .padding {
    @apply p-1;
  }

  .button:hover {
    @apply rounded-lg;
    @apply bg-a-gray-50;
  }
  .button:hover > div {
    @apply bg-a-gray-200;
  }

  .ring {
    @apply ring-white;
  }

  .tooltip-bg,
  .tooltip-bg:hover {
    @apply !bg-transparent;
  }

  .disabled,
  .disabled > .icon {
    @apply text-a-gray-400;
  }

  .disabled:hover {
    @apply bg-white;
  }
</style>
