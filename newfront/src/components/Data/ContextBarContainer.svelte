<script lang="ts">
  import { showContextBar } from "./index"
  import Wimpel from "./Wimpel.svelte"
</script>

<div
  class="absolute top-0 right-0 bottom-0 z-10 flex bg-white/90 text-sm drop-shadow-[-3px_3px_3px_rgba(0,0,0,0.3)] {$showContextBar
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
