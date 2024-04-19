<script lang="ts">
  import * as Sentry from "@sentry/svelte"
  import { BrowserTracing } from "@sentry/tracing"
  import { SvelteToast } from "@zerodevx/svelte-toast"
  import { env } from "$env/dynamic/public"

  import { afterNavigate } from "$app/navigation"

  import { contentRootElement } from "$lib/stores/basics"
  import type { User } from "$lib/types/user"

  import LightboxImage from "$components/LightboxImage.svelte"
  import Messages from "$components/Messages.svelte"
  import Navbar from "$components/Navbar/Navbar.svelte"
  import NavigationLoader from "$components/NavigationLoader.svelte"

  import "$lib/css/app.css"

  import { Matomo } from "@sinnwerkstatt/sveltekit-matomo"

  export let data

  if (env.PUBLIC_SENTRY_DSN) {
    Sentry.init({
      dsn: env.PUBLIC_SENTRY_DSN,
      environment: "svelte frontend",
      integrations: [new BrowserTracing()],
      tracesSampleRate: 1.0,
      // initialScope: { tags: { mode: "svelte frontend" } },
    })

    if (data.user) {
      const scope = Sentry.getCurrentScope()
      scope.setUser({ id: (data.user as User).username })
    }
  }

  afterNavigate(() => $contentRootElement?.scrollTo(0, 0))
</script>

<Messages />
<NavigationLoader />

<Navbar />

<div
  bind:this={$contentRootElement}
  class="overflow-x-auto transition-colors dark:bg-gray-900"
>
  <slot />
</div>

{#if env.PUBLIC_MATOMO_URL && env.PUBLIC_MATOMO_SITE_ID}
  <Matomo
    url={env.PUBLIC_MATOMO_URL}
    siteId={+env.PUBLIC_MATOMO_SITE_ID}
    linkTracking={false}
  />
{/if}

<SvelteToast
  options={{ reversed: true, classes: ["toast"], duration: 8000, pausable: true }}
/>

<LightboxImage />
