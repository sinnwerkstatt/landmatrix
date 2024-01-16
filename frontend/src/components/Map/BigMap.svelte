<script lang="ts">
  import { geoJson, type MapOptions } from "leaflet"

  import "leaflet-gesture-handling/dist/leaflet-gesture-handling.css"

  import { GestureHandling } from "leaflet-gesture-handling?client"

  import "leaflet/dist/leaflet.css"

  import { Icon, Map } from "leaflet?client"
  import { nanoid } from "nanoid"
  import { createEventDispatcher, onDestroy, onMount } from "svelte"
  import { _ } from "svelte-i18n"

  import { geoJsonLayerGroup } from "$lib/stores"
  import { padBounds } from "$lib/utils/location"

  import LoadingPulse from "$components/LoadingPulse.svelte"
  import {
    getBaseLayers,
    getContextLayers,
    visibleContextLayers,
    visibleLayer,
  } from "$components/Map/layers"

  import BigMapStandaloneLayerSwitcher from "./BigMapStandaloneLayerSwitcher.svelte"

  export let options: MapOptions = {}
  export let containerClass = ""
  export let showLayerSwitcher = true

  const dispatch = createEventDispatcher<{ ready: Map }>()

  let mapId = "bigMap-" + nanoid()
  let map: Map

  if (!import.meta.env.SSR) {
    // noinspection TypeScriptUnresolvedVariable
    delete Icon.Default.prototype._getIconUrl
    Icon.Default.mergeOptions({
      iconRetinaUrl: "/images/marker-icon-2x.png",
      iconUrl: "/images/marker-icon.png",
      shadowUrl: "/images/marker-shadow.png",
      shadowSize: [0, 0],
    })
  }

  $: contextLayers = getContextLayers($_)
  $: baseLayers = getBaseLayers($_)

  onMount(async () => {
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

    if (!$geoJsonLayerGroup) {
      $geoJsonLayerGroup = geoJson()
      $geoJsonLayerGroup.on("layeradd layerremove", function () {
        // console.log("add or rm")
        const bounds = this.getBounds()
        bounds.isValid() && map.fitBounds(padBounds(bounds), { duration: 1 })
      })
    }

    map.addLayer($geoJsonLayerGroup)

    map.whenReady(() => {
      dispatch("ready", map)
    })
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
      if (l.id === $visibleLayer) l.layer.addTo(map)
      else l.layer.remove()
    })
  }

  $: if (map && $visibleContextLayers) {
    contextLayers.forEach(l => {
      if ($visibleContextLayers.includes(l.id)) l.layer.addTo(map)
      else l.layer.remove()
    })
  }
</script>

<div class="relative mx-auto {containerClass}">
  <!-- ! isolate is important to capture and contextualize leaflet's "400" z-index -->
  <div id={mapId} class="isolate h-full w-full">
    {#if !map}
      <LoadingPulse class="h-[300px]" />
    {/if}
  </div>
  {#if showLayerSwitcher}
    <BigMapStandaloneLayerSwitcher />
  {/if}
  <slot />
</div>

<style>
  :global(.leaflet-container a) {
    @apply text-orange;
  }
</style>
