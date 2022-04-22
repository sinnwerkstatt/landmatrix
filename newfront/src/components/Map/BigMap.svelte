<script lang="ts">
  import "leaflet/dist/leaflet.css";
  import { createEventDispatcher, onDestroy, onMount, setContext } from "svelte";
  import { baseLayers } from "$components/Map/layers";

  export let options = {};
  export let containerClass = "";
  export let showLayerSwitcher = true;

  const dispatch = createEventDispatcher();

  let map;
  setContext("BigMap", { getMap: () => map });

  // import { Icon, Map } from "leaflet";
  // import { GestureHandling } from "leaflet-gesture-handling";
  // import "leaflet-gesture-handling/dist/leaflet-gesture-handling.css";
  // import "leaflet/dist/leaflet.css";

  // Map.addInitHook("addHandler", "gestureHandling", GestureHandling);

  async function initializeMap() {
    const L = (await import("leaflet")).default;
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: "/images/marker-icon-2x.png",
      iconUrl: "/images/marker-icon.png",
      shadowUrl: "/images/marker-shadow.png",
      shadowSize: [0, 0],
    });

    map = L.map("bigmap", {
      zoomSnap: 0.5,
      minZoom: 1,
      zoom: 3,
      zoomControl: true,
      gestureHandling: true,
      ...options,
    });

    map.whenReady(() => dispatch("ready", map));

    baseLayers.forEach((lay) => {
      new L.TileLayer(lay.url, {
        attribution: lay.attribution,
      }).addTo(map);
    });
  }

  onMount(() => initializeMap());
  onDestroy(() => map && map.remove());
</script>

<div class="mx-auto relative {containerClass}">
  <div id="bigmap" class="h-full w-full" />
  {#if showLayerSwitcher}
    <div>huhu</div>
  {/if}
  <!--    <BigMapStandaloneLayerSwitcher v-if="!hideLayerSwitcher" />-->
</div>
