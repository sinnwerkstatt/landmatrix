<script lang="ts">
    import IconMove from "../icons/IconMove.svelte"
    import IconEllipsis from "../icons/IconEllipsis.svelte"

    export let label = "label"
    export let state = "default"
    export let menu = false
    export let handle = false
    export let active = false
</script>

<button class="{state}" class:active>
        <div class="flex items-center gap-2">
            {#if handle}
                <span class="shrink-0 cursor-move" draggable="true"><IconMove /></span>
            {/if}
            {label}
        </div>
        {#if menu}
            <span class="text-a-gray-400"><IconEllipsis /></span>
        {/if}
</button>

<style>
    button {
        @apply flex items-center justify-between gap-2;
        @apply px-4;
        @apply h-14 w-full;
        @apply shrink-0;
        @apply text-a-sm text-left font-medium;
        @apply bg-white;
        @apply border-b-2 border-a-gray-200;
    }
    button:hover,
    button.active {
        @apply bg-a-gray-100;
        @apply border-transparent rounded-lg;
    }
</style>