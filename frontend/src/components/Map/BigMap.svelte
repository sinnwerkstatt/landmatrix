<script lang="ts">
  import "leaflet/dist/leaflet.css"

  import * as L from "leaflet?client"
  import { geoJson, Map } from "leaflet?client"

  import "leaflet-gesture-handling/dist/leaflet-gesture-handling.css"

  import type { MapOptions } from "leaflet"
  import { GestureHandling } from "leaflet-gesture-handling?client"
  import { nanoid } from "nanoid"
  import { createEventDispatcher, onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { browser } from "$app/environment"

  import LoadingPulse from "$components/LoadingPulse.svelte"

  import BigMapStandaloneLayerSwitcher from "./BigMapStandaloneLayerSwitcher.svelte"
  import type { BaseLayer, ContextLayer } from "./layers"
  import {
    getBaseLayers,
    getContextLayers,
    visibleContextLayers,
    visibleLayer,
  } from "./layers"

  export let options: MapOptions = {}
  export let containerClass = ""
  export let showLayerSwitcher = true

  const dispatch = createEventDispatcher<{ ready: Map }>()

  let mapId = "bigMap-" + nanoid()
  let map: Map | undefined

  if (browser) {
    delete L.Icon.Default.prototype._getIconUrl
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: "/images/marker-icon-2x.png",
      iconUrl: "/images/marker-icon.png",
      shadowUrl: "/images/marker-shadow.png",
      shadowSize: [0, 0],
    })
  }

  let contextLayers: ContextLayer[] = []
  let baseLayers: BaseLayer[] = []

  onMount(async () => {
    if (!browser) return

    contextLayers = getContextLayers($_)
    baseLayers = getBaseLayers($_)
    // onDestroy sometimes triggers after onMount on loading a new map
    // clean up by removing layers from old map
    baseLayers.forEach(l => l.layer.remove())
    contextLayers.forEach(l => l.layer.remove())

    Map.addInitHook("addHandler", "gestureHandling", GestureHandling)

    // create new Map in div with mapId
    map = new Map(mapId, {
      zoomSnap: 0.5,
      minZoom: 1,
      zoom: 3,
      zoomControl: true,
      gestureHandling: true,
      ...options,
    })

    map.whenReady(() => dispatch("ready", map!))
  })

  // See bug ticket #668: Sometimes not called when switching views quickly.
  onDestroy(() => {
    if (map) {
      map.remove()
      map = undefined
    }
  })

  $: if (map && $visibleLayer) {
    baseLayers.forEach(l => {
      if (l.id === $visibleLayer) l.layer.addTo(map!)
      else l.layer.remove()
    })
  }

  $: if (map && $visibleContextLayers) {
    contextLayers.forEach(l => {
      if ($visibleContextLayers.includes(l.id)) l.layer.addTo(map!)
      else l.layer.remove()
    })
  }
</script>

<div class="relative mx-auto {containerClass}">
  <!-- ! isolate is important to capture and contextualize leaflet's "400" z-index -->
  <div class="isolate h-full w-full" id={mapId}>
    {#if !map}
      <LoadingPulse class="h-[300px]" />
    {/if}
  </div>
  {#if showLayerSwitcher}
    <BigMapStandaloneLayerSwitcher />
  {/if}
  <slot />
</div>

<style lang="postcss">
  :global(.leaflet-container a) {
    @apply text-orange;
  }
</style>
