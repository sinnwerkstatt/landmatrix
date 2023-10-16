<script lang="ts">
  import { fieldDefinitions } from "$lib/stores"
  import { onMount } from "svelte"

  async function fetchFieldDefinitions() {
    if ($fieldDefinitions.length === 0) {
      const res = await fetch("/api/field_definitions/")
      fieldDefinitions.set(await res.json())
    }
  }

  onMount(() => {
    fetchFieldDefinitions()
  })
</script>

<slot />
