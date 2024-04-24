<script lang="ts">
    import { fade } from "svelte/transition"
    import { clickOutside } from "$lib/accountability/clickOutside"

    export let visible = false
    export let extraClass = ""

    function handleClickOutside(event) {
        visible = false;
    }
</script>

{#if visible}
    <div class="{extraClass} flex flex-col bg-white rounded-lg border border-a-gray-200 shadow-a-md"
        use:clickOutside on:clickoutside={handleClickOutside}
        in:fade={{ duration: 150 }} >
        <slot />
    </div>
{/if}