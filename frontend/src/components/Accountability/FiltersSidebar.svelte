<script lang="ts">
    import { openedFilterBar } from "$lib/accountability/stores"

    import Sidebar from "./atomic/Sidebar.svelte"
    import Filters from "./atomic/Filters.svelte"
    import Button from "./Button.svelte"
    import IconCollapse from "$components/Accountability/icons/IconCollapse.svelte"
    import Modal from "./Modal.svelte"
    import Input from "./atomic/Input.svelte"
    import Avatar from "./atomic/Avatar.svelte"
    import Divider from "./atomic/Divider.svelte"
    import Card from "./atomic/Card.svelte"
    import CardTable from "./atomic/CardTable.svelte"

    let openSaveModal = false

    let form = {
        name: undefined,
        description: undefined,
        users: ["10", "11"],
    }

    const owner = { value: "8", label: "Marie", initials: "MG" }

    const users = [
        { value: "10", label: "Nikka", initials: "NR" },
        { value: "11", label: "Angela", initials: "AH" },
        { value: "12", label: "Jérémy", initials: "JB" },
        { value: "13", label: "Mohamadou", initials: "MD" }
    ]

    const infos = [
        { label: "Created at:", value: undefined },
        { label: "Created by:", value: undefined },
        { label: "Last modification:", value: undefined },
        { label: "Last modification by:", value: undefined }
    ]

    function clearFilters() {
        console.log("Clear all");
    }
 
</script>

{#if $openedFilterBar}
    <Sidebar>
        <div class="flex items-center flex-nowrap justify-between">
            <span class="text-a-sm font-semibold text-a-gray-500">Filters</span>
            <button on:click={() => { $openedFilterBar = false }}>
                <IconCollapse />
            </button>
        </div>

        <Filters />

        <div class="flex justify-center gap-2">
            <Button label="Save new project" size="sm" style="neutral" on:click={() => openSaveModal = true} />
            <Button label="Clear all" size="sm" style="neutral" type="outline" />
        </div>
    </Sidebar>
{/if}

<Modal bind:open={openSaveModal} title="Create new project" large={true}>
    <div class="grid grid-cols-2 w-full divide-x">

        <div class="pr-4 lg:pr-14">
            <h2 class="text-a-sm font-semibold text-a-gray-500">Informations</h2>
            <Input type="text" label="Name" placeholder="Add name" bind:value={form.name} />
            <Input type="textarea" label="Description" placeholder="Add description" bind:value={form.description}
                   maxlength={280} />
            <Input type="multiselect" label="Users (who can edit)" placeholder="Search for user"
                   choices={users} bind:value={form.users} badgeType="avatar" />
            <Avatar initials={owner.initials} label="{owner.label} (owner)" extraClass="mt-1" padding={true} />
            <Divider />
            <Card>
                <CardTable data={infos} />
            </Card>
        </div>

        <div class="pl-4 lg:pl-14">
            <h2 class="text-a-sm font-semibold text-a-gray-500">Filters</h2>
            <Filters />
        </div>

    </div>
</Modal>
