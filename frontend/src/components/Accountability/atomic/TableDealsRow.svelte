<script lang="ts">
    import { slide } from "svelte/transition"

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

    let open = false
    let dealChecked = false
    let dealPartiallyChecked = false
    let selectedVariables:number[] = []

    function getAllAssignees(array) {
        let result = []
        array.forEach(e => {
            if (e && !result.map(u => u.id).includes(e.id)) result.push(e)
        })
        return result
    }

    $: dealAssignees = getAllAssignees(deal.variables?.map(e => e.assignee))

    // ==================================================================================================
    // Checkbox functions
    function checkDeal(event) {
        const deal_id = event.detail.value
        const checked = event.detail.checked
       
        if (checked) {
            selectedVariables = deal.variables.map(e => e.id)
        } else {
            selectedVariables = []
        }
    }

    function checkVariable(event) {
        const variable_id = event.detail.value
        const checked = event.detail.checked

        if (checked) {
            selectedVariables = [...selectedVariables, variable_id]
        } else {
            selectedVariables = selectedVariables.filter(e => e != variable_id)
        }
    }

    function updateDealCheckbox(deal, selectedVariables) {
        if (deal.variables.length == selectedVariables.length) {
            dealChecked = true
        } else if (selectedVariables.length > 0) {
            dealChecked = false
            dealPartiallyChecked = true
        } else {
            dealChecked = false
            dealPartiallyChecked = false
        }

    }

    $: updateDealCheckbox(deal, selectedVariables)

    // ==================================================================================================
    // Assignment functions
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
                    {@const checked = selectedVariables.includes(variable.id)}
                    <TableCell style="nested">
                        <span class="w-fit"><Checkbox paddingX=0 paddingY=0 value={variable.id} checked={checked} on:changed={checkVariable} /></span>
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