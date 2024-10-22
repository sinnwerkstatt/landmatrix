<script lang="ts">
  import { quintOut } from "svelte/easing"
  import { slide } from "svelte/transition"

  export let transition = true

  let transitionParams

  $: if (transition) {
    transitionParams = {
      delay: 100,
      duration: 500,
      easing: quintOut,
      axis: "x",
    }
  } else {
    transitionParams = {
      delay: 0,
      duration: 0,
      axis: "x",
    }
  }
</script>

<div
  class="flex h-full w-[14.7rem] shrink-0 flex-col flex-nowrap content-center overflow-hidden border
     border-a-gray-200 bg-white px-2 py-6"
  transition:slide={transitionParams}
>
  <slot />
</div>
