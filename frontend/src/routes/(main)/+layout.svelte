<script lang="ts">
  import { fetchFieldDefinitions } from "$lib/stores"
  import { onMount } from "svelte"

  onMount(() => {
    fetchFieldDefinitions(fetch)
  })
</script>

<slot />
