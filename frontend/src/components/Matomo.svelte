<script type="ts">
  import { onMount } from "svelte"

  import { afterNavigate } from "$app/navigation"

  // import { delayedCalls } from "$lib/matomo"

  export let url = import.meta.env.VITE_MATOMO_URL
  export let siteId = import.meta.env.VITE_MATOMO_SITE_ID
  export let cookies = true
  export let consentRequired = false
  // export let consentExpires = 0
  export let doNotTrack = false
  export let heartBeat = 2000
  // export let blockLoading = false
  // export let addNoProxyWorkaround = true

  let _matomo
  let scriptUrl

  $: scriptUrl = `${url}/matomo.js`
  $: trackUrl = `${url}/matomo.php`
  $: tracker = _matomo && _matomo.getTracker(trackUrl, siteId)

  $: if (tracker && !cookies) tracker.disableCookies()
  $: if (tracker && consentRequired) tracker.requireConsent()
  $: if (tracker && doNotTrack) tracker.setDoNotTrack()
  $: if (tracker && heartBeat) tracker.enableHeartBeatTimer(heartBeat)

  // $: while (tracker && $delayedCalls.length) {
  //   const [fnName, args] = $delayedCalls.shift()
  //   if (tracker[fnName] instanceof Function) {
  //     // if (debug) console.log("Matomo debug: Calling", fnName, args);
  //     if (!doNotTrack) tracker[fnName](...args)
  //   } else {
  //     throw new Error(`Trying to call nonexistent function ${fnName}`)
  //   }
  // }

  afterNavigate(({ from, to }) => {
    if (to?.url.href && tracker) {
      // console.log("got tracker", tracker)
      // console.log("got tracker", tracker.trackPageView)
      tracker.setCustomUrl(to.url.href)
      tracker.trackPageView()
    }
  })

  onMount(() => {
    _matomo = window.Matomo
  })
</script>

<svelte:head>
  <script async defer src={scriptUrl}></script>
</svelte:head>
