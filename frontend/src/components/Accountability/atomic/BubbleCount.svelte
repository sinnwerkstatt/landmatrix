<script>
    export let size = "base" // base, sm, lg
    export let count = 0; // Any number
</script>

<span class="bubble {size}">
    {#if count > 99}
        <span class="smaller">99+</span>
    {:else}
        <span>{count}</span>
    {/if}
</span>

<style>
    .bubble {
        @apply w-4 h-4;
        @apply flex place-content-center pt-0.5;
        @apply text-white text-a-xs;
        @apply bg-a-primary-500 rounded-full;
        @apply ring-[1.5px] ring-white;
    }

    .bubble.sm {
        @apply w-2 h-2;
    }
    .bubble.sm > span {
        @apply hidden;
    }

    .bubble.lg {
        @apply w-6 h-6;
        @apply text-a-sm;
    }

    .smaller {
        @apply text-[0.5rem];
    }

    .lg .smaller {
        @apply text-a-xs pt-1;
    }
</style>