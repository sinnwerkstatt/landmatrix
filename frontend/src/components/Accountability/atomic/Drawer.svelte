<script lang="ts">
    import { fade } from "svelte/transition"
    import { slide } from "svelte/transition"
    import { quintOut } from 'svelte/easing'

    export let open = false

    const transitionParams = {
        delay: 100,
        duration: 500,
        easing: quintOut,
        axis: 'x'
    }

</script>

{#if open}
    <div class="absolute top-0 left-0 w-screen h-screen bg-a-gray-900/60 grid justify-end" transition:fade={{ delay: 100, duration: 200 }}>
        <div class="h-full w-screen md:w-[45rem] bg-white" transition:slide={transitionParams} >
            <slot />
        </div>
    </div>
{/if}