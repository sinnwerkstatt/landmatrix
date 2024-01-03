<script lang="ts">
  import { clickOutside } from "$lib/helpers"

  let detailsElement: HTMLDetailsElement

  const closeSummary = () => {
    if (detailsElement) detailsElement.removeAttribute("open")
  }
</script>

<details bind:this={detailsElement} class="whitespace-nowrap">
  <summary on:outClick={closeSummary} use:clickOutside>
    <slot name="summary" />
  </summary>
  <slot name="details" />
</details>

<style>
  details > summary {
    list-style: none;
  }
  details > summary::-webkit-details-marker {
    display: none;
  }
</style>
