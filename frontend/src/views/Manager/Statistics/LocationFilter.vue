<template>
  <div class="location-filter form-group">
    <label>Country/Region</label>
    <div class="input-group">
      <div class="multiselect-div">
        <multi-select
          :options="regions"
          :value="selectedRegion"
          label="name"
          select-label=""
          placeholder="Region"
          @input="(r) => $emit('updateRegion', r)"
        />
      </div>
      <div class="multiselect-div">
        <multi-select
          :options="countries"
          :value="selectedCountry"
          label="name"
          select-label=""
          placeholder="Country"
          @input="(c) => $emit('updateCountry', c)"
        />
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "LocationFilter",
    props: ["regions", "countries", "selectedRegion", "selectedCountry"],
  };
</script>
