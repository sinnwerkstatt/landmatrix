<script lang="ts">
  export const checkbox = false
  export let ncol: number = 2 // To define if auto layout needed
  export let gridColsTemplate: string = `repeat(${ncol}, 1fr)` // CSS grid-template-columns rules
  export let divider = true

  $: gridColsStyle = `grid-template-columns: ${gridColsTemplate};`
</script>

<div
  class="grid {divider ? 'divide-x divide-a-gray-200' : ''}"
  class:divider
  style={gridColsStyle}
>
  <slot />
</div>

<style>
  div {
    @apply h-fit w-full;
    @apply bg-white;
    @apply border-b border-a-gray-200;
  }
</style>
