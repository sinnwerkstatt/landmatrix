<script lang="ts">
    export let extraClass = ""
</script>

<div class="p-4 rounded-lg border border-a-gray-200 bg-white {extraClass}">
    <slot />
</div>