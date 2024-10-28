<script lang="ts">
  // import { filters } from "$lib/accountability/filters.js"
  import { updateFilters } from "$lib/accountability/projects.js"
  // import { deals } from "$lib/accountability/stores.js"

  export let data

  // Update filters if new project selected
  $: updateFilters(data.project)

  // ==========
  // $: {
  //     console.log("=> Project:")
  //     console.log(data.project)
  // }

  // $: {
  //     console.log("=> Filters:")
  //     console.log($filters)
  // }

  // $: console.log($deals)
</script>

<slot />
