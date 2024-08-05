<script lang="ts">
    import { myProjects, bookmarkedProjects, addUserBookmark, removeUserBookmark, updateUserBookmarks } from "$lib/accountability/projects"

    import SidebarTab from "./atomic/SidebarTab.svelte"
    import Section from "./atomic/Section.svelte"
    import SortableList from "./atomic/SortableList.svelte"

    function handleEdit(event) {
        const projectId = event.detail.id
        console.log("Edit action: " + projectId)
    }

    async function handleBookmark(event) {
        const action = event.detail.action
        const projectId = event.detail.id
        console.log(`Action ${action} on project ${projectId}`)
        if (action == "add") {
            try {
                await addUserBookmark(projectId)
            } catch (error) {
                console.error(error)
            }
        } else if (action == "remove") {
            try {
                await removeUserBookmark(projectId)
            } catch (error) {
                console.error(error)
            }
        }
    }

    async function handleReorder(event) {
        try {
            await updateUserBookmarks()
        } catch (error) {
            console.error(error)
        }
    }

    $: console.log($bookmarkedProjects)

</script>

<div class="h-fit flex flex-col overflow-hidden">
    <SidebarTab label="All deals" active={true} />

    <div class="overflow-auto">
        <Section title="Bookmarked projects" on:edit on:bookmark>
            <SortableList bind:items={$bookmarkedProjects} on:edit={handleEdit} on:bookmark={handleBookmark} on:reorder={handleReorder} />
        </Section>
        
        <Section title="My projects">
            {#each $myProjects as { id, name }, i }
                {@const menuPosition = i+1 == $myProjects.length ? "top" : "bottom" }
                <SidebarTab {id} label={name} menu={true} handle={false} on:edit={handleEdit} on:bookmark={handleBookmark}
                            {menuPosition} />
            {/each}
        </Section>
    </div>
</div>