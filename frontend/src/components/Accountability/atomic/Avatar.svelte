<script lang="ts">
    import IconUser from "$components/Accountability/icons/IconUser.svelte"

    export let type = "base" // assignment, base
    export let size = "md" // sm, md, lg, xl
    export let initials = "JD"

    let iconSize = {
        "sm": "8",
        "md": "14",
        "lg": "18",
        "xl": "32"
    }
</script>

<div class="flex items-center justify-center rounded-full {type} {size}">
    {#if type=="base"}
        {initials}
    {:else}
        <IconUser size={iconSize[size]} />
    {/if}
</div>

<style>
    /* Type styling */
    .base {
        @apply bg-a-gray-100;
    }
    .assignment {
        @apply text-a-gray-200;
        @apply border-2 border-a-gray-200 border-dashed;
    }

    /* Size styling */
    .sm {
        @apply h-6 w-6;
        @apply text-a-xs;
    }
    .md {
        @apply h-8 w-8;
        @apply text-a-sm;
    }
    .lg {
        @apply h-12 w-12;
        @apply text-a-base;
    }
    .xl {
        @apply h-[6.5rem] w-[6.5rem];
        @apply text-a-3xl;
    }
</style>