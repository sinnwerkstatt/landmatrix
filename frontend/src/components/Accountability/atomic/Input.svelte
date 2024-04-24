<script lang="ts">
    import { preventNonNumericalInput } from "$lib/accountability/inputHelpers"

    import DropdownMenu from "./DropdownMenu.svelte"
    import InputCheckboxGroup from "./InputCheckboxGroup.svelte"
    import Badge from "./Badge.svelte"

    import IconUser from "../icons/IconUser.svelte"
    import IconXMark from "../icons/IconXMark.svelte"
    import IconChevron from "../icons/IconChevron.svelte"
    import IconSearch from "../icons/IconSearch.svelte"
    import IconCheck from "../icons/IconCheck.svelte"

    export let type:"text"|"number"|"multiselect" = "text"
    export let choices:{ value:string, label:string }[] = []
    export let value;

    export let label = ""
    export let placeholder = "Placeholder"
    export let icon = ""
    export let status:"neutral"|"valid"|"invalid" = "neutral"
    export let disabled = false

    // Type number
    export let unit:string = "ha"
    export let min:string = ""
    export let max:string = ""
    export let step:string = "100"

    // Locales
    let open = false
    let filter = ""

    // Functions
    function reset() {
        value = "";
        status = "neutral";
    }

    // function searchMatch(string, searchWord) {
    //     return string.toLowerCase().indexOf(searchWord.toLowerCase())>=0;
    // }
</script>

<div class:disabled class="{status} wrapper wrapper-grid bg-red">

    <!-- Icon -->
    {#if icon != ""}
        <span><IconUser size=16 /></span>
    {/if}

    <!-- Input -->
    {#if type == "text"}
        <input {disabled} type="text" name="name" {placeholder} bind:value class="w-full bg-transparent"
            class:noIcon={icon == "" ? true : false} />

    {:else if type == "multiselect"}
        <button {disabled} on:click={() => { open = !open }} 
                class="pseudo-input w-full bg-transparent text-left" class:noIcon={icon == "" ? true : false}>
            <span class="placeholder">{placeholder}</span>
        </button>

    {:else if type == "number"}
        <input {disabled} type="number" name="name" pattern="[0-9]+" {placeholder} bind:value {min} {max} {step}
               class="w-full bg-transparent noIcon" on:keypress={preventNonNumericalInput} />
    {/if}
    
    <!-- Right item -->
    {#if type == "text"}
        <button {disabled} on:click={reset}><IconXMark /></button>
    {:else if type == "multiselect"}
        <button {disabled} on:click={() => { open = !open }} class="rotate-180"><IconChevron /></button>
    {:else if type == "number"}
        <span>{unit}</span>
    {/if}
</div>

<!-- Dropdown menu for multiselect -->
{#if type == "multiselect" && !disabled && open}
    <div class="absolute z-10 w-[13.5rem] mt-2">
        <DropdownMenu extraClass="pb-4" visible={open}>
            <div class="wrapper wrapper-grid m-4">
                <span><IconSearch /></span>
                <input {disabled} type="text" name="name" placeholder="Search" class="bg-transparent w-full" bind:value={filter} />
                <button {disabled} class="text-red" on:click={() => { filter="" }}><IconXMark /></button>
            </div>

            <div class="max-h-52 overflow-auto">
                <InputCheckboxGroup choices={choices} bind:group={value} {filter} />
            </div>
        </DropdownMenu>
    </div>
{/if}

<!-- Badges for multiselect -->
{#if type == "multiselect" && value instanceof Array && value.length > 0}
    <div class="mt-2 flex flex-wrap gap-1">
        {#each value as val}
            {@const element = choices.find((e) => e.value == val) }
            <Badge color="neutral" button={true} {disabled} label={element?.label}
                   on:click={() => { value = value.filter(v => v != val) }} />
        {/each}
    </div>
{/if}

<style>
    input,
    .pseudo-input {
        @apply relative z-0;
        @apply outline-none;
    }

    input.noIcon,
    .pseudo-input.noIcon {
        @apply col-start-1 col-span-2;
    }

    .wrapper-grid {
        display: grid;
        grid-template-columns: 16px auto 16px;
        @apply items-center gap-2.5;
    }

    .wrapper {
        @apply min-w-32;
        @apply px-4 py-3 rounded-lg border;
        @apply bg-a-gray-50;
        @apply border-a-gray-300;
    }

    .wrapper::placeholder,
    .wrapper .placeholder {
        @apply line-clamp-1;
    }

    .wrapper::placeholder,
    .wrapper .placeholder,
    .wrapper > span,
    .wrapper > button {
        @apply text-a-gray-400;
    }

    .wrapper:focus-within {
        @apply border-a-gray-900;
    }

    .wrapper.disabled,
    .wrapper.disabled > span,
    .wrapper.disabled > button {
        @apply text-a-gray-400;
    }

    .wrapper.disabled > button {
        @apply cursor-default;
    }

    .wrapper.valid,
    .wrapper.valid > span,
    .wrapper.valid > button {
        @apply text-a-success-500 bg-a-success-50;
    }

    .wrapper.valid,
    .wrapper.valid:focus-within {
        @apply border-a-success-500;
    }

    .wrapper.invalid,
    .wrapper.invalid > span,
    .wrapper.invalid > button {
        @apply text-a-error-500 bg-a-error-50;
    }

    .wrapper.invalid,
    .wrapper.invalid:focus-within {
        @apply border-a-error-500;
    }

    label.hide {
        @apply hidden;
    }
</style>