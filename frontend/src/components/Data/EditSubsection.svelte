<script lang="ts">
  import type { Snippet } from "svelte"

  import { objectSections } from "$lib/sections"

  interface Props {
    id: string
    children?: Snippet
  }

  let { id, children }: Props = $props()

  let sec = $derived($objectSections[id])
</script>

<div class="mt-2 space-y-4 pt-6">
  {#if sec.title}
    <h3 class="heading3 my-0">{sec.title}</h3>
  {/if}

  {@render children?.()}
</div>
