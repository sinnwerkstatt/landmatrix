<script lang="ts">
    import { myProjects, bookmarkedProjects } from "$lib/accountability/stores"

    import SidebarTab from "./atomic/SidebarTab.svelte"
    import Section from "./atomic/Section.svelte"
    import SortableList from "./atomic/SortableList.svelte"

    // let bookmarked = [
    //     { id: 1, name: "Philippines – Soy", position: 0 },
    //     { id: 2, name: "Senegal", position: 1 },
    //     { id: 3, name: "Queensland – Forest", position: 2 },
    // ];

    // let myProjects = [
    //     { id: 10, name: "South Africa – In negotiation" },
    //     { id: 20, name: "Albania" },
    // ];

    function handleEdit(event) {
        const projectId = event.detail.id
        console.log("Edit action: " + projectId)
    }

    function handleBookmark(event) {
        const projectId = event.detail.id
        console.log("Bookmark action: " + projectId)
    }

    function handleReorder(event) {
        const reordered = event.detail.reordered
        const old_order = $bookmarkedProjects.map(e => e.id).toString()
        const new_order = reordered.map(e => e.id).toString()

        if (old_order != new_order) {
            console.log("Update UserInfo bookmarks")
        }

        bookmarkedProjects.set(reordered)
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