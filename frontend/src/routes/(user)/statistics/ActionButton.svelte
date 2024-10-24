<script lang="ts">
  import type { ComponentType } from "svelte"

  export let label: string
  export let icon: ComponentType
  export let highlight: boolean = false
</script>

<button
  class="group flex items-center gap-3 rounded-full p-1 transition-colors hover:bg-gray-50 hover:text-orange dark:hover:bg-gray-700"
  class:text-violet={highlight}
  on:click
  type="button"
>
  <svelte:component this={icon} class="h-8 w-8 transition-colors" />
  <span class="text-2xl transition-colors">
    {label}
  </span>
</button>
