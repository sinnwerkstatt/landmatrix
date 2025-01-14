<script lang="ts">
  import { fade } from "svelte/transition"

  import { clickOutside } from "$lib/accountability/clickOutside"

  interface Props {
    visible?: boolean
    extraClass?: string
    top: any
    left: any
    children?: import("svelte").Snippet
    onclickoutside?: () => void
  }

  let {
    visible = $bindable(false),
    extraClass = "",
    top,
    left,
    children,
    onclickoutside,
  }: Props = $props()

  function handleClickOutside() {
    visible = false
  }
</script>

{#if visible}
  <div
    class="{extraClass} flex flex-col rounded-lg border border-a-gray-200 bg-white shadow-a-md"
    style="{top ? `top:${top}px;` : ''} {left ? `left:${left}px;` : ''}"
    use:clickOutside
    onclickoutside={handleClickOutside}
    in:fade={{ duration: 150 }}
  >
    {@render children?.()}
  </div>
{/if}
<!-- Not sur if the onclickoutside needs to be changed and how -->
