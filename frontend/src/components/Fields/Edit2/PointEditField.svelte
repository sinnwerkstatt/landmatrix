<script lang="ts">
  import * as turf from "@turf/turf"
  import type { Point } from "geojson"
  import { _ } from "svelte-i18n"

  export let value: Point = turf.geometry("Point", [0, 0])
  export let fieldname: string

  export const extras = {}
</script>

<div class="flex gap-2">
  <div class="w-1/2">
    <small class="-mb-0.5">{$_("Longitude")}</small>
    <input
      class="inpt"
      name="{fieldname}_longitude"
      type="number"
      bind:value={value.coordinates[0]}
      required={!!value.coordinates[1]}
      placeholder="-180 to 180"
      min={-180}
      max={180}
      step={0.1 ** 5}
    />
  </div>
  <div class="w-1/2">
    <small class="-mb-0.5">{$_("Latitude")}</small>
    <input
      class="inpt"
      name="{fieldname}_latitude"
      type="number"
      bind:value={value.coordinates[1]}
      required={!!value.coordinates[0]}
      placeholder="-90 to 90"
      min={-90}
      max={90}
      step={0.1 ** 5}
    />
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
