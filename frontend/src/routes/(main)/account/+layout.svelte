<script lang="ts">
  import type { Snippet } from "svelte"

  interface Props {
    children?: Snippet
  }

  let { children }: Props = $props()
</script>

<div class="mt-12 flex h-5/6 items-center justify-center">
  <div class="w-[clamp(300px,80%,800px)] border border-neutral-600 p-6">
    {@render children?.()}
  </div>
</div>
