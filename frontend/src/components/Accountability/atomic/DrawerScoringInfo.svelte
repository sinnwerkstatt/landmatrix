<script lang="ts">
    import Badge from "./Badge.svelte"

    export let dealInfo:{label:string, value:string}[]
</script>

<div class="px-4 border rounded-lg flex flex-col divide-y">
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
</div>