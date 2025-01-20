<script lang="ts">
  import * as Sentry from "@sentry/sveltekit"
  import { SvelteToast } from "@zerodevx/svelte-toast"
  import { env } from "$env/dynamic/public"

  import { page } from "$app/state"

  import LightboxImage from "$components/LightboxImage.svelte"
  import Messages from "$components/Messages.svelte"
  import Navbar from "$components/Navbar/Navbar.svelte"
  import NavigationLoader from "$components/NavigationLoader.svelte"

  import "$lib/css/app.css"

  import { Matomo } from "@sinnwerkstatt/sveltekit-matomo"

  import type { User } from "$lib/types/data"

  let { data, children } = $props()

  if (env.PUBLIC_SENTRY_DSN) {
    if (data.user) {
      const scope = Sentry.getCurrentScope()
      scope.setUser({ id: (data.user as User).username })
    }
  }
</script>

{#if page.url.pathname.split("/")[1] !== "accountability"}
  <div id="main-content" class="grid h-screen">
    <div>
      <Messages />
      <NavigationLoader />
      <Navbar />
    </div>

    <div id="content" class="h-full overflow-y-auto transition-colors dark:bg-gray-900">
      {@render children?.()}
    </div>
  </div>
{:else}
  <!-- Reset layout for /accountability -->
  {@render children?.()}
{/if}

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

<style>
  #main-content {
    grid-template-rows: auto 1fr;
  }
</style>
