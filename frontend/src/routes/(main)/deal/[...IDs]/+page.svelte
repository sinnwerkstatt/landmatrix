<script lang="ts">
  import { onMount } from "svelte"

  import { goto } from "$app/navigation"
  import { page } from "$app/stores"

  onMount(() => {
    const activeTab = $page.url.hash.split("-")[0] || "#locations"
    const newLoc = activeTab.replace("#", "")

    goto(`${$page.url.pathname}${newLoc}/`, { replaceState: true })
  })
</script>
