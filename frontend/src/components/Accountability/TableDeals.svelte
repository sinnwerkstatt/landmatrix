<script lang="ts">
    import Table from "./atomic/Table.svelte"
    import TableRow from "./atomic/TableRow.svelte"
    import TableCell from "./atomic/TableCell.svelte"
    import TableDealsRow from "./atomic/TableDealsRow.svelte"

    import Input from "./atomic/Input.svelte"
    import Checkbox from "./atomic/Checkbox.svelte"
    import type { forEach } from "ramda"
    import { map } from "leaflet?client"

    export let deals:{
        id:number,
        country: {id:number, name:string},
        status:string,
        variables:{id:number, 
                status:string, 
                score:number|null, 
                assignee:{id:number, name:string}|null}[]
    }[] = []

    const columns:{label:string, value:string}[] = [
        { label: "id", value: "id" },
        { label: "status", value: "status" },
        { label: "variable scoring", value: "variables" },
        { label: "assignee", value: "assignees" },
        { label: "country", value: "country" }
    ]

    const gridColsTemplate = "52px repeat(5, 1fr)"

    let pageContent = []
    let searchWord:string = ""

    let searchResult = deals

    function search(searchWord) {
        if (searchWord == "") {
            return deals

        } else {
            const via_id = deals.filter(e => (e.id).toString().includes(searchWord))
            const via_country = deals.filter(e => e.country.name.toLowerCase().includes(searchWord.toLowerCase()))

            let results = via_id
            let included_ids = results.map(e => e.id)

            // Add other search results if they're not already included
            via_country.forEach(e => {
                if (!included_ids.includes(e.id)) results.push(e)
            })

            // Sort results by id
            results.sort((a, b) => a.id - b.id)

            // Return
            return results
        }
    }

    $: searchResult = search(searchWord)

</script>

<Table bind:data={searchResult} bind:pageContent={pageContent} rowHeight=57 >

    <!-- Table filters -->
    <div slot="filters" class="flex justify-between">
        <div><Input type="text" icon="search" placeholder="Search for a deal" bind:value={searchWord} /></div>
        <div>Right</div>
    </div>

    <!-- Table header -->
    <svelte:fragment slot="header">
        <TableRow {gridColsTemplate} >
            <TableCell style="heading" >
                <div class="w-fit">
                    <Checkbox paddingX=0 paddingY=0 />
                </div>
            </TableCell>

            {#each columns as { label }}
                <TableCell style="heading" >{label.toUpperCase()}</TableCell>
            {/each}
        </TableRow>
    </svelte:fragment>

    <!-- Table body and footer -->
    <svelte:fragment slot="body">
        {#each pageContent as deal}
            <TableDealsRow {gridColsTemplate} {columns} {deal} />
        {/each}
    </svelte:fragment>

</Table>