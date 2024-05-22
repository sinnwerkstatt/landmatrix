<script lang="ts">
    import { page } from "$app/stores"
    import { dealsHistory } from "$lib/accountability/stores"

    import ProjectsSidebar from "$components/Accountability/ProjectsSidebar.svelte"
    import FiltersSidebar from "$components/Accountability/FiltersSidebar.svelte"
    import PageHeading from "$components/Accountability/PageHeading.svelte"
    import DealsMenu from "$components/Accountability/DealsMenu.svelte"
    import Avatar from "$components/Accountability/atomic/Avatar.svelte"

    // If currentProject =/= page.params.project, update project and empty current page and current Deal
    function updateLocalStorage(pathname) {
        if ($page.params.project) {
            dealsHistory.set(pathname)
        }
    }

    $: updateLocalStorage($page.url.pathname)

    // TODO: Remember to handle differently the "all deals" project with ID = 0

    // TODO: Remember to handle errors when a deal doesn't exist for a project (reset dealsHistory)

</script>

<div class="h-screen w-full flex flex-row flex-nowrap bg-a-gray-50">
    <ProjectsSidebar />
    <FiltersSidebar />
    <div class="h-screen w-full px-4 flex flex-col">
        <PageHeading />
        <div class="flex flex-wrap justify-between gap-6 mb-6">
            <DealsMenu />
            <span class="text-a-gray-400">Users placeholder</span>
            <!-- <Avatar /> -->
        </div>
        <div class="pb-10 h-full overflow-auto">
            <slot />
        </div>
    </div>
</div>