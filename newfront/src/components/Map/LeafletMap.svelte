<script>
  import { createEventDispatcher, setContext } from "svelte";
  import L from "leaflet";
  export let options = {};
  export let events = [];
  let map = null;

  import "leaflet/dist/leaflet.css";

  setContext(L, { getMap: () => map });
  const dispatch = createEventDispatcher();
  function initialize(container) {
    map = L.map(container, options);
    map.whenReady(() => dispatch("ready", map));
    return {
      destroy: () => {
        map.remove();
      },
    };
  }
  export function getMap() {
    return map;
  }
</script>

<div style="height:100%; width:100%;" use:initialize>
  {#if map}
    <slot />
  {/if}
</div>
