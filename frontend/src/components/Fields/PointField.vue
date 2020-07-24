<template>
  <div>
    <div v-if="readonly">
      <span v-if="val.lat">Lat: {{ parseFloat(val.lat.toFixed(8)) }}</span>
      <span v-if="val.lng">Lng: {{ parseFloat(val.lng.toFixed(8)) }}</span>
    </div>
  </div>
</template>

<script>
  export default {
    props: ["formfield", "value", "readonly"],
    data() {
      return {
        val: this.value,
      };
    },
    methods: {
      emitVal() {
        this.$emit("input", this.val);
      },
    },
  };
</script>

<style scoped>
  span {
    display: block;
  }
</style>
