<script lang="ts">
    import { createEventDispatcher } from "svelte"

    export let label = "Label"
    export let description = "Description"
    export let value:number|null = null
    export let score:number|null = null

    const dispatch = createEventDispatcher()

    const colors = [
        { value: null, class: "neutral" },
        { value: "NO_SCORE", class: "black" },
        { value: "SEVERE_VIOLATIONS", class: "red" },
        { value: "PARTIAL_VIOLATIONS", class: "yellow" },
        { value: "NO_VIOLATIONS", class: "green" }
    ]

    $: color = colors.find(e => e.value == value)?.class

    function getBehavior(value, score) {
        if (score == null) return ""
        if (value == score) return "active"
        return "dimmed"
    }

    $: behavior = getBehavior(value, score)

    function onClick() {
        dispatch('onClick', { value })
    }

</script>

<button class="p-4 min-w-40 border rounded-lg grow transition-colors {color} {behavior}" on:click={onClick} >
    <h2 class="mb-2 text-left text-a-base font-medium">{label}</h2>
    <p class="m-0 text-left text-a-sm text-a-gray-500 font-normal">{description}</p>
</button>

<style>
    .black {
        @apply bg-a-gray-50 border-a-gray-900;
    }
    .black:hover,
    .black.active {
        @apply bg-a-gray-100;
    }

    .red {
        @apply bg-a-error-50 border-a-error-500;
    }
    .red:hover,
    .red.active {
        @apply bg-a-error-100;
    }

    .yellow {
        @apply bg-a-warning-50 border-a-warning-500;
    }
    .yellow:hover,
    .yellow.active {
        @apply bg-a-warning-100;
    }

    .green {
        @apply bg-a-success-50 border-a-success-700;
    }
    .green:hover,
    .green.active {
        @apply bg-a-success-100;
    }
    
    .dimmed {
        @apply bg-white border-a-gray-200;
    }
    .dimmed:hover {
        @apply bg-a-gray-50;
    }
</style>