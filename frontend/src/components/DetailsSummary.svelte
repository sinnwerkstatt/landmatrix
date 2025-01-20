<script lang="ts">
  import type { Snippet } from "svelte"

  import { clickOutside } from "$lib/helpers"

  interface Props {
    summary?: Snippet
    details?: Snippet
  }

  let { summary, details }: Props = $props()

  let detailsElement: HTMLDetailsElement | undefined = $state()

  const closeSummary = () => {
    if (detailsElement) detailsElement.removeAttribute("open")
  }
</script>

<details bind:this={detailsElement} class="whitespace-nowrap">
  <summary onoutClick={closeSummary} use:clickOutside>
    {@render summary?.()}
  </summary>
  {@render details?.()}
</details>

<style>
  details > summary {
    list-style: none;
  }
  details > summary::-webkit-details-marker {
    display: none;
  }
</style>
