<script lang="ts">
  import { createEventDispatcher, onMount } from "svelte";
  // import LeafletMap from "$components/Map/LeafletMap.svelte";
  import { baseLayers } from "$components/Map/layers";
  // import { TileLayer } from "leaflet";
  import { browser } from "$app/env";
  // import iconRetinaUrl from "static/images/marker-icon-2x.png";
  // import iconUrl from "$static/images/marker-icon.png";
  // import shadowUrl from "$static/images/marker-shadow.png";
  const dispatch = createEventDispatcher();

  let lmap;
  function mapReady(map) {
    lmap = map.detail;
    dispatch("ready", lmap);
    console.log(lmap);
    baseLayers.forEach((lay) => {
      // new TileLayer(lay.url, {
      //   attribution: lay.attribution,
      // }).addTo(lmap);
    });
  }

  // import { Icon, Map } from "leaflet";
  // import { GestureHandling } from "leaflet-gesture-handling";
  // import "leaflet-gesture-handling/dist/leaflet-gesture-handling.css";
  // import "leaflet/dist/leaflet.css";

  // Map.addInitHook("addHandler", "gestureHandling", GestureHandling);

  // @ts-ignore
  // delete Icon.Default.prototype._getIconUrl;
  // let shadowSize = [0, 0];
  // Icon.Default.mergeOptions({ iconRetinaUrl, iconUrl, shadowUrl, shadowSize });

  export let options = {};
  export let containerClass = "";
  export let hideLayerSwitcher = false;

  let LMap;

  // computed: {

  //   visibleLayer() {
  //     return this.$store.state.visibleLayer;
  //   },
  let mapOptions = {
    zoomSnap: 0.5,
    minZoom: 1,
    zoom: 3,
    zoomControl: true,
    gestureHandling: true,
    ...options,
  };

  let LeafletContainer;
  onMount(async () => {
    if (browser) {
      LeafletContainer = (await import("$components/Map/LeafletMap.svelte")).default;
    }
  });
</script>

<div class="mx-auto relative {containerClass}">
  {#if browser}
    <svelte:component this={LeafletContainer} />
  {/if}
  <!--  <LeafletMap options={mapOptions} on:ready={mapReady} />-->
  <!--    <BigMapStandaloneLayerSwitcher v-if="!hideLayerSwitcher" />-->
</div>
