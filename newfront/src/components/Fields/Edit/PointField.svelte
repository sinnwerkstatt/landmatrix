<script lang="ts">
  import { _ } from "svelte-i18n";
  import LowLevelDecimalField from "./LowLevelDecimalField.svelte";

  type LatLng = {
    lat?: number;
    lng?: number;
  };
  export let value: LatLng = {};
</script>

<div class="flex gap-1">
  <div class="w-full">
    <div class="text-[12px] -mb-0.5">{$_("Latitude")}</div>
    <LowLevelDecimalField
      on:input
      bind:value={value.lat}
      min="-90"
      max="90"
      decimals="5"
    />
  </div>
  <div class="w-full">
    <div class="text-[12px] -mb-0.5">{$_("Longitude")}</div>
    <LowLevelDecimalField
      on:input
      bind:value={value.lng}
      min="-180"
      max="180"
      decimals="5"
    />
  </div>
</div>
