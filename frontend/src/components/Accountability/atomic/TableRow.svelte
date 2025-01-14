<script lang="ts">
  export const checkbox = false
  interface Props {
    ncol?: number // To define if auto layout needed
    gridColsTemplate?: string // CSS grid-template-columns rules
    divider?: boolean
    children?: import("svelte").Snippet
  }

  let {
    ncol = 2,
    gridColsTemplate = `repeat(${ncol}, 1fr)`,
    divider = true,
    children,
  }: Props = $props()

  let gridColsStyle = $derived(`grid-template-columns: ${gridColsTemplate};`)
</script>

<div
  class="grid {divider ? 'divide-x divide-a-gray-200' : ''}"
  class:divider
  style={gridColsStyle}
>
  {@render children?.()}
</div>

<style>
  div {
    @apply h-fit w-full;
    @apply bg-white;
    @apply border-b border-a-gray-200;
  }
</style>
