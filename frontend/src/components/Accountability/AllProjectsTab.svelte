<script lang="ts">
    import SidebarTab from "./atomic/SidebarTab.svelte"
    import Button from "./Button.svelte"
    import IconFilter from "./icons/IconFilter.svelte"
    import Section from "./atomic/Section.svelte"
    import Pagination from "./atomic/Pagination.svelte"

    const projects = [
        { id: 11, name: "Albania" },
        { id: 12, name: "Nikka's project test" },
        { id: 13, name: "South Africa – in negotiation" },
        { id: 14, name: "Philippines – Soy" },
        { id: 15, name: "Queensland – Forest" },
        { id: 16, name: "Senegal" },
        { id: 17, name: "Some" },
        { id: 18, name: "Additional" },
        { id: 19, name: "Projects" },
        { id: 20, name: "For" },
        { id: 21, name: "Testing" },
        { id: 22, name: "Pagination" },
        { id: 23, name: "Components" }
    ]

    // Alphabetically sort projects
    let sortedProjects = projects.sort((a, b) => a.name.localeCompare(b.name))

    // Bind page content from Pagination
    let pageContent = [];

    // Swap alphabetical sorting each time the button is clicked
    function sortProjects() { sortedProjects = sortedProjects.reverse() }

    // Menu
    function handleEdit(event) {
        const projectId = event.detail.id
        console.log("Edit action: " + projectId)
    }

    function handleBookmark(event) {
        const projectId = event.detail.id
        console.log("Bookmark action: " + projectId)
    }
</script>

<div class="flex flex-col my-2 h-full overflow-hidden">
    <Button label="Filter projects (0)" type="outline" style="neutral" tailwind="self-center">
        <span slot="icon-after"><IconFilter /></span>
    </Button>

    <div class="overflow-scroll h-full">
        <Section title="Results" alwaysOpen={true} sortable="auto" stickyTitle={true} on:sort={sortProjects}>
            <Pagination bind:dataset={sortedProjects} bind:pageContent={pageContent} rowHeight="56">
                {#each pageContent as { id, name }}
                    <SidebarTab {id} label={name} menu={true} handle={false} on:edit={handleEdit} on:bookmark={handleBookmark} />
                {/each}
            </Pagination>
        </Section>
    </div>
</div>