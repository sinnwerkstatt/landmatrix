<script lang="ts">
  import { showContextBar } from "./index";
  import Wimpel from "./Wimpel.svelte";

  // showContextBar(state) {
  //   this.$emit("visibility-changed", state);
  // },
</script>

<div
  class="absolute bg-white/95 top-0 right-0 bottom-0 z-10 flex text-sm drop-shadow-[-3px_3px_3px_rgba(0,0,0,0.3)] {$showContextBar
    ? 'w-[clamp(220px,20%,300px)]'
    : 'w-0'}"
>
  <Wimpel
    showing={$showContextBar}
    flipped={true}
    on:click={() => showContextBar.set(!$showContextBar)}
  />
  <div
    class="w-full h-full overflow-y-auto overflow-x-hidden p-2"
    class:hidden={!$showContextBar}
  >
    <slot />
  </div>
</div>
