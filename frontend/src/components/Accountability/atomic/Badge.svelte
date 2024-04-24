<script lang="ts">
    import IconCheck from "../icons/IconCheck.svelte"
    import IconEye from "../icons/IconEye.svelte"
    import IconBookmark from "../icons/IconBookmark.svelte"
    import IconXMark from "../icons/IconXMark.svelte"

    export let label = "Badge"
    export let notification = false
    export let button = false
    export let disabled = false

    export let size: "base"|"small" = "small"
    export let icon: ""|"check"|"eye"|"bookmark" = ""
    export let color: "primary"|"warning"|"error"|"success"|"neutral"|"blue" = "primary"
    export let variant: "filled"|"light" = "light"

    $: iconSize = size == "base" ? "24" : "16";

    const icons = [
        { icon: "check", component: IconCheck },
        { icon: "eye", component: IconEye },
        { icon: "bookmark", component: IconBookmark }
    ]
</script>

<div class:disabled class="wrapper {size} {icon} {color} {variant}" >
    {#if icon}
        <svelte:component this={icons.find(e => e.icon == icon)?.component} />
    {/if}

    {#if notification}
        <div class="notification inline-block rounded-xl"></div>
    {/if}

    <span class="line-clamp-1">{label}</span>

    {#if button}
        <button {disabled} on:click >
            <IconXMark size={iconSize} />
        </button>
    {/if}
</div>

<style>
    .wrapper {
        @apply w-fit h-9;
        @apply px-4;
        @apply flex gap-1.5 items-center;
        @apply rounded;
        @apply text-a-base font-medium;
    }

    .wrapper > .notification {
        @apply w-3 h-3;
    }

    .wrapper.small {
        @apply h-[1.375rem];
        @apply px-2;
        @apply text-a-sm;
    }

    .wrapper.small .notification {
        @apply w-2 h-2;
    }

    /* Disabled */
    .wrapper.disabled {
        @apply !text-a-gray-400;
        @apply !bg-a-gray-100 ;
    }
    .wrapper.disabled > .notification {
        @apply !bg-a-gray-400;
    }

    /* Light color variants */
    .light.primary {
        @apply text-a-primary-500 bg-a-primary-200;
    }
    .light.primary > .notification {
        @apply bg-a-primary-500;
    }

    .light.warning {
        @apply text-a-warning-600 bg-a-warning-100;
    }
    .light.warning > .notification {
        @apply bg-a-warning-600;
    }

    .light.error {
        @apply text-a-error-500 bg-a-error-100;
    }
    .light.error > .notification {
        @apply bg-a-error-500;
    }

    .light.success {
        @apply text-a-success-600 bg-a-success-100;
    }
    .light.success > .notification {
        @apply bg-a-success-600;
    }

    .light.neutral {
        @apply text-a-gray-800 bg-a-gray-100;
    }
    .light.neutral > .notification {
        @apply bg-a-gray-800;
    }

    /* Filled color variants */
    .filled {
        @apply text-white;
    }
    .filled > .notification {
        @apply bg-white;
    }

    .filled.primary {
        @apply bg-a-primary-500;
    }
    .filled.warning {
        @apply bg-a-warning-500;
    }
    .filled.error {
        @apply bg-a-error-500;
    }
    .filled.success {
        @apply bg-a-success-500;
    }
    .filled.neutral {
        @apply bg-a-gray-800;
    }

    .blue {
        @apply bg-a-blue;
    }
</style>