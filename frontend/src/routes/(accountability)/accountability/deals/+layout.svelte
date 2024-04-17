<script lang="ts">
    import ProjectsSidebar from "$components/Accountability/ProjectsSidebar.svelte"
    import FiltersSidebar from "$components/Accountability/FiltersSidebar.svelte"
    import PageHeading from "$components/Accountability/PageHeading.svelte"
</script>

<div class="flex flex-row flex-nowrap w-full bg-white">
    <ProjectsSidebar />
    <FiltersSidebar />
    <div>
        <PageHeading />
        <slot />
    </div>
</div>