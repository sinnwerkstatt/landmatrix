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
</script>

<li
  bind:this={listItem}
  class={$$props.class}
  on:mouseleave={hideDropdown}
  on:focusout={hideDropdown}
  on:keydown={handleKeyDown}
>
  <button
    class="flex items-center gap-2 hover:text-orange p-2"
    on:mouseenter={showDropdown}
    on:focus={showDropdown}
  >
    {#if title}
      {title} <ChevronDownIcon class="h-3 w-3" />
    {:else}
      <slot name="title" />
    {/if}
  </button>
  <div bind:this={dropdownMenu} class="hidden absolute">
    <slot />
  </div>
</li>
