<template>
  <div>
    <div v-if="value.lat">Lat: {{ parseFloat(value.lat.toFixed(8)) }}</div>
    <div v-if="value.lng">Lng: {{ parseFloat(value.lng.toFixed(8)) }}</div>
  </div>
</template>

<script>
  export default {
    props: {
      formfield: { type: Object, required: true },
      value: { type: Object, required: true },
      model: { type: String, required: true },
    },
  };
</script>
