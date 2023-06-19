<script lang="ts">
  import * as Sentry from "@sentry/svelte"
  import { BrowserTracing } from "@sentry/tracing"
  import type { Client } from "@urql/core"
  import { SvelteToast } from "@zerodevx/svelte-toast"
  import { onMount } from "svelte"

  import { afterNavigate } from "$app/navigation"

  import { getAllUsers } from "$lib/stores"
  import type { User } from "$lib/types/user"
  import { UserRole } from "$lib/types/user"

  import Footer from "$components/Footer.svelte"
  import LightboxImage from "$components/LightboxImage.svelte"
  import Matomo from "$components/Matomo.svelte"
  import Messages from "$components/Messages.svelte"
  import Navbar from "$components/Navbar/Navbar.svelte"
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
  })

  let contentRoot: Element
  afterNavigate(() => contentRoot.scrollTo(0, 0))
</script>

<Messages />
<NavigationLoader />

<div class="h-[62px]">
  <Navbar />
</div>

<div bind:this={contentRoot} class="h-[calc(100vh-62px-32px)] overflow-x-auto">
  <slot />
</div>

<div class="h-[32px]">
  <Footer />
</div>

<Matomo />

<SvelteToast
  options={{ reversed: true, classes: ["toast"], duration: 8000, pausable: true }}
/>

<LightboxImage />
