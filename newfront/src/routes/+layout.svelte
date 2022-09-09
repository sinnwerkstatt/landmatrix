<script lang="ts">
  import { SvelteToast } from "@zerodevx/svelte-toast"

  import Footer from "$components/Footer.svelte"
  import Messages from "$components/Messages.svelte"
  import Navbar from "$components/Navbar.svelte"
  import NavigationLoader from "$components/NavigationLoader.svelte"

  import "../app.css"

  const toastOptions = {
    reversed: true,
    classes: ["toast"],
    duration: 8000,
    pausable: true,
  }
</script>

<Messages />
<NavigationLoader />
<Navbar />
<div class="h-[calc(100vh-58px-32px)] overflow-x-auto">
  <slot />
</div>
<Footer />
<SvelteToast options={toastOptions} />
