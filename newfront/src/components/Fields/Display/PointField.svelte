<script lang="ts">
  import type { FormField } from "$components/Fields/fields";

  export let formfield: FormField;
  export let value: object[];
  export let model: string;
</script>

<div class="point_field">
  {#if value.lat}
    <div>Lat: {parseFloat(value.lat.toFixed(8))}</div>
  {/if}
  {#if value.lng}
    <div>Lng: {parseFloat(value.lng.toFixed(8))}</div>{/if}
</div>
