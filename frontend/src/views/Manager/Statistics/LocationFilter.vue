<template>
  <div class="location-filter form-group">
    <label>Country/Region</label>
    <div class="input-group">
      <div class="multiselect-div">
        <multiselect
          :value="selectedRegion"
          :options="regions"
          label="name"
          placeholder="Region"
          @input="(r) => $emit('updateRegion', r)"
        />
      </div>
      <div class="multiselect-div">
        <multiselect
          :value="selectedCountry"
          :options="countries"
          label="name"
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
  props: ['regions', 'countries', 'selectedRegion', 'selectedCountry'],
}
</script>

<style scoped>

</style>
