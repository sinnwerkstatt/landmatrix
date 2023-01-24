<script lang="ts">
  import type { FormField } from "$components/Fields/fields"

  export let value: { lat?: number; lng?: number } | null
  export let formfield: FormField

  // @fixme JSON_Field
  $: value = value ?? {}
</script>

<div class="point_field" data-name={formfield?.name ?? ""}>
  {#if value.lat}
    <div>Lat: {parseFloat(value.lat.toFixed(8))}</div>
  {/if}
  {#if value.lng}
    <div>Lng: {parseFloat(value.lng.toFixed(8))}</div>
  {/if}
</div>
