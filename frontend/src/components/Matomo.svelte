<script lang="ts">
  import { onMount } from "svelte"

  import { afterNavigate } from "$app/navigation"
  import { page } from "$app/stores"

  import { tracker } from "$lib/stores/tracker"

  export let url: string = import.meta.env.VITE_MATOMO_URL
  export let siteId: number = import.meta.env.VITE_MATOMO_SITE_ID
  export let cookies = true
  export let consentRequired = false
  export let doNotTrack = false
  export let heartBeat = 15

  async function initializeMatomo() {
    const matomo = window.Matomo
    if (!matomo) return
    const track = matomo.getTracker(`${url}/matomo.php`, siteId)
    if (!track) return

    if (!cookies) track.disableCookies()
    if (consentRequired) track.requireConsent()
    if (doNotTrack) track.setDoNotTrack(true)
    if (heartBeat) track.enableHeartBeatTimer(heartBeat)

    tracker.set(track)

    track.setCustomDimension(1, $page.data.user ? "true" : "false")
    track.setCustomUrl($page.url.href)
    track.trackPageView()
  }

  onMount(async () => {
    setTimeout(initializeMatomo, 100)
  })

  afterNavigate(async ({ to }) => {
    if (!$tracker) {
      await initializeMatomo()
      return
    }

    if (to?.url.href && $tracker) {
      $tracker.setCustomDimension(1, $page.data.user ? "true" : "false")
      $tracker.setCustomUrl(to.url.href)
      $tracker.trackPageView()
    }
  })
</script>

<svelte:head>
  {#if url}
    <script async defer src={`${url}/matomo.js`}></script>
  {/if}
</svelte:head>
