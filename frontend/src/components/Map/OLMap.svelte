<script lang="ts">
  import { defaults } from "ol/control"
  import Map from "ol/Map"
  import { fromLonLat } from "ol/proj"
  import View from "ol/View"
  import { onDestroy, onMount, type Snippet } from "svelte"

  import "ol/ol.css"

  import LoadingPulse from "$components/LoadingPulse.svelte"
  import BigMapStandaloneLayerSwitcher from "$components/Map/BigMapStandaloneLayerSwitcher.svelte"
  import {
    baseLayers,
    contextLayers,
    selectedLayers,
  } from "$components/Map/mapstuff.svelte"

  interface Props {
    children?: Snippet
    containerClass?: string
    class?: string
    showLayerSwitcher?: boolean
    mapReady?: (map: Map) => void
    options?: {
      zoom?: number
      minZoom?: number
      center?: [number, number]
      zoomControl?: boolean
    }
  }

  let {
    children,
    containerClass = "",

    class: className = undefined,
    showLayerSwitcher = false,
    mapReady,
    options,
  }: Props = $props()

  let map: Map | undefined = $state()
  let mapDiv: HTMLDivElement | undefined = $state()

  async function mapSetup() {
    const view = new View({
      // projection: "EPSG:4326",
      center: fromLonLat(options?.center ?? [-30, 20]),
      zoom: options?.zoom ?? 0,
      minZoom: options?.minZoom ?? 0,
    })
    map = new Map({
      target: mapDiv,
      controls: defaults({ zoom: options?.zoomControl ?? true }),
      view: view,
    })

    baseLayers.forEach(lX => map!.addLayer(lX.layer))
    contextLayers.forEach(lX => map!.addLayer(lX.layer))

    mapReady?.(map)
  }

  onMount(mapSetup)
  onDestroy(() => {
    if (map) map.setTarget(undefined)
  })

  $effect(() => {
    baseLayers.forEach(lX => {
      lX.layer.setVisible(selectedLayers.baseLayer === lX.id)
    })
  })
  $effect(() => {
    contextLayers.forEach(lX => {
      lX.layer.setVisible(selectedLayers.contextLayers.includes(lX.id))
    })
  })
</script>

<div class="relative mx-auto {containerClass}">
  <div bind:this={mapDiv} class="relative isolate h-full w-full {className}">
    {#if !map}
      <LoadingPulse class="h-[300px]" />
    {:else}
      {#if showLayerSwitcher}
        <BigMapStandaloneLayerSwitcher />
      {/if}
      {@render children?.()}
    {/if}
  </div>
</div>

<style lang="postcss">
  :global(div.ol-zoom) {
    --ol-foreground-color: hsl(32, 97%, 55%);
    --ol-subtle-foreground-color: hsl(32, 97%, 75%);
  }

  :global(.ol-viewport a) {
    @apply text-orange;
  }
</style>
