<script lang="ts">
    // import { deals } from "$lib/accountability/placeholders"
    import { deals } from "$lib/accountability/stores"

    import TableDeals from "$components/Accountability/TableDeals.svelte"
    import DrawerScoring from "$components/Accountability/DrawerScoring.svelte"

</script>

<div class="h-full overflow-auto">
    <TableDeals deals={$deals} />
</div>

<DrawerScoring />