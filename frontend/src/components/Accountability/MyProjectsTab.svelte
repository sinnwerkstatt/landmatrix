<script lang="ts">
    import { myProjects, bookmarkedProjects } from "$lib/accountability/stores"
    import { updateUserBookmarks } from "$lib/accountability/projects"

    import SidebarTab from "./atomic/SidebarTab.svelte"
    import Section from "./atomic/Section.svelte"
    import SortableList from "./atomic/SortableList.svelte"

    function handleEdit(event) {
        const projectId = event.detail.id
        console.log("Edit action: " + projectId)
    }

    function handleBookmark(event) {
        const projectId = event.detail.id
        console.log("Bookmark action: " + projectId)
    }

    async function handleReorder(event) {
        console.log("Update bookmarks order on db");
        try {
            const res = await updateUserBookmarks()
            const json = await res.json()
            console.log(json)
        } catch (error) {
            console.error(error)
        }
    }

</script>

<div class="h-fit flex flex-col overflow-hidden">
    <SidebarTab label="All deals" active={true} />

    <div class="overflow-auto">
        <Section title="Bookmarked projects" on:edit on:bookmark>
            <SortableList bind:items={$bookmarkedProjects} on:edit={handleEdit} on:bookmark={handleBookmark} on:reorder={handleReorder} />
            <!-- <SortableList on:edit={handleEdit} on:bookmark={handleBookmark} on:reorder={handleReorder} /> -->
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