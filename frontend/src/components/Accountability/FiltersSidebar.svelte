<script lang="ts">
    import { usersToUserChoices } from "$lib/accountability/helpers"
    import { openedFilterBar, users, me } from "$lib/accountability/stores"
    import { createProject, updateProject, refreshProjects } from "$lib/accountability/projects"
    import { filters, FilterValues } from "$lib/accountability/filters"
    import { page } from "$app/stores"

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

    let showSaveModal = false
    let disableSaveModal = false
    let action:"create"|"update" = "create"
    let modalTitle = ""

    let form = {
        name: undefined,
        description: undefined,
        editors: [],
    }
    let formErrors = {}
    $: formStatus = {
        name: formErrors.name ? "invalid" : "neutral",
        description: formErrors.description ? "invalid" : "neutral",
    }

    $: userChoices = usersToUserChoices($users).filter(e => e.value != $page.data.user.id)

    usersToUserChoices($users)

    let infos = [
        { label: "Created at:", value: undefined },
        { label: "Created by:", value: undefined },
        { label: "Last modification:", value: undefined },
        { label: "Last modification by:", value: undefined }
    ]

    function resetFormErrors(form) {
        formErrors = {}
    }

    async function save() {
        console.log("===" + action + "===")
        formErrors = {}
        disableSaveModal = true

        if (action == "create") {
            const res = await createProject(form, $filters)
            if (res.ok) {
                formErrors = {}
                showSaveModal = false
                try {
                    await refreshProjects()
                } catch (error) {
                    console.error(error)
                }
            } else {
                formErrors = await res.json()
            }

        } else if (action == "update") {
            const res = await updateProject($page.data.project.id, form, $filters)
            if (res.ok) {
                formErrors = {}
                showSaveModal = false
                try {
                    await refreshProjects()
                } catch (error) {
                    console.error(error)
                }
            } else {
                formErrors = await res.json()
            }
        }

        disableSaveModal = false

        // TODO: Show success message or error messages in toast        

    }

    $: resetFormErrors(form)

    function resetFilters() {
        const baseFilters = new FilterValues($page.data.project.filters)
        $filters = baseFilters
    }

    function openSaveModal(eventAction:"create"|"update") {
        action = eventAction
        if (action == "create") {
            modalTitle = "Create new project"
            form = { name: undefined, description: undefined, editors: [] }
            infos = [
                { label: "Created at:", value: undefined },
                { label: "Created by:", value: undefined },
                { label: "Last modification:", value: undefined },
                { label: "Last modification by:", value: undefined }
            ]
            showSaveModal = true

        } else if (action == "update") {
            modalTitle = "Update existing project"
            const project = $page.data.project
            form = { name: project.name, description: project.description, editors: project.editors }
            infos = [
                { label: "Created at:", value: new Date(project.created_at).toISOString().substring(0, 10) },
                { label: "Created by:", value: $users.filter(u => u.id == project.owner)[0].name },
                { label: "Last modification:", value: project.modified_at ? new Date(project.modified_at).toISOString().substring(0, 10) : undefined },
                { label: "Last modification by:", value: project.modified_by ?? undefined }
            ]
            showSaveModal = true
        }
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

        <div class="px-2 flex justify-between gap-2 flex-wrap">
            <Button label="Save new project" size="sm" style="neutral" on:click={() => openSaveModal("create")} />
            {#if $page.data.project.owner == $me.id}
                <Button label="Update" size="sm" style="neutral" on:click={() => openSaveModal("update")} />
            {/if}
            <Button label="Reset filters" size="sm" style="neutral" type="outline" on:click={resetFilters} />
            <Button label="Clear filters" size="sm" style="neutral" type="outline" on:click={() => $filters = $filters.empty()} />
        </div>
    </Sidebar>
{/if}

<Modal bind:open={showSaveModal} title={modalTitle} large={true} on:click={save} bind:disabled={disableSaveModal}>
    <div class="grid grid-cols-2 w-full divide-x">

        <div class="pr-4 lg:pr-14">
            <h2 class="text-a-sm font-semibold text-a-gray-500">Informations</h2>
            <Input type="text" label="Name" placeholder="Add name" bind:value={form.name} status={formStatus.name} message={formErrors.name} />
            <Input type="textarea" label="Description" placeholder="Add description" bind:value={form.description}
                   maxlength={280} status={formStatus.description} message={formErrors.description} />
            <Input type="multiselect" label="Users (who can edit)" placeholder="Search for user"
                   choices={userChoices} bind:value={form.editors} badgeType="avatar" />
            <Avatar initials={$me.initials} label="{$me.label} (owner)" extraClass="mt-1" padding={true} />
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
