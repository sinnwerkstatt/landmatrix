<script lang="ts">
    import { page } from "$app/stores"
    import { updateDealVariable } from "$lib/accountability/scores"
    import { scoreLabels, vggtInfo } from "$lib/accountability/vggtInfo"
    import { currentDeal, currentVariable, openDrawer, deals } from "$lib/accountability/stores"

    import Drawer from "./atomic/Drawer.svelte"
    import DrawerScoringItem from "./atomic/DrawerScoringItem.svelte"
    import Badge from "./atomic/Badge.svelte"
    import Input from "./atomic/Input.svelte"
    import Avatar from "./atomic/Avatar.svelte"
    import IconXMark from "./icons/IconXMark.svelte"
    import Section from "./atomic/Section.svelte"
    import DrawerScoringInfo from "./atomic/DrawerScoringInfo.svelte"
    import Button from "./Button.svelte"
    import Modal from "./Modal.svelte"

    let pendingChanges = false
    let openNavigationConfirmationModal = false
    let navigationAction:"previous"|"next"|"quit"|undefined = undefined

    let vggtArticles = $page.data.vggtArticles
    let vggtVariables = $page.data.vggtVariables
    let vggtVariableNumbers = vggtVariables.map(v => v.number).sort((a,b) => a - b)

    $: variableInfo = vggtVariables.filter(v => v.number == $currentVariable)[0]

    $: deal = $deals.find(deal => deal.id == $currentDeal) ?? undefined
    $: variable = deal?.score?.variables.find(v => v.vggt_variable == $currentVariable)
    $: score = variable?.score ?? undefined
    $: status = variable?.status ?? ''

    const selectableStatuses = [
        { value: "VALIDATED", label: "Validated" },
        { value: "WAITING", label: "Waiting for review" }
    ]

    const statuses = [
        { value: "TO_SCORE", label: "To score" },
        ...selectableStatuses
    ]

    function selectScore(event) {
        const value = event.detail.value

        // Select the new score
        if (score != "NO_SCORE" && score == value) { // If clicking on selected, unselect (= "NO_SCORE")
            score = "NO_SCORE"
        } else {
            score = value
        }

        // Check if the user changed the score
        const currentScore = deal.score.variables.find(v => v.vggt_variable == $currentVariable).score
        currentScore != score ? pendingChanges = true : pendingChanges = false

        // Update the status
        if (value == 0) {
            status = "TO_SCORE"
        } else {
            if (!["WAITING", "VALIDATED"].includes(status)) status = "VALIDATED"
        }
    }

    function isPreviousAvailable(current) {
        const index = vggtVariableNumbers.findIndex(n => n == current)
        if (index - 1 >= 0) return true
        return false
    }

    function isNextAvailable(current) {
        const index = vggtVariableNumbers.findIndex(n => n == current)
        const length = vggtVariableNumbers.length
        if (index + 1 < length) return true
        return false
    }

    $: previousAvailable = isPreviousAvailable($currentVariable)
    $: nextAvailable = isNextAvailable($currentVariable)

    function navigate(action:"previous"|"next"|"quit") {
        switch (action) {
            case "previous":
            if (previousAvailable) currentVariable.set($currentVariable-1)
                break
            case "next":
            if (nextAvailable) currentVariable.set($currentVariable+1)
                break
            case "quit":
                openDrawer.set(false)
                break
            default:
                break
        }
    }

    function navigationConfirmationModal(action:"previous"|"next"|"quit") {
        if (pendingChanges) {
            navigationAction = action
            openNavigationConfirmationModal = true
        } else {
            navigate(action)
        }
    }

    function confirmNavigation() {
        openNavigationConfirmationModal = false
        navigate(navigationAction)
        navigationAction = undefined
    }

    async function save() {
        const deal_id = deal.id
        const variable_number = variable.vggt_variable
        const body = { status, score }
        try {
            const res = await updateDealVariable(deal_id, variable_number, body)
            if (res.ok) pendingChanges = false
            console.log("===== UPDATING FRONTEND =====")
            console.log($deals)
            
            const deal_index = $deals.findIndex(d => d.id == deal_id)
            const variable_index = $deals.find(d => d.id == deal_id).score.variables.findIndex(v => v.vggt_variable == variable_number)

            const allDeals = $deals


            const newValue = await res.json()

            console.log("--- Value from store ---")
            console.log($deals[deal_index].score.variables[variable_index])

            console.log("--- Value from allDeals ---")
            console.log(allDeals[deal_index].score.variables[variable_index])

            console.log("--- Updated value from allDeals ---")
            allDeals[deal_index].score.variables[variable_index] = newValue
            console.log(allDeals[deal_index].score.variables[variable_index])

            console.log("--- $deals and allDeals ---")
            console.log($deals)
            console.log(allDeals)

            // console.log($deals[deal_index].score.variables)
            // console.log(allDeals[deal_index].score.variables)
            // console.log("---")
            // console.log(allDeals[deal_index].score.variables[variable_index])
            // console.log("---")
            // console.log(newValue)
            // allDeals[deal_index].score.variables[variable_index] = newValue
            // console.log(allDeals[deal_index].score.variables[variable_index])

            
            // console.log(allDeals[deal_index].score.variables[variable_index])
            // console.log($deals[deal_index].score.variables[variable_index])
            // $deals[deal_index].score.variables[variable_index] = newValue

        } catch (error) {
            console.error(error)
            console.error(error.body.message)
        }
    }

</script>

<Drawer bind:open={$openDrawer}>
    <div class="h-screen flex flex-col divide-y divide-a-gray-200">
        <!-- Heading -->
        <div class="p-6">
            <div class="flex justify-between">
                <div class="flex items-center gap-2">
                    <span class="block w-3 h-3 rounded-full indicator"></span>
                    <h1 class="text-a-xl font-semibold">Variable {$currentVariable} - {variableInfo.name}</h1>
                    <Badge variant="filled" label={$currentDeal} href="https://landmatrix.org/deal/{$currentDeal}/" />
                </div>
                <button class="text-a-gray-400" on:click={() => navigationConfirmationModal("quit")}><IconXMark size=24 /></button>
            </div>
            <div class="mt-2 flex gap-4">
                <Input type="select" choices={selectableStatuses} style="white" extraClass="!w-60"
                    search={false} value={status}  />
                <Avatar />
            </div>
        </div>

        <!-- Body -->
        <div class="p-6 h-full w-full overflow-auto">
            <h2>VGGT compliance</h2>
            <div class="flex gap-2">
                {#each variableInfo.score_options as value}
                    {@const label = scoreLabels[value] ?? ""}
                    {@const description = vggtInfo[$currentVariable].score_meaning[value] ?? ""}
                    <DrawerScoringItem {label} {description} {value} {score} on:onClick={selectScore} />
                {/each}
            </div>

            <Section title="Show more details" extraClass="pl-0 underline underline-offset-4" open={false}>
                <!-- Help -->
                {#if vggtInfo[$currentVariable].score_help.length > 0}
                    <h3>Help</h3>
                    <ul>
                        {#each vggtInfo[$currentVariable].score_help as help}
                            <li>{help}</li>
                        {/each}
                    </ul>
                {/if}

                <!-- Resources -->
                <h3>Resources (VGGTs articles linked to this variable)</h3>
                {#each variableInfo.articles as id}
                    {@const item = vggtArticles.find(i => i.id == id)}
                    <ul>
                        <li class="font-semibold">Article {item.chapter}.{item.article} (Chapter {item.chapter}: {item.title})</li>
                        <ul>
                            <li>{item.description}</li>
                        </ul>
                    </ul>
                {/each}
            </Section>

            <!-- LM Info -->
            <h2 class="mt-4">Land Matrix information</h2>
            <DrawerScoringInfo {deal} fields={variableInfo.landmatrix_fields} />
            {#if variableInfo?.landmatrix_additional_fields.length > 0}
                <h4 class="my-4 text-sm font-medium text-a-gray-500">Additional fields</h4>
                <DrawerScoringInfo {deal} fields={variableInfo.landmatrix_additional_fields} />
            {/if}
            <h2 class="mt-10">Deal main information</h2>
            <DrawerScoringInfo {deal} main_info={true} />
        </div>

        <!-- Footer -->
        <div class="p-6 grow-0 flex justify-between">
            <Button label="Previous" type="outline" style="neutral" on:click={() => navigationConfirmationModal("previous")} disabled={!previousAvailable} />
            <div class="flex gap-4">
                <Button label="Next" type="outline" style="neutral" on:click={() => navigationConfirmationModal("next")} disabled={!nextAvailable} />
                <Button label="Save" style="neutral" on:click={save} disabled={!pendingChanges} />
            </div>
        </div>
    </div>
</Drawer>

<Modal bind:open={openNavigationConfirmationModal} title="Confirm navigation" confirmLabel="Leave page" 
       on:click={confirmNavigation}>
    You changed the score for this variable. Are you sure you want to leave? Any unsaved changes will be lost.
</Modal>

<style>
    h2 {
        @apply text-a-2xl font-semibold mb-4;
    }

    h3 {
        @apply py-2;
        @apply text-a-base;
    }

    ul {
        @apply list-disc pl-4;
        @apply text-a-sm font-normal text-a-gray-500;
    }

    .indicator {
        @apply bg-a-gray-200;
    }
</style>