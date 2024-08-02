<script lang="ts">
    import { usersToUserChoices } from "$lib/accountability/helpers"
    import { openedFilterBar, users } from "$lib/accountability/stores"
    import { createProject } from "$lib/accountability/projects"
    import { filters } from "$lib/accountability/filters"

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
    let disableSaveModal = false
    
    let form = {
        name: undefined,
        description: undefined,
        users: ["153"],
    }
    let formErrors = {}
    $: formStatus = {
        name: formErrors.name ? "invalid" : "neutral",
        description: formErrors.description ? "invalid" : "neutral",
    }

    const owner = { value: 585, label: "Marie GRADELER", initials: "MG" }

    const userChoices = usersToUserChoices($users).filter(e => e.value != owner.value)

    usersToUserChoices($users)

    const infos = [
        { label: "Created at:", value: undefined },
        { label: "Created by:", value: undefined },
        { label: "Last modification:", value: undefined },
        { label: "Last modification by:", value: undefined }
    ]

    function resetFormErrors(form) {
        formErrors = {}
    }

    async function save() {
        formErrors = {}
        disableSaveModal = true

        const res = await createProject(form, $filters)
        if (res.ok) {
            formErrors = {}
            disableSaveModal = false
            openSaveModal = false
        } else {
            formErrors = await res.json()
            disableSaveModal = false
        }
    }

    $: resetFormErrors(form)
 
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
            <Button label="Clear all" size="sm" style="neutral" type="outline" on:click={() => $filters = $filters.empty()} />
        </div>
    </Sidebar>
{/if}

<Modal bind:open={openSaveModal} title="Create new project" large={true} on:click={save} bind:disabled={disableSaveModal}>
    <div class="grid grid-cols-2 w-full divide-x">

        <div class="pr-4 lg:pr-14">
            <h2 class="text-a-sm font-semibold text-a-gray-500">Informations</h2>
            <Input type="text" label="Name" placeholder="Add name" bind:value={form.name} status={formStatus.name} message={formErrors.name} />
            <Input type="textarea" label="Description" placeholder="Add description" bind:value={form.description}
                   maxlength={280} status={formStatus.description} message={formErrors.description} />
            <Input type="multiselect" label="Users (who can edit)" placeholder="Search for user"
                   choices={userChoices} bind:value={form.users} badgeType="avatar" />
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