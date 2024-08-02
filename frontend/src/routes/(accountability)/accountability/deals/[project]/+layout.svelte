<script lang="ts">
    import { updateFilters } from '$lib/accountability/projects.js'
    import { deals } from '$lib/accountability/stores.js'

    export let data

    // Update filters if new project selected
    $: updateFilters(data.project)

    $: console.log($deals)
    
    // $: console.log(data.project)
</script>

<slot />