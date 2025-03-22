<script lang="ts">
  import type { Snippet } from "svelte"
  import { createFloatingActions } from "svelte-floating-ui"
  import { autoPlacement, offset, shift } from "svelte-floating-ui/dom"

  import InfoIcon from "$components/icons/InfoIcon.svelte"

  interface Props {
    children: Snippet
  }

  let { children }: Props = $props()

  let showTooltip = $state(false)

  const [floatingRef, floatingContent] = createFloatingActions({
    strategy: "absolute",
    middleware: [offset(10), shift(), autoPlacement()],
  })
</script>

<div
  class="p-2"
  role="presentation"
  aria-hidden="true"
  onmouseenter={() => (showTooltip = true)}
  onmouseleave={() => (showTooltip = false)}
  use:floatingRef
>
  <InfoIcon />
</div>

{#if showTooltip}
  <div
    class="absolute w-96 border-2 bg-white p-4 drop-shadow-2xl dark:bg-gray-900 dark:text-white"
    use:floatingContent
  >
    {@render children()}
  </div>
{/if}
