<script lang="ts">
    import { fade } from "svelte/transition"

    import Button from "./Button.svelte"
    import IconXMark from "./icons/IconXMark.svelte"

    export let open:boolean = false
    export let extraClass:string = ""
    export let title:string;
    export let large:boolean = false
    export let confirmLabel = "Save"
    export let disabled = false
</script>

{#if open}
    <div class="absolute z-30 left-0 top-0 w-screen h-screen bg-a-gray-900/50 grid place-items-center md:p-12" transition:fade={{ duration: 100 }}>
        <div class="relative flex flex-col min-w-[30rem] max-h-full max-h-full bg-white rounded-lg overflow-hidden shadow-a-md {extraClass}"
             class:large>
            <div class="header text-center text-a-xl font-semibold border-b">
                {title}
                <button class="absolute right-4 top-4 text-a-gray-400" {disabled} on:click={() => open = false}><IconXMark size="24" /></button>
            </div>
            <div class="px-14 py-4 overflow-auto">
                <slot />
            </div>
            <div class="footer flex justify-center gap-4 border-t">
                <Button label="Cancel" style="neutral" type="outline" {disabled} on:click={() => open = false} />
                <Button label={confirmLabel} style="neutral" {disabled} on:click />
            </div>
        </div>
    </div>
{/if}

<style>
    .header,
    .footer {
        @apply w-full p-6;
    }

    .large {
        @apply w-full md:w-10/12 lg:w-8/12 2xl:w-1/2;
    }
</style>