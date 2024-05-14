<script lang="ts">
    import { page } from "$app/stores"
    import { dealsHistory } from "$lib/accountability/stores"

    import CardKPI from "$components/Accountability/CardKPI.svelte"

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

<!-- <p>Project ID: {$page.params.project}</p> -->

<!-- KPI cards -->
<div>
    <CardKPI />
    <CardKPI />
    <CardKPI />
</div>

<!-- Map -->

<!-- Activity thread -->