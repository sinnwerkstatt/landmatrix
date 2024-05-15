<script lang="ts">
    export let label = "Embed"
    export let disabled = false
</script>

<button {disabled} class="border border-a-gray-200 px-1.5 py-0.5 rounded" on:click >
    <span class="line-clamp-1 text-a-sm text-a-gray-900 font-medium">{label}</span>
</button>

<style>
    button:disabled > span {
        @apply text-a-gray-400;
    }
</style>