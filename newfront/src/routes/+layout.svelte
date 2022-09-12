<script lang="ts">
  import { SvelteToast } from "@zerodevx/svelte-toast"
  import { onMount } from "svelte"

  import { getAllUsers } from "$lib/stores"
  import { UserLevel } from "$lib/types/user"

  import Footer from "$components/Footer.svelte"
  import Messages from "$components/Messages.svelte"
  import Navbar from "$components/Navbar.svelte"
  import NavigationLoader from "$components/NavigationLoader.svelte"

  import "../app.css"
  import type { LayoutData } from "./$types"

  const toastOptions = {
    reversed: true,
    classes: ["toast"],
    duration: 8000,
    pausable: true,
  }

  export let data: LayoutData
  onMount(async () => {
    if (data.user?.level >= UserLevel.EDITOR) {
      await getAllUsers(data.urqlClient)
    }
  })
</script>

<Messages />
<NavigationLoader />
<Navbar />
<div class="h-[calc(100vh-58px-32px)] overflow-x-auto">
  <slot />
</div>
<Footer />
<SvelteToast options={toastOptions} />
