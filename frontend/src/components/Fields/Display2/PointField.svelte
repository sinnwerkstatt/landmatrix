<script lang="ts">
  import type { Point } from "geojson"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: Point | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS
</script>

{#if value}
  <div class={wrapperClass} data-fieldname={fieldname}>
    {#if label}
      <Label2 value={label} class={labelClass} />
    {/if}
    <div class={valueClass}>
      {#if value.coordinates[1]}
        <div>Lat: {parseFloat(value.coordinates[1].toFixed(8))}</div>
      {/if}
      {#if value.coordinates[0]}
        <div>Lng: {parseFloat(value.coordinates[0].toFixed(8))}</div>
      {/if}
    </div>
  </div>
{/if}
