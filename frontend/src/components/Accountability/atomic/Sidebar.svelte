<script lang="ts">
    import { slide } from "svelte/transition"
    import { quintOut } from 'svelte/easing'

    export let transition = true

    let transitionParams

    $: if (transition) {
        transitionParams = {
            delay: 100,
            duration: 500,
            easing: quintOut,
            axis: 'x'
        }
    } else {
        transitionParams = {
            delay: 0,
            duration: 0,
            axis: 'x'
        }
    }

</script>

<div class="h-full w-[14.7rem] shrink-0 px-2 py-6 flex flex-col flex-nowrap content-center
     overflow-hidden border border-a-gray-200 bg-white" 
     transition:slide={transitionParams}>
    <slot />
</div>