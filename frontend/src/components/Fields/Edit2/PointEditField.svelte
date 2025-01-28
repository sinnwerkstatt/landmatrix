<script lang="ts">
  import type { Point } from "geojson"
  import { _ } from "svelte-i18n"

  interface Props {
    value?: Point | null
    fieldname: string
    onchange?: () => void
  }

  let { value = $bindable(), fieldname, onchange }: Props = $props()

  let longitude: number | null = $state(null)
  let latitude: number | null = $state(null)

  $effect(() => {
    if (value) {
      longitude = value.coordinates[0]
      latitude = value.coordinates[1]
    }
  })

  const onInputChange = () => {
    if (longitude === null && latitude === null) {
      value = null
    }
    if (longitude !== null && latitude !== null) {
      value = $state.snapshot({ type: "Point", coordinates: [longitude, latitude] })
    }
    onchange?.()
  }
</script>

<div class="flex gap-2">
  <div class="w-1/2">
    <label for="{fieldname}_longitude">
      <small class="-mb-0.5">{$_("Longitude")}</small>
    </label>
    <input
      class="inpt"
      id="{fieldname}_longitude"
      type="number"
      bind:value={longitude}
      required={latitude !== null}
      onchange={onInputChange}
      placeholder="-180 to 180"
      min={-180}
      max={180}
      step={0.1 ** 6}
    />
  </div>

  <div class="w-1/2">
    <label for="{fieldname}_latitude">
      <small class="-mb-0.5">{$_("Latitude")}</small>
    </label>
    <input
      class="inpt"
      id="{fieldname}_latitude"
      type="number"
      bind:value={latitude}
      required={longitude !== null}
      onchange={onInputChange}
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
    appearance: textfield;
  }
</style>
