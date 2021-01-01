<template>
  <div>
    <div>Lat: {{ value.lat }}</div>
    <div>Lng: {{ value.lng }}</div>
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
