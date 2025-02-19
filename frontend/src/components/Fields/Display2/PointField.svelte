<script lang="ts">
  import type { Point } from "geojson"

  interface Props {
    value: Point | null
  }

  let { value }: Props = $props()
</script>

{#if value}
  <div>Long: {parseFloat(value.coordinates[0].toFixed(6))}</div>
  <div>Lat: {parseFloat(value.coordinates[1].toFixed(6))}</div>
{/if}
