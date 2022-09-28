<script lang="ts">
  import * as Sentry from "@sentry/svelte"
  import { BrowserTracing } from "@sentry/tracing"
  import { SvelteToast } from "@zerodevx/svelte-toast"
  import { onMount } from "svelte"

  import { getAllUsers } from "$lib/stores"
  import { UserRole } from "$lib/types/user"

  import Footer from "$components/Footer.svelte"
  import Messages from "$components/Messages.svelte"
  import Navbar from "$components/Navbar.svelte"
  import NavigationLoader from "$components/NavigationLoader.svelte"

  import "../app.css"
  import type { LayoutData } from "./$types"

  export let data: LayoutData

  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN,
    environment: "svelte frontend",
    integrations: [new BrowserTracing()],
    tracesSampleRate: 1.0,
    // initialScope: { tags: { mode: "svelte frontend" } },
  })

  if (data.user)
    Sentry.configureScope(scope => scope.setUser({ id: data.user.username }))

  onMount(async () => {
    if (data.user?.role >= UserRole.EDITOR) {
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

<SvelteToast
  options={{ reversed: true, classes: ["toast"], duration: 8000, pausable: true }}
/>
