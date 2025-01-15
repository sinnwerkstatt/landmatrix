<script lang="ts">
  import { quintOut } from "svelte/easing"
  import { fade, slide } from "svelte/transition"

  interface Props {
    open?: boolean
    children?: import("svelte").Snippet
  }

  let { open = $bindable(false), children }: Props = $props()

  const transitionParams = {
    delay: 100,
    duration: 500,
    easing: quintOut,
    axis: "x",
  }
</script>

{#if open}
  <div
    class="absolute left-0 top-0 grid h-screen w-screen justify-end bg-a-gray-900/60"
    transition:fade={{ delay: 100, duration: 200 }}
  >
    <div
      class="h-full w-screen bg-white md:w-[45rem]"
      transition:slide={transitionParams}
    >
      {@render children?.()}
    </div>
  </div>
{/if}
