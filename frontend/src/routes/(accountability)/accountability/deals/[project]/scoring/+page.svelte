<script lang="ts">
    import { deals } from "$lib/accountability/placeholders"

    import TableDeals from "$components/Accountability/TableDeals.svelte"
</script>

<div class="h-full overflow-auto">
    <TableDeals {deals} />
</div>