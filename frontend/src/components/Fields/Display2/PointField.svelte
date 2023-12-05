<script lang="ts">
  import type { Point } from "geojson"

  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: Point | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = "mb-3 flex flex-wrap leading-5"
  export let labelClass = "md:w-5/12 lg:w-4/12"
  export let valueClass = "text-lm-dark dark:text-white md:w-7/12 lg:w-8/12"
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
