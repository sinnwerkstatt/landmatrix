<script lang="ts">
    import { deals } from "$lib/accountability/placeholders"

    import TableDeals from "$components/Accountability/TableDeals.svelte"
    import DrawerScoring from "$components/Accountability/DrawerScoring.svelte"

    let openDrawer = true

</script>

<div class="h-full overflow-auto">
    <TableDeals {deals} />
</div>

<button on:click={() => openDrawer = true}>O</button>

<DrawerScoring bind:open={openDrawer} />