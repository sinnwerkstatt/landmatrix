<script lang="ts">
  import type { Snippet } from "svelte"
  import { twMerge } from "tailwind-merge"

  import { showContextBar } from "./stores"
  import Wimpel from "./Wimpel.svelte"

  interface Props {
    children?: Snippet
  }

  let { children }: Props = $props()
</script>

<div
  class={twMerge(
    "absolute bottom-0 right-0 top-0 z-10 flex bg-white/90 text-sm shadow-inner drop-shadow-[-3px_3px_1px_rgba(0,0,0,0.3)] dark:bg-gray-700",
    $showContextBar ? "w-[clamp(220px,20%,400px)]" : "w-0",
  )}
>
  <Wimpel
    showing={$showContextBar}
    flipped
    onclick={() => showContextBar.set(!$showContextBar)}
  />
  <div class="h-full w-full overflow-y-auto p-2 lg:p-3" class:hidden={!$showContextBar}>
    {@render children?.()}
  </div>
</div>
