<script lang="ts">
    import Pagination from "./Pagination.svelte"

    export let data:[] = []
    export let pageContent = [] // Data that should be displayed in this specific page (pagination)

    let container:HTMLElement

    // Styling
    export let rowHeight = 56;

    let rowsByPage:number;
    let tableHeight = "132";

    let pagination;

    $: tableHeight = (rowsByPage * rowHeight + 34).toString()
</script>

<div class="h-full flex flex-col" >

    <!-- Filters -->
    <div class="p-4 bg-white border-x border-t rounded-t-lg">
        <slot name="filters" />
    </div>

    <!-- Table container for height calculation -->
    <div class="grow" bind:this={container}>
        <div class="flex flex-col border-x overflow-auto" style="height: {tableHeight}px;">
    
            <!-- Header -->
            <div>
                <slot name="header" />
                <!-- <svelte:fragment slot="header"></svelte:fragment> ADD TABLE ROW IN THIS -->
            </div>
        
            <!-- Body -->
            <div class="grow">
                <slot name="body" />
                <!-- <svelte:fragment slot="body"></svelte:fragment> ADD TABLE ROW IN THIS -->
            </div>
        </div>
    
        <div class="min-h-16 p-4 flex justify-between bg-white border-x border-b rounded-b-lg">
            <div class="text-a-sm font-normal text-a-gray-500">
                Showing
                <span class="font-medium text-a-gray-900">{pagination?.first}-{pagination?.last}</span>
                of
                <span class="font-medium text-a-gray-900">{pagination?.total}</span>
            </div>
            <div class="w-40 md:w-96">
                <Pagination detached={true} bind:box={container} bind:dataset={data} bind:pageContent={pageContent} bind:rowsByPage={rowsByPage} {rowHeight} bind:pagination={pagination} justify="end" />
            </div>
        </div>
    </div>

</div>

