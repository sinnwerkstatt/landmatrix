<script lang="ts">
    export let value;
    export let choices:{ value:string, label:string }[] = []
    export let disabled = false
    export let paddingX:string = "4"
</script>

<div class="flex flex-col">
    {#each choices as choice}
        <label class:disabled class="relative grid grid-rows-1 gap-2 place-items-center cursor-pointer hover:bg-a-gray-100 px-{paddingX} py-2"
               style="grid-template-columns: 1rem auto;" >
            <!-- Input -->
            <input type="radio" name={choice.label} value={choice.value} bind:group={value} {disabled}
                   class="peer col-start-1 row-start-1 appearance-none w-4 h-4 rounded-2xl border border-a-gray-300 bg-a-gray-50" />

            <!-- Checked -->
            <span class="col-start-1 row-start-1 w-2.5 h-2.5 rounded-full pointer-events-none bg-a-gray-900 opacity-0 peer-checked:opacity-100" ></span>

            <!-- Label -->
            <span class="col-start-2 row-start-1 w-full select-none text-a-sm font-normal">
                {choice.label}
            </span>
        </label>
    {/each}
</div>

<style>
    input {
        @apply cursor-pointer;
    }
    input:checked {
        @apply bg-a-gray-200;
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
    .disabled > input:checked {
        @apply bg-a-gray-400 border-a-gray-400;
    }
</style>