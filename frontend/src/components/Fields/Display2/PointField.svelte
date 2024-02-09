<script lang="ts">
  import type { Point } from "geojson"

  export let value: Point | null
</script>

{#if value}
  <div>Lat: {parseFloat(value.coordinates[1].toFixed(8))}</div>
  <div>Lng: {parseFloat(value.coordinates[0].toFixed(8))}</div>
{/if}
