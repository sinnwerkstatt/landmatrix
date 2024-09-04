<script lang="ts">
    import { dealFields } from "$lib/fieldLookups"

    import Badge from "./Badge.svelte"

    // export let dealInfo:{label:string, value:string}[]
    export let deal:{}|undefined
    export let fields:string[]

    // $: console.log(deal)
    // $: console.log(fields)
    $: console.log($dealFields)
</script>

{#if deal}
    <div class="px-4 border rounded-lg flex flex-col divide-y">
        {#each fields as field}
            {@const value = deal[field]}
            {@const label = $dealFields[field].label ?? field}
            <div class="py-2 grid gap-4" style="grid-template-columns: 24rem auto;">
                <div>{label}</div>
                <div class="font-normal text-a-gray-500">
                    <!-- TODO: Parse arrays and objects properly -->
                    {#if value && value.length > 0}
                        {value}
                    {:else}
                        —
                    {/if}
                    <!-- {#if label == "Size"}
                        {value} ha
                    {:else if label == "Investor" && id}
                        <span class="flex gap-4">
                            {name} 
                            <Badge label={id} color="blue" variant="filled" 
                                href="https://landmatrix.org/investor/{id}/" />
                        </span>
                    {:else if value}
                        {value}
                    {:else}
                        —
                    {/if} -->
                </div>
            </div>
        {/each}
    </div>
{/if}

<!-- <div class="px-4 border rounded-lg flex flex-col divide-y">
    {#if deal}
        {#each fields as field}
            {@const value = deal[field]}
            <div class="flex gap-8">
                <p>{field}</p>
                <p>{value}</p>
            </div>
        {/each}
    {/if}
</div> -->

<!-- <div class="px-4 border rounded-lg flex flex-col divide-y">
    {#each dealInfo as {label, value, id, name}}
        <div class="py-2 grid gap-4" style="grid-template-columns: 24rem auto;">
            <div>{label}</div>
            <div class="font-normal text-a-gray-500">
                {#if label == "Size"}
                    {value} ha
                {:else if label == "Investor" && id}
                    <span class="flex gap-4">
                        {name} 
                        <Badge label={id} color="blue" variant="filled" 
                               href="https://landmatrix.org/investor/{id}/" />
                    </span>
                {:else if value}
                    {value}
                {:else}
                    —
                {/if}
            </div>
        </div>
    {/each}
</div> -->