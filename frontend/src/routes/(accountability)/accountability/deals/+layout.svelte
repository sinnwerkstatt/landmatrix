<script lang="ts">
    import ProjectsSidebar from "$components/Accountability/ProjectsSidebar.svelte"
    import FiltersSidebar from "$components/Accountability/FiltersSidebar.svelte"
    import PageHeading from "$components/Accountability/PageHeading.svelte"
    import DealsMenu from "$components/Accountability/DealsMenu.svelte"
</script>

<div class="flex flex-row flex-nowrap w-full bg-white">
    <ProjectsSidebar />
    <FiltersSidebar />
    <div class="w-full px-4">
        <PageHeading />
        <div class="flex flex-wrap justify-between gap-6 mb-6">
            <DealsMenu />
            <span class="text-a-gray-400">Users placeholder</span>
        </div>
        <slot />
    </div>
</div>