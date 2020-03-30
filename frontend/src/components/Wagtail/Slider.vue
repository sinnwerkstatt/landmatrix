<template>
  <b-carousel
    :id="value.id"
    :interval="3000"
    controls
    indicators
    style="width: 100%; height: 100%;"
  >
    <b-carousel-slide v-for="image in value.images" :key="image.id">
      <template v-slot:img>
        <wagtail-image :value="image" />
      </template>
    </b-carousel-slide>
  </b-carousel>
</template>

<script>
  export default {
    props: ["value"],
  };
</script>

<style scoped></style>
