<script lang="ts">
    import { users } from "$lib/accountability/placeholders"
    import { usersToUserChoices } from "$lib/accountability/helpers"
    import { tableSelection } from "$lib/accountability/stores"

    import Table from "./atomic/Table.svelte"
    import TableRow from "./atomic/TableRow.svelte"
    import TableCell from "./atomic/TableCell.svelte"
    import TableDealsRow from "./atomic/TableDealsRow.svelte"

    import Input from "./atomic/Input.svelte"
    import Checkbox from "./atomic/Checkbox.svelte"

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
    let statusFilter = ""
    let assigneeFilter = ""

    let searchResult = deals

    const statuses = [
        { value: "no_score", label: "To score" },
        { value: "pending", label: "Waiting for review" },
        { value: "validated", label: "Validated" },
        { value: "no_data", label: "No data" }
    ]

    function getAssignedUsers(deals, users) {
        const allAssignees = deals.map(deal => deal.variables).flat().map(e => e.assignee).filter(Boolean).map(user => user.id)
        const uniqueAssignees = [...new Set(allAssignees)]
        const assignedUsers = users.filter(user => uniqueAssignees.includes(user.id))
        const result = usersToUserChoices(assignedUsers)
        return result
    }

    $: userChoices = getAssignedUsers(deals, users)

    function search(searchWord, data) {
        if (searchWord == "") {
            return data

        } else {
            const via_id = data.filter(e => (e.id).toString().includes(searchWord))
            const via_country = data.filter(e => e.country.name.toLowerCase().includes(searchWord.toLowerCase()))

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

    function assignedToUser(deals, user_id) {
        let result = []
        deals.forEach(deal => {
            const assignees = deal.variables.map(variable => variable?.assignee?.id).filter(Boolean)
            if (assignees.includes(Number(user_id))) result.push(deal)
        })
        return result
    }

    function filterDeals(searchWord, statusFilter, assigneeFilter) {
        let data = deals
        if (statusFilter) {
            data = data.filter(e => e.status == statusFilter)
        }
        if (assigneeFilter) {
            data = assignedToUser(data, assigneeFilter)
        }
        let result = search(searchWord, data)
        return result
    }

    $: searchResult = filterDeals(searchWord, statusFilter, assigneeFilter)

    function createDealSelectObject(bool:boolean) {
        let res = {}
        deals.forEach(deal => {
            let vars = {}
            deal.variables.forEach(variable => {
                vars[variable.id] = bool
            })
            const obj = { deal: deal.id, variables: vars }
            res[deal.id] = obj
        })

        return res
    }

    // Select deals
    function selectAllDeals(event) {
        const checked = event.detail.checked

        if (checked) {
            tableSelection.set(createDealSelectObject(true))
        } else {
            tableSelection.set(createDealSelectObject(false))
        }
    }

</script>

<Table bind:data={searchResult} bind:pageContent={pageContent} rowHeight=57 >

    <!-- Table filters -->
    <div slot="filters" class="flex flex-wrap gap-2">
        <div><Input type="text" icon="search" placeholder="Search for a deal (ID, Country)" bind:value={searchWord} /></div>
        <div class="w-52">
            <Input type="select" placeholder="Deal status" choices={statuses} search={false} bind:value={statusFilter}
                   extraClass="!w-52" style="white" />
        </div>
        <div class="w-40">
            <Input type="select" placeholder="Assignee" choices={userChoices} search={false} bind:value={assigneeFilter}
                   extraClass="!w-40" style="white" />
        </div>
    </div>

    <!-- Table header -->
    <svelte:fragment slot="header">
        <TableRow {gridColsTemplate} >
            <TableCell style="heading" >
                <div class="w-fit">
                    <Checkbox paddingX=0 paddingY=0 on:changed={selectAllDeals} />
                </div>
            </TableCell>

            {#each columns as column (column.value) }
                <TableCell style="heading" >{column.label.toUpperCase()}</TableCell>
            {/each}
        </TableRow>
    </svelte:fragment>

    <!-- Table body and footer -->
    <svelte:fragment slot="body">
        {#each pageContent as deal (deal.id)}
            <TableDealsRow {gridColsTemplate} {columns} {deal} />
        {/each}
    </svelte:fragment>

</Table>