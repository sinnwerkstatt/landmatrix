<script lang="ts">
    export let checkbox = false
    export let ncol:number = 2 // To define if auto layout needed
    export let gridColsTemplate:string = `repeat(${ncol}, 1fr)` // CSS grid-template-columns rules

    $: gridColsStyle = `grid-template-columns: ${gridColsTemplate};`
    
</script>

<div class="grid divide-x divide-a-gray-200" style="{gridColsStyle}">
    <slot />
</div>

<style>
    div {
        @apply h-fit w-full;
        @apply bg-white;
        @apply border-b border-a-gray-200;
    }
</style>