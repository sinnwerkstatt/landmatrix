<script lang="ts">
  import type { Snippet } from "svelte"

  interface Props {
    children?: Snippet
    class?: string
  }

  let { children, class: className = "" }: Props = $props()
</script>

{#if children}
  <h1
    class="heading2 mx-auto mb-6 mt-8 w-[clamp(20rem,75%,80rem)] text-center lg:mb-12 lg:mt-16"
  >
    <span class="relative z-10 text-orange {className}">
      {@render children()}
    </span>
  </h1>
{/if}
