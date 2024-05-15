<script lang="ts">
    import { page } from "$app/stores"

    function getCurrentTab(path) {
        if (path.includes("scoring")) return "scoring"
        if (path.includes("results")) return "results"
        return "overview"
    }

    function writeHref(project, path) {
        let href = `/accountability/deals/${project}/`
        if (path) href += `${path}/`
        return href
    }

    $: currentTab = getCurrentTab($page.url.pathname)

    $: hrefOverview = writeHref($page.params.project, "")
    $: hrefScoring = writeHref($page.params.project, "scoring")
    $: hrefResults = writeHref($page.params.project, "results")
    
</script>

<div class="flex">
    <ul class="flex justify-center gap-1">
        <li class="{ currentTab == 'overview' ? 'active' : '' }">
            <a href={hrefOverview} >Overview</a>
        </li>
        <li class="{ currentTab == 'scoring' ? 'active' : '' }">
            <a href={hrefScoring} >Scoring</a>
        </li>
        <li class="{ currentTab == 'results' ? 'active' : '' }">
            <a href={hrefResults} >Results</a>
        </li>
    </ul>
</div>

<style>
    /* Style matches Tabs.svelte */
    a {
        @apply w-fit;
        @apply px-[0.63rem] py-[0.44rem];
        @apply text-a-sm text-a-gray-400;
        @apply border border-a-gray-200 rounded-lg;
        @apply bg-white;
    }
    a:hover {
        @apply cursor-pointer;
        @apply text-a-gray-900 bg-a-gray-200;
    }
    li.active > a {
        @apply text-white bg-a-gray-900 border-a-gray-900;
    }
</style>