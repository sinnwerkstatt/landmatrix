<script lang="ts">
  import { computePosition } from "@floating-ui/dom";
  import type { Placement } from "@floating-ui/dom";
  import ChevronDownIcon from "$components/icons/ChevronDownIcon.svelte";

  export let title = "";
  export let placement: Placement = "bottom";

  let dropdownMenu;
  let listItem;

  async function showDropdown(e) {
    const referenceElement = e.currentTarget;

    dropdownMenu.style.display = "block";

    await computePosition(referenceElement, dropdownMenu, { placement }).then(
      ({ x = 0, y = 0 }) => {
        Object.assign(dropdownMenu.style, {
          // display: "block",
          left: `${x + 10}px`,
          top: `${y}px`,
        });
      }
    );
  }

  function hideDropdown() {
    dropdownMenu.style.display = "none";
  }

  const handleKeyDown = async (e: KeyboardEvent) => {
    console.log(e.code, e.key);
    // console.log(dropdownMenu.children);
    // dropdownMenu.children[1].focus();
  };

  let isFocused = false;
  let isHover = false;

  const onMouseEnter = (e) => {
    if (!isFocused) {
      showDropdown(e);
    }
    isHover = true;
  };

  const onMouseLeave = (e) => {
    if (!isFocused) {
      hideDropdown();
    }
    isHover = false;
  };

  const onFocusIn = (e) => {
    isFocused = true;
  };

  const onFocusOut = (e) => {
    if (!isHover) {
      hideDropdown();
    }
    isFocused = false;
  };
</script>

<li
  bind:this={listItem}
  class={$$props.class}
  on:mouseenter={onMouseEnter}
  on:mouseleave={onMouseLeave}
  on:focusin={onFocusIn}
  on:focusout={onFocusOut}
  on:keydown={handleKeyDown}
>
  <div class="flex items-center cursor-default gap-2 hover:text-orange p-2">
    {#if title}
      {title} <ChevronDownIcon class="h-3 w-3" />
    {:else}
      <slot name="title" />
    {/if}
  </div>
  <div bind:this={dropdownMenu} class="hidden absolute">
    <slot />
  </div>
</li>
