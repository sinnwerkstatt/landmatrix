<script lang="ts">
    import IconUser from "$components/Accountability/icons/IconUser.svelte"
    import IconXMark from "../icons/IconXMark.svelte"

    export let type:"base"|"assignment" = "base"
    export let size:"sm"|"md"|"lg"|"xl" = "md"
    export let initials = "JD"
    export let label = ""
    export let button = false
    export let padding = false
    export let extraClass = ""

    let iconSize = {
        "sm": "8",
        "md": "14",
        "lg": "18",
        "xl": "32"
    }
</script>

<div class="flex items-center {extraClass}" class:button class:padding>
    <div class="flex items-center justify-center rounded-full {type} {size}">
        {#if type=="base"}
            {initials}
        {:else}
            <IconUser size={iconSize[size]} />
        {/if}
    </div>
    <span class="text-sm pl-2">{label}</span>
    {#if button}
        <button class="text-a-gray-400" on:click><IconXMark size=24 /></button>
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

    .padding {
        @apply p-1;
    }

    .button:hover {
        @apply w-fit rounded-lg;
        @apply bg-a-gray-50;
    }
    .button:hover > div {
        @apply bg-a-gray-200;
    }
</style>