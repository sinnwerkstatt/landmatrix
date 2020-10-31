<template>
  <div class="form-field row">
    <div class="label" :class="labelClasses">
      {{ formfield.label }}
    </div>
    <div class="val" :class="valClasses">
      <div v-if="readonly">
        <span v-if="val.lat">Lat: {{ parseFloat(val.lat.toFixed(8)) }}</span>
        <span v-if="val.lng">Lng: {{ parseFloat(val.lng.toFixed(8)) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
  import { fieldMixin } from "./fieldMixin";

  export default {
    mixins: [fieldMixin],
  };
</script>

<style scoped>
  span {
    display: block;
  }
</style>
