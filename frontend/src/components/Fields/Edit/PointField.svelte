<script lang="ts">
  import { _ } from "svelte-i18n"

  import LowLevelDecimalField from "./LowLevelDecimalField.svelte"

  export let value: { lat?: number; lng?: number } | null

  // @fixme JSON_Field
  $: value = value ?? {}
</script>

<div class="flex gap-1">
  <div class="w-full">
    <div class="-mb-0.5 text-[12px]">{$_("Latitude")}</div>
    <LowLevelDecimalField
      on:input
      bind:value={value.lat}
      required={!!value.lng}
      min={-90}
      max={90}
      decimals={5}
      name="point_lat"
    />
  </div>
  <div class="w-full">
    <div class="-mb-0.5 text-[12px]">{$_("Longitude")}</div>
    <LowLevelDecimalField
      on:input
      bind:value={value.lng}
      required={!!value.lat}
      min={-180}
      max={180}
      decimals={5}
      name="point_lng"
    />
  </div>
</div>
