<script lang="ts">
  import * as turf from "@turf/turf"
  import type { Point } from "geojson"
  import { _ } from "svelte-i18n"

  import { LABEL_CLASS, VALUE_CLASS, WRAPPER_CLASS } from "$components/Fields/consts"
  import Label2 from "$components/Fields/Display2/Label2.svelte"

  export let value: Point | null
  export let fieldname: string
  export let label = ""
  export let wrapperClass = WRAPPER_CLASS
  export let labelClass = LABEL_CLASS
  export let valueClass = VALUE_CLASS

  let latitude: number | null = value ? value.coordinates[1] : null
  let longitude: number | null = value ? value.coordinates[0] : null

  $: value =
    latitude && longitude ? turf.geometry("Point", [longitude, latitude]) : null
</script>

<div class={wrapperClass} data-fieldname={fieldname}>
  {#if label}
    <Label2 value={label} class={labelClass} />
  {/if}
  <div class={valueClass}>
    <div>
      <small class="-mb-0.5">{$_("Latitude")}</small>
      <input
        class="inpt"
        type="number"
        bind:value={latitude}
        required={!!longitude}
        placeholder="-90 to 90"
        min={-90}
        max={90}
        step={0.1 ** 5}
      />
    </div>
    <div>
      <small class="-mb-0.5">{$_("Longitude")}</small>
      <input
        class="inpt"
        type="number"
        bind:value={longitude}
        required={!!latitude}
        placeholder="-180 to 180"
        min={-180}
        max={180}
        step={0.1 ** 5}
      />
    </div>
  </div>
</div>

<style>
  /* Chrome, Safari, Edge, Opera */
  input::-webkit-outer-spin-button,
  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  /* Firefox */
  input[type="number"] {
    -moz-appearance: textfield;
  }
</style>
