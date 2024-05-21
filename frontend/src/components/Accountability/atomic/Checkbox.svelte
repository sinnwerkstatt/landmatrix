<script lang="ts">
    import { createEventDispatcher } from 'svelte'

    import IconCheck from "../icons/IconCheck.svelte"
    import IconMinus from "../icons/IconMinus.svelte"

    export let value = ""
    export let checked = false
    export let partiallyChecked = false
    export let label = ""
    export let bold = false
    export let disabled = false
    export let hidden = false
    export let paddingX:string = "4"
    export let paddingY:string = "2"

    const dispatch = createEventDispatcher()

    function onChange() {
        dispatch('changed', { value, checked })
    }

</script>

<label class:disabled class:hidden
       class="h-fit relative grid grid-rows-1 place-items-center cursor-pointer hover:bg-a-gray-100 px-{paddingX} py-{paddingY}"
       style="grid-template-columns: 1rem auto;">

    <!-- Checkbox -->
    <input type="checkbox" name="input" {value} bind:checked on:change={onChange} {disabled}
           class="col-start-1 row-start-1 appearance-none w-4 h-4 rounded border border-a-gray-300 bg-a-gray-50" 
           class:partiallyChecked />

    <!-- Checked svg -->
    <span class="col-start-1 row-start-1 z-10 pointer-events-none text-a-gray-50">
        {#if checked}
            <IconCheck />
        {:else if partiallyChecked}
            <IconMinus size="16" />
        {/if}
    </span>

    <!-- Label -->
    {#if label}
        <span class="pl-2 col-start-2 row-start-1 w-full select-none text-a-sm font-normal" class:bold>
            {label}
        </span>
    {/if}

</label>

<style>
    .bold {
        @apply font-semibold;
    }

    .partiallyChecked {
        @apply border-a-gray-400;
        @apply bg-a-gray-400;
    }

    input {
        @apply cursor-pointer;
    }
    input:checked {
        @apply border-a-gray-900;
        @apply bg-a-gray-900;
    }

    .disabled {
        @apply cursor-default;
        @apply text-a-gray-400;
    }
    .disabled:hover {
        @apply bg-white;
    }
    .disabled > input {
        @apply cursor-default;
    }
    .disabled > input:checked,
    .disabled > input.partiallyChecked {
        @apply bg-a-gray-400 border-a-gray-400;
    }
</style>