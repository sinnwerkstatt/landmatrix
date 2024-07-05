<script lang="ts">
    import { onMount } from "svelte"
    import { tableSelection } from "$lib/accountability/stores"
    import { initTableSelection } from "$lib/accountability/helpers"

    import Table from "./atomic/Table.svelte"
    import TableRow from "./atomic/TableRow.svelte"
    import TableCell from "./atomic/TableCell.svelte"
    import Checkbox from "./atomic/Checkbox.svelte"
    import BadgeStatus from "./atomic/BadgeStatus.svelte"
    import Avatar from "./atomic/Avatar.svelte"

    export let deal:{
        id:number,
        country: {id:number, name:string},
        status:string,
        variables:{id:number, 
                status:string, 
                score:number|null, 
                assignee:{id:number, name:string}|null}[]
    }

    $: data = deal.variables ? deal.variables : []

    const columns:{label:string, value:string}[] = [
        { label: "id", value: "id" },
        { label: "variable scoring", value: "variables" },
        { label: "assignee", value: "assignees" }
    ]

    const gridColsTemplate = "32px repeat(3, 1fr)"

    let pageContent = []
    let dealChecked = false
    let dealPartiallyChecked = false
    
    function updateDealCheckbox(selection) {
        console.log("Updating deal checkbox")
        if (!tableSelection[deal.id]?.variables) {
            const nvar = Object.keys($tableSelection[deal.id].variables).length
            const nselect = Object.values($tableSelection[deal.id].variables).filter(Boolean).length
    
            if (nvar == nselect) {
                dealChecked = true
            } else {
                dealChecked = false
                nselect > 0 ? dealPartiallyChecked = true : dealPartiallyChecked = false
            }
        }
    }

    onMount(() => {
        initTableSelection(deal)
        updateDealCheckbox()
    })

    function checkDeal(event) {
        const checked = event.detail.checked
        
        if (checked) {
            deal.variables.forEach(v => {
                $tableSelection[deal.id].variables[v.id] = true
            })
        } else {
            deal.variables.forEach(v => {
                $tableSelection[deal.id].variables[v.id] = false
            })
        }
    }

    function removeAssignee() {
        console.log("Remove assignee")
    }

    $: updateDealCheckbox($tableSelection)

</script>

<Table {data} bind:pageContent={pageContent} filters={false} rowHeight=57>

    <!-- Table header -->
    <svelte:fragment slot="header" >
        <TableRow {gridColsTemplate}>
            <TableCell style="heading" >
                <div class="w-fit">
                    <Checkbox paddingX=0 paddingY=0 on:changed={checkDeal}
                     bind:checked={dealChecked} bind:partiallyChecked={dealPartiallyChecked} />
                </div>
            </TableCell>

            {#each columns as column(column.value)}
                <TableCell style="heading">{column.label.toUpperCase()}</TableCell>
            {/each}

        </TableRow>
    </svelte:fragment>

    <!-- Table body -->
    <svelte:fragment slot="body">
        {#each pageContent as variable (variable.id)}
            <TableRow {gridColsTemplate}>
                <!-- Checkbox -->
                <TableCell>
                    <div class="w-fit">
                        <Checkbox paddingX=0 paddingY=0 value={variable.id}
                         bind:checked={$tableSelection[deal.id].variables[variable.id]} />
                    </div>
                </TableCell>

                <!-- ID -->
                <TableCell>{variable.id}</TableCell>

                <!-- Scoring status -->
                <TableCell>
                    <BadgeStatus type="dot" value={variable.status} />
                </TableCell>

                <!-- Assignee -->
                <TableCell>
                    {#if variable.assignee}
                        <Avatar size="sm" label={variable.assignee?.name} initials={variable.assignee?.initials}
                                buttonOnHover={true} on:click={removeAssignee} />
                    {/if}
                </TableCell>

            </TableRow>
        {/each}
    </svelte:fragment>

</Table>