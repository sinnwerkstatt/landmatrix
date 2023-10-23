<script lang="ts">
  import { onMount } from "svelte"

  import { fetchFieldDefinitions } from "$lib/stores"

  onMount(() => {
    fetchFieldDefinitions(fetch)
  })
</script>

<slot />
