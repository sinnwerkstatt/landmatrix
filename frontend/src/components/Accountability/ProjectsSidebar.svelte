<script lang="ts">
    import Sidebar from "./atomic/Sidebar.svelte"
    import Tabs from "./atomic/Tabs.svelte"

    import MyProjectsTab from "./MyProjectsTab.svelte"
    import AllProjectsTab from "./AllProjectsTab.svelte"

    let tabItems = [
        { label: "My projects", value: 1, component: MyProjectsTab},
        { label: "All projects", value: 2, component: AllProjectsTab}
    ]
</script>

<Sidebar>
    <Tabs items={tabItems} />
</Sidebar>