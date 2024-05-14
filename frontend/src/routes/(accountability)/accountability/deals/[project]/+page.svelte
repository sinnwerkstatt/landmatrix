<script lang="ts">
    import { page } from "$app/stores"
    import { dealsHistory } from "$lib/accountability/stores"

    import CardKPI from "$components/Accountability/CardKPI.svelte"
    import Thread from "$components/Accountability/Thread.svelte"

    // If currentProject =/= page.params.project, update project and empty current page and current Deal
    function updateLocalStorage(pathname) {
        if ($page.params.project) {
            dealsHistory.set(pathname)
        }
    }

    $: updateLocalStorage($page.url.pathname)

    const totalDeals = 130
    const toScore = 100
    const waiting = 20
    const validated = 100

    // TODO: Remember to handle differently the "all deals" project with ID = 0

    // TODO: Remember to handle errors when a deal doesn't exist for a project (reset dealsHistory)

</script>

<!-- <p>Project ID: {$page.params.project}</p> -->

<!-- KPI cards -->
<div class="flex flex-col xl:grid xl:grid-cols-3 gap-4">
    <CardKPI label="To score" value="{toScore}/{totalDeals}" color="neutral" icon="check" button="Go to" />
    <CardKPI label="Waiting for review" value="{waiting}/{totalDeals}" color="orange" icon="eye" button="Go to" />
    <CardKPI label="Validated" value="{validated}/{totalDeals}" color="green" icon="check" button="Go to" />
</div>

<!-- Map -->
<div class="h-80 bg-a-gray-100 rounded-lg my-4 grid place-items-center">
    <span class="text-a-gray-400">Map placeholder</span>
</div>

<!-- Activity thread -->
<Thread />