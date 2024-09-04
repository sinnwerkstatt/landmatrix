<script lang="ts">
    import { onMount } from "svelte"
    import { page } from "$app/stores"
    import { slide } from "svelte/transition"
    import { tableSelection, currentDeal, currentVariable, openDrawer } from "$lib/accountability/stores"
    import { initTableSelection } from "$lib/accountability/helpers"

    import TableRow from "./TableRow.svelte"
    import TableCell from "./TableCell.svelte"
    import Checkbox from "./Checkbox.svelte"
    import IconChevron from "../icons/IconChevron.svelte"
    import BadgeStatus from "./BadgeStatus.svelte"
    import VariableDots from "./VariableDots.svelte"
    import Avatar from "./Avatar.svelte"
    import AvatarGroup from "./AvatarGroup.svelte"

    export let gridColsTemplate = ""
    export let columns = []
    export let deal
    
    let dealChecked = false
    let dealPartiallyChecked = false
    let open = false

    function updateDealCheckbox(selection) {
        if (!$tableSelection[deal.id]?.variables) {
            dealChecked = false
            dealPartiallyChecked = false

        } else {
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

    // ==================================================================================================
    // More checkbox reactivity functions
    function checkDeal(event) {
        const checked = event.detail.checked

        dealPartiallyChecked = false

        if (checked) {
            deal.score.variables.forEach(v => {
                $tableSelection[deal.id].variables[v.vggt_variable] = true
            })
        } else {
            deal.score.variables.forEach(v => {
                $tableSelection[deal.id].variables[v.vggt_variable] = false
            })
        }
    }

    $: updateDealCheckbox($tableSelection[deal.id])

    // ==================================================================================================
    // Assignment functions
    function getAllAssignees(array) {
        let result = []
        array.forEach(e => {
            if (e && !result.map(u => u.id).includes(e.id)) result.push(e)
        })
        return result
    }

    $: dealAssignees = getAllAssignees(deal.score.variables?.map(e => e.assignee))

    function removeAssignee() {
        console.log("Remove assignee")
    }

    // ==================================================================================================
    // Opening a deal page or a scoring drawer
    function openVariable(id) {
        currentDeal.set(deal.id)
        currentVariable.set(id)
        openDrawer.set(true) 
    }


</script>

<div class="row">

    <!-- Deal row -->
    <TableRow {gridColsTemplate} >
        <TableCell>
            <div class="flex items-center gap-2">
                <Checkbox paddingX=0 paddingY=0 value={deal.id} bind:partiallyChecked={dealPartiallyChecked}
                        bind:checked={dealChecked} on:changed={checkDeal} />
                <button class="text-a-gray-400 { !open ? 'rotate-180' : '' } " 
                        on:click={() => open = !open}>
                    <IconChevron size="16" />
                </button>
            </div>
        </TableCell>

        {#each columns as column}
            <!-- {@const val = deal[column.value]} -->

            <!-- Deal ID -->
            {#if column.value == "id"}
                <TableCell>
                    <a class="link" href="{$page.url.href}{deal.id}/">Deal #{deal.id}</a>
                    <!-- TODO: New label for new version -->
                </TableCell>

            <!-- Deal Status -->
            {:else if column.value == "status"}
                <TableCell>
                    <BadgeStatus value={deal.score.status} />
                </TableCell>
            
            <!-- Variable Scoring -->
            {:else if column.value == "variables"}
                <TableCell>
                    <VariableDots variables={deal.score.variables} />
                </TableCell>

            <!-- Assignee -->
            {:else if column.value == "assignees"}
                <TableCell>
                    {#if dealAssignees && dealAssignees.length == 1}
                        <Avatar size="sm" label={dealAssignees[0].name} initials={dealAssignees[0].initials} />
                    {:else if dealAssignees && dealAssignees.length > 1}
                        <AvatarGroup size="sm" users={dealAssignees} maxAvatars=4 />
                    {/if}
                </TableCell>

            <!-- Else (simple text) -->
            {:else if column.value == "country"}
                <TableCell>{deal.country.name}</TableCell>
            {/if}

        {/each}
    </TableRow>

    <!-- Variable rows -->
    {#if open}
        <div transition:slide >

            <TableRow {gridColsTemplate} >
                
                {#each deal.score.variables as variable}
                    <TableCell style="nested">
                        <span class="w-fit"><Checkbox paddingX=0 paddingY=0 value={variable.vggt_variable} bind:checked={$tableSelection[deal.id].variables[variable.vggt_variable]} /></span>
                    </TableCell>

                    <TableCell style="nested" >
                        <button class="text-left w-fit underline underline-offset-4" 
                                on:click={() => openVariable(variable.vggt_variable)} >
                            Variable {variable.vggt_variable}
                        </button>
                    </TableCell>
                    <TableCell style="nested"></TableCell>

                    <TableCell style="nested">
                        <BadgeStatus type="dot" value={variable.status} />
                    </TableCell>

                    <TableCell style="nested">
                        {#if variable.assignee}
                            <Avatar size="sm" label={variable.assignee?.name} initials={variable.assignee?.initials}
                                    buttonOnHover={true} on:click={removeAssignee} />
                        {/if}
                    </TableCell>

                    <TableCell style="nested"></TableCell>
                {/each}
            </TableRow>
            
        </div>
    {/if}


</div>