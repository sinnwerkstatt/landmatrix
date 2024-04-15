<script lang="ts">
    import SidebarTab from "./atomic/SidebarTab.svelte"
    import Button from "./Button.svelte"
    import IconFilter from "./icons/IconFilter.svelte"
    import Section from "./atomic/Section.svelte"

    const projects = [
        { name: "Albania" },
        { name: "Nikka's project test" },
        { name: "South Africa – in negotiation" },
        { name: "Philippines – Soy" },
        { name: "Queensland – Forest" },
        { name: "Senegal" }
    ]

    // Alphabetically sort projects
    let sortedProjects = projects.sort((a, b) => a.name.localeCompare(b.name))

    // Swap alphabetical sorting each time the button is clicked
    function sortProjects() { sortedProjects = sortedProjects.reverse() }
</script>

<div class="flex flex-col my-2 h-full overflow-hidden">
    <Button label="Filter projects (0)" type="outline" style="neutral" tailwind="self-center">
        <span slot="icon-after"><IconFilter /></span>
    </Button>

    <div class="overflow-scroll">
        <Section title="Results" alwaysOpen={true} sortable="auto" stickyTitle={true} on:sort={sortProjects}>
            {#each sortedProjects as { name }}
                <SidebarTab label={name} menu={true} handle={false} />
            {/each}
        </Section>
    </div>
</div>