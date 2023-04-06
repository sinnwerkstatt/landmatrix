<script lang="ts">
  import { afterNavigate } from "$app/navigation"
  import { page } from "$app/stores"
  import { onMount } from "svelte"
  import { writable } from "svelte/store"

  export let url = import.meta.env.VITE_MATOMO_URL
  export let siteId = import.meta.env.VITE_MATOMO_SITE_ID
  export let cookies = true
  export let consentRequired = false

  export let doNotTrack = false
  export let heartBeat = 2000

  let tracker = writable()

  interface Tracker {
    disableCookies()
    requireConsent()
    setDoNotTrack()
    enableHeartBeatTimer(heartBeat)
    setCustomUrl(url): void
    setCustomDimension(dimension, value): void
    trackPageView(): void
  }
  interface Matomo {
    getTracker(trackerUrl, siteId): Tracker | undefined
  }
  async function initializeMatomo() {
    const _matomo: Matomo | undefined = window.Matomo
    if (!_matomo) return
    const track = _matomo.getTracker(`${url}/matomo.php`, siteId)
    if (!track) return

    if (!cookies) track.disableCookies()
    if (consentRequired) track.requireConsent()
    if (doNotTrack) track.setDoNotTrack()
    if (heartBeat) track.enableHeartBeatTimer(heartBeat)
    await tracker.set(track)

    track.setCustomDimension("LoggedIn", !!$page.data.user)
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
      $tracker.setCustomDimension("LoggedIn", !!$page.data.user)
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
