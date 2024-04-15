<script lang="ts">
    import ProjectsSidebar from "$components/Accountability/ProjectsSidebar.svelte"
</script>

<div class="flex flex-row flex-nowrap w-full bg-white">
    <ProjectsSidebar />
    <slot />
</div>