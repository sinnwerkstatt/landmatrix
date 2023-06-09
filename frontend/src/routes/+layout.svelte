<script lang="ts">
  import * as Sentry from "@sentry/svelte"
  import { BrowserTracing } from "@sentry/tracing"
  import type { Client } from "@urql/core"
  import { SvelteToast } from "@zerodevx/svelte-toast"
  import { onMount } from "svelte"

  import { getAllUsers, isDarkMode } from "$lib/stores"
  import type { User } from "$lib/types/user"
  import { UserRole } from "$lib/types/user"

  import Footer from "$components/Footer.svelte"
  import LightboxImage from "$components/LightboxImage.svelte"
  import Matomo from "$components/Matomo.svelte"
  import Messages from "$components/Messages.svelte"
  import Navbar from "$components/Navbar.svelte"
  import NavigationLoader from "$components/NavigationLoader.svelte"

  import "../app.css"

  // import type { LayoutData } from "./$types"
  // export let data: LayoutData
  export let data: { user: User | undefined; urqlClient: Client } = {}

  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN,
    environment: "svelte frontend",
    integrations: [new BrowserTracing()],
    tracesSampleRate: 1.0,
    // initialScope: { tags: { mode: "svelte frontend" } },
  })

  if (data.user)
    Sentry.configureScope(scope => scope.setUser({ id: (data.user as User).username }))

  onMount(async () => {
    if (data.user?.role >= UserRole.EDITOR) {
      await getAllUsers(data.urqlClient)
    }
    $isDarkMode =
      window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches
    window
      .matchMedia("(prefers-color-scheme: dark)")
      .addEventListener("change", event => {
        $isDarkMode = event.matches
      })
  })
</script>

<Messages />
<NavigationLoader />
<Navbar />
<div class="h-[calc(100vh-58px-32px)] overflow-x-auto">
  <slot />
</div>
<Footer />

<Matomo />

<SvelteToast
  options={{ reversed: true, classes: ["toast"], duration: 8000, pausable: true }}
/>

<LightboxImage />
