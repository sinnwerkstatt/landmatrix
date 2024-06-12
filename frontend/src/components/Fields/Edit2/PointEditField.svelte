<script lang="ts">
  import type { Point } from "geojson"
  import { _ } from "svelte-i18n"

  export let value: Point | null = null

  $: val = value !== null ? value : { type: "Point", coordinates: [null, null] }

  const onChange = () => {
    value =
      val.coordinates[0] !== null && val.coordinates[1] !== null ? (val as Point) : null
  }

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
      bind:value={val.coordinates[0]}
      required={!!val.coordinates[1]}
      on:change={onChange}
      placeholder="-180 to 180"
      min={-180}
      max={180}
      step={0.1 ** 6}
    />
  </div>
  <div class="w-1/2">
    <small class="-mb-0.5">{$_("Latitude")}</small>
    <input
      class="inpt"
      name="{fieldname}_latitude"
      type="number"
      bind:value={val.coordinates[1]}
      required={!!val.coordinates[0]}
      on:change={onChange}
      placeholder="-90 to 90"
      min={-90}
      max={90}
      step={0.1 ** 6}
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
