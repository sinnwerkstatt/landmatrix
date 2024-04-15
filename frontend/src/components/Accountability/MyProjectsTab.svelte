<script lang="ts">
    import SidebarTab from "./atomic/SidebarTab.svelte";
    import Section from "./atomic/Section.svelte";
    import SortableList from "./atomic/SortableList.svelte";

    let bookmarked = [
        { id: 1, name: "Philippines – Soy", position: 0 },
        { id: 2, name: "Senegal", position: 1 },
        { id: 3, name: "Queensland – Forest", position: 2 }
    ];

</script>

<div class="h-full flex flex-col overflow-hidden">
    <SidebarTab label="All deals" active={true} />

    <div class="overflow-scroll">
        <Section title="Bookmarked projects">
            <SortableList bind:items={bookmarked} />
        </Section>
        
        <Section title="My projects">
            <SidebarTab label="South Africa – In negotiation" menu={true} handle={false} />
            <SidebarTab label="Albania" menu={true} handle={false} />
        </Section>
    </div>
</div>