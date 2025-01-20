<script lang="ts">
  import type { Point } from "geojson"

  interface Props {
    value: Point | null
  }

  let { value }: Props = $props()
</script>

{#if value}
  <div>Lat: {parseFloat(value.coordinates[1].toFixed(8))}</div>
  <div>Lng: {parseFloat(value.coordinates[0].toFixed(8))}</div>
{/if}
