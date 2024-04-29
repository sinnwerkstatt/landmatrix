<script lang="ts">
    import SidebarTab from "./atomic/SidebarTab.svelte";
    import Section from "./atomic/Section.svelte";
    import SortableList from "./atomic/SortableList.svelte";

    let bookmarked = [
        { id: 1, name: "Philippines – Soy", position: 0 },
        { id: 2, name: "Senegal", position: 1 },
        { id: 3, name: "Queensland – Forest", position: 2 }
    ];

    let myProjects = [
        { id: 10, name: "South Africa – In negotiation" },
        { id: 20, name: "Albania" }
    ];

    // $: console.log(bookmarked)

    function handleEdit(event) {
        const projectId = event.detail.id
        console.log("Edit action: " + projectId)
    }

    function handleBookmark(event) {
        const projectId = event.detail.id
        console.log("Bookmark action: " + projectId)
    }

</script>

<div class="h-fit flex flex-col overflow-hidden">
    <SidebarTab label="All deals" active={true} />

    <div class="overflow-auto">
        <Section title="Bookmarked projects" on:edit on:bookmark>
            <SortableList bind:items={bookmarked} on:edit={handleEdit} on:bookmark={handleBookmark} />
        </Section>
        
        <Section title="My projects">
            {#each myProjects as { id, name }, i }
                {@const menuPosition = i+1 == myProjects.length ? "top" : "bottom" }
                <SidebarTab {id} label={name} menu={true} handle={false} on:edit={handleEdit} on:bookmark={handleBookmark}
                            {menuPosition} />
            {/each}
        </Section>
    </div>
</div>