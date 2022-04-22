<script lang="ts">
  import type { MapOptions } from "leaflet";
  import "leaflet/dist/leaflet.css";
  import { Icon, Map } from "leaflet?client";
  import { createEventDispatcher, onDestroy, onMount } from "svelte";
  import LoadingPulse from "$components/LoadingPulse.svelte";
  import { baseLayers, visibleLayer } from "$components/Map/layers";

  export let options: MapOptions = {};
  export let containerClass = "";
  export let showLayerSwitcher = true;

  const dispatch = createEventDispatcher();

  let map;

  // import { GestureHandling } from "leaflet-gesture-handling";
  // import "leaflet-gesture-handling/dist/leaflet-gesture-handling.css";
  // Map.addInitHook("addHandler", "gestureHandling", GestureHandling);
  if (!import.meta.env.SSR) {
    delete Icon.Default.prototype._getIconUrl;
    Icon.Default.mergeOptions({
      iconRetinaUrl: "/images/marker-icon-2x.png",
      iconUrl: "/images/marker-icon.png",
      shadowUrl: "/images/marker-shadow.png",
      shadowSize: [0, 0],
    });
  }

  onMount(() => {
    map = new Map("bigmap", {
      zoomSnap: 0.5,
      minZoom: 1,
      zoom: 3,
      zoomControl: true,
      // gestureHandling: true,
      ...options,
    });
    map.whenReady(() => dispatch("ready", map));
  });
  onDestroy(() => map && map.remove());

  $: if (map && $visibleLayer) {
    baseLayers.forEach((l) => {
      if (l.name === $visibleLayer) l.layer.addTo(map);
      else l.layer.remove();
    });
  }
</script>

<div class="mx-auto relative {containerClass}">
  <!--  z-0 is important to capture and contextualize leaflet's "400" z-index -->
  <div id="bigmap" class="h-full w-full z-0">
    {#if !map}
      <LoadingPulse class="h-[300px]" />
    {/if}
  </div>
  {#if showLayerSwitcher}
    <div>huhu</div>
    <!--    <BigMapStandaloneLayerSwitcher />-->
  {/if}
</div>
