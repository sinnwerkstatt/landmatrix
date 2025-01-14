<script lang="ts">
  // import { filters } from "$lib/accountability/filters.js"
  import { updateFilters } from "$lib/accountability/projects.js"

  interface Props {
    // import { deals } from "$lib/accountability/stores.js"
    data: any
    children?: import("svelte").Snippet
  }

  let { data, children }: Props = $props()

  // Update filters if new project selected
  $effect(() => {
    updateFilters(data.project)
  })

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

{@render children?.()}
