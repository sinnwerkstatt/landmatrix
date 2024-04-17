<script lang="ts">
    import SidebarTab from "./atomic/SidebarTab.svelte";
    import Section from "./atomic/Section.svelte";
    import SortableList from "./atomic/SortableList.svelte";

    let bookmarked = [
        { id: 1, name: "Philippines – Soy", position: 0 },
        { id: 2, name: "Senegal", position: 1 },
        { id: 3, name: "Queensland – Forest", position: 2 }
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

    <div class="overflow-scroll">
        <Section title="Bookmarked projects" on:edit on:bookmark>
            <SortableList bind:items={bookmarked} on:edit={handleEdit} on:bookmark={handleBookmark} />
        </Section>
        
        <Section title="My projects">
            <SidebarTab id={10} label="South Africa – In negotiation" menu={true} handle={false} on:edit={handleEdit} on:bookmark={handleBookmark} />
            <SidebarTab id={20} label="Albania" menu={true} handle={false} on:edit={handleEdit} on:bookmark={handleBookmark} />
        </Section>
    </div>
</div>