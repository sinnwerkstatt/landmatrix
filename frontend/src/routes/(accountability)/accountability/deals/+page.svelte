<script lang="ts">
    import { browser } from "$app/environment"
    import { goto } from "$app/navigation"
    import { dealsHistory } from "$lib/accountability/stores"

    // Go to last Deals page opened
    if (browser) {
        goto($dealsHistory)
    }

</script>

<div>
    Placeholder
</div>