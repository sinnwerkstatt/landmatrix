<script lang="ts">
    import { onMount } from "svelte"
    import { slide } from "svelte/transition"
    import { tableSelection } from "$lib/accountability/stores"

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
    let checkedVariables:number[] = []
    let open = false

    function updateDealCheckbox(selection) {
        const nvar = Object.keys($tableSelection[deal.id].variables).length
        const nselect = Object.values($tableSelection[deal.id].variables).filter(Boolean).length

        if (nvar == nselect) {
            dealChecked = true
        } else {
            dealChecked = false
            nselect > 0 ? dealPartiallyChecked = true : dealPartiallyChecked = false
        }
    }

    onMount(() => {
        const dealSelection = $tableSelection[deal.id]
        if (!dealSelection) $tableSelection[deal.id] = { deal: deal.id, variables: {} }
        deal.variables.forEach(v => {
            if (!$tableSelection[deal.id].variables[v.id]) $tableSelection[deal.id].variables[v.id] = false
        })
        updateDealCheckbox()
    })

    // ==================================================================================================
    // More checkbox reactivity functions
    function checkDeal(event) {
        const checked = event.detail.checked

        dealPartiallyChecked = false

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

    $: dealAssignees = getAllAssignees(deal.variables?.map(e => e.assignee))

    function removeAssignee() {
        console.log("Remove assignee")
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
            {@const val = deal[column.value]}

            <!-- Deal ID -->
            {#if column.value == "id"}
                <TableCell>
                    <a class="link" href="">Deal #{val}</a>
                    <!-- TODO: New label for new version -->
                </TableCell>

            <!-- Deal Status -->
            {:else if column.value == "status"}
                <TableCell>
                    <BadgeStatus value={val} />
                </TableCell>
            
            <!-- Variable Scoring -->
            {:else if column.value == "variables"}
                <TableCell>
                    <VariableDots variables={val} />
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
                <TableCell>{val.name}</TableCell>
            {/if}

        {/each}
    </TableRow>

    <!-- Variable rows -->
    {#if open}
        <div transition:slide >

            <TableRow {gridColsTemplate} >
                
                {#each deal.variables as variable}
                    <TableCell style="nested">
                        <span class="w-fit"><Checkbox paddingX=0 paddingY=0 value={variable.id} bind:checked={$tableSelection[deal.id].variables[variable.id]} /></span>
                    </TableCell>

                    <TableCell style="nested" >Variable {variable.id}</TableCell>
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