<script lang="ts">
  import Wimpel from "./Wimpel.svelte"
  import { showContextBar } from "./stores"
</script>

<div
  class="absolute bottom-0 right-0 top-0 z-10 flex bg-white/90 text-sm drop-shadow-[-3px_3px_1px_rgba(0,0,0,0.3)] dark:bg-gray-700 {$showContextBar
    ? 'w-[clamp(220px,20%,300px)]'
    : 'w-0'}"
>
  <Wimpel
    showing={$showContextBar}
    flipped
    on:click={() => showContextBar.set(!$showContextBar)}
  />
  <div
    class="h-full w-full overflow-y-auto overflow-x-hidden p-2"
    class:hidden={!$showContextBar}
  >
    <slot />
  </div>
</div>
