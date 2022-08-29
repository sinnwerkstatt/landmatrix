<script lang="ts">
  export let value: { lat: number; lng: number }
</script>

<div class="point_field">
  {#if value.lat}
    <div>Lat: {parseFloat(value.lat.toFixed(8))}</div>
  {/if}
  {#if value.lng}
    <div>Lng: {parseFloat(value.lng.toFixed(8))}</div>{/if}
</div>
